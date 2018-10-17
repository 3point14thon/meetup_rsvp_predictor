import requests
from time import sleep
from api_key import api_key
import psycopg2 as pg2

class MeetupApiClient:
    '''
    A class that requests information from meetup.com.

    Attributes:
    meetup_url, the base url for meetups api
    url_code_log, a log containing the url responses from a call to
                  find_past_events

    Methodes:
    get_item,
        input: api_method as a string,
               parameters as a dicitonary
        ouput: a url request object
    get_groups,
        input: parameters as a dicitonary
        ouput: a url request object
    get_events,
        input: parameters as a dicitonary
        ouput: a url request object
    find_past_events,
        input: location as a dictionary(to be used as parameters),
               end_date as a string representing milliseconds from the epoch,
               start_date as a string representing milliseconds from the epoch
        output: all events in the specified location within the specified
                location as a dictionary,
                {group_name: [json dict of events, lat, lon]}
    '''
    def __init__(self):
        self.meetup_url = 'https://api.meetup.com/'
        self.cur = None
        self.conn = None
        self.connect_db()

    def connect_db(self):
        self.conn = pg2.connect(dbname='meetups', user = 'postgres',
                           password = 'password', host = 'localhost')
        self.cur = self.conn.cursor()

    def make_group_key(self, api_method, parameters):
        if api_method == 'find/groups':
            for key in parameters:
                api_method += parameters[key]
            return api_method
        else:
            return api_method

    def cache_if_new(self, id_, api_method, parameters):
        res = self.get_item(api_method, parameters)
        if (res.status_code != 404 and
            self.not_in_table('meta_data', 'url', res.url)):
            if 'find/groups' in api_method :
                self.insert_meta(res)
                for group in res.json():
                    self.insert_group(group, res.url)
            else:
                self.insert_meta(res)
                #self.insert_event()
            self.api_cooldown(res.headers)
        return res.headers

    def insert_meta(self, res):
        values = (res.url, res.headers['link'],
                  res.status_code, res.headers['date'])
        cols = ('url', 'rel_links', 'url_code', 'req_date')
        self.insert_values('meta_data', values, cols)

    def insert_group(self, group, meta_data_url):
        if self.not_in_table('meetup_group', 'id', group['id']):
            cols = ('id',
                    'meta_data_url',
                    'created',
                    'name',
                    'join_mode',
                    'lat',
                    'lon',
                    'urlname',
                    'who',
                    'localized_location',
                    'region',
                    'timezone',
                    'pro_network_urlname',
                    'category_id',
                    'visibility',
                    'key_photo_id',
                    'questions_req',
                    'photo_req',
                    'past_event_count',
                    'members',
                    'description')
            values = self.find_values(group, cols)
            values[cols.index('meta_data_url')] = meta_data_url
            self.update_group_reltables(group, cols, values)
            self.insert_values('meetup_group', values, cols)

    def update_group_reltables(self, group, cols, values):
        if 'pro_network' in group:
            values[cols.index('pro_network_urlname')] = group['pro_network']['network_url']
            self.insert_pronet(group['pro_network'])
        if 'category' in group:
            values[cols.index('category_id')] = group['category']['id']
            self.insert_category(group['category'])
        if 'key_photo' in group:
            values[cols.index('key_photo_id')] = group['key_photo']['id']
            self.insert_photo(group['key_photo'])
        if 'join_info' in group:
            values[cols.index('photo_req')] = group['join_info']['photo_req']
            values[cols.index('questions_req')] = group['join_info']['questions_req']
            for question in group['join_info']['questions']:
                self.insert_question(question)
                self.insert_values('group_questions', (group['id'], question['id']))
        if 'topics' in group:
            for topic in group['topics']:
                self.insert_topic(topic)
                self.insert_values('group_topics', (group['id'], topic['id']))
        return values

    def insert_event(self, event):
        if self.not_in_table('event', 'id', event['id']):
            cols = ('id',
                    'meta_data_url',
                    'created',
                    'description',
                    'duration',
                    'featured',
                    'featured_photo_id',
                    'meetup_group_id',
                    'how_to_find_us',
                    'link',
                    'local_date',
                    'local_time',
                    'manual_attendance_count',
                    'name',
                    'plain_text_no_images_description',
                    'pro_is_email_shared',
                    'rsvp_close_offset',
                    'rsvp_limit',
                    'rsvp_open_offset',
                    'series_id',
                    'time_since_epoch',
                    'updated',
                    'utc_offset',
                    'venue_id',
                    'visibility',
                    'waitlist_count',
                    'why',
                    'yes_rsvp_count')
            values = self.find_values(event, cols)
            values = self.update_event_reltables(event, cols, values)
            self.insert_values('event', values, cols)

    def update_event_reltables(self, event, cols, values):
        if 'featured_photo' in event:
            values[cols.index('featured_photo')] = event['featured_photo']['id']
            self.insert_photo(event['featured_photo'])
        if 'group' in event:
            values[cols.index('meetup_group_id')] = event['group']['id']
        if 'key_photo' in event:
            values[cols.index('key_photo_id')] = event['key_photo']['id']
            self.insert_photo(event['key_photo'])
        if 'series' in event:
            values[cols.index('series')] = event['series']['id']
            self.insert_photo(event['series'])
        if 'venue' in event:
            values[cols.index('venue_id')] = event['venue']['id']
            self.insert_photo(event['venue'])
        if 'event_hosts' in event:
            for host in event['event_hosts']:
                self.insert_host(host)
                self.insert_values('hosted', (event['id'], host['id']))
        return values

    def insert_host(self, host):
        if self.not_in_table('host', 'id', host['id']):
            cols = ('id',
                    'name',
                    'intro',
                    'photo_id',
                    'host_count',
                    'join_date',
                    'role')
            values = self.find_values(host, cols)
            if 'photo' in host:
                values[cols.index('photo_id')] = host['photo']['id']
                self.insert_photo(host['photo'])
            self.insert_values('host', values, cols)

    def insert_series(self, series):
        if self.not_in_table('series', 'id', series['id']):
            cols = ('id',
                    'description',
                    'end_date',
                    'start_date',
                    'template_event_id')
            values = self.find_values(series, cols)
            self.insert_values('series', values, cols)

    def insert_venue(self, venue):
        if self.not_in_table('venue', 'id', venue['id']):
            cols = ('id',
                    'address_1',
                    'address_2',
                    'address_3',
                    'city',
                    'country',
                    'localized_country_name',
                    'lat',
                    'lon',
                    'name',
                    'phone',
                    'repinned',
                    'state',
                    'zip')
            values = self.find_values(venue, cols)
            self.insert_values('venue', values, cols)

    def insert_values(self, table, values, cols = ''):
        place_holder = '%s,' * len(values)
        if cols != '':
            cols = str(tuple(cols)).replace("'", "")
        self.cur.execute(f"INSERT INTO {table} {cols} VALUES ({place_holder[0:-1]});", values)
        self.conn.commit()

    def find_values(self, item, cols):
        values = []
        for col in cols:
            if col in item:
                values.append(item[col])
            else:
                values.append(None)
        return values

    def not_in_table(self, table, id_name, item):
        selection = f"SELECT {id_name} FROM {table}"
        condition = f" WHERE {id_name}='{item}';"
        self.cur.execute(selection + condition)
        querry = self.cur.fetchone()
        return not querry or item not in querry

    def insert_pronet(self, net):
        if self.not_in_table('pro_network', 'id', net['urlname']):
            cols = ('name',
                    'urlname',
                    'number_of_groups',
                    'network_url')
            values = self.find_values(net, cols)
            self.insert_values('pro_network', values, cols)

    def insert_topic(self, topic):
        if self.not_in_table('topic', 'id', topic['id']):
            cols = ('id',
                    'name',
                    'urlkey',
                    'lang')
            values = self.find_values(topic, cols)
            self.insert_values('topic', values, cols)

    def insert_category(self, category):
        if self.not_in_table('category', 'id', category['id']):
            cols = ('id',
                    'name',
                    'shortname',
                    'sortname')
            values = self.find_values(category, cols)
            self.insert_values('category', values, cols)

    def insert_photo(self, photo):
        if self.not_in_table('photo', 'id', photo['id']):
            cols = ('id',
                    'base_url',
                    'highres_link',
                    'photo_link',
                    'thumb_link',
                    'type')
            values = self.find_values(photo, cols)
            self.insert_values('photo', values, cols)

    def insert_question(self, question):
        if self.not_in_table('questions', 'id', question['id']):
            cols = ('id',
                    'question')
            values = self.find_values(question, cols)
            self.insert_values('questions', values, cols)

    def partition_link(self, header):
        return header['Link'].partition(',')[0].partition(';')

    def has_next(self, header):
        return self.partition_link(header)[2] == ' rel="next"'

    def next_link(self, header):
        return self.partition_link(header)[0].strip('<>')

    def get_items(self, api_method, parameters):
        id_ = self.make_group_key(api_method, parameters)
        parameters['key'] = api_key()
        api_method = self.meetup_url + api_method
        header = self.cache_if_new(id_, api_method, parameters)
        #import pdb; pdb.set_trace()
        while 'Link' in header and self.has_next(header):
            header = self.cache_if_new(id_=self.next_link(header),
                                       api_method=self.next_link(header),
                                       parameters={'key': api_key()})

    def get_item(self, api_method, parameters):
        n = 0
        response = requests.get(api_method, parameters)
        while (response.status_code == 400) and (n != 100):
            response = requests.get(api_method, parameters)
            n += 1
        return response

    def api_cooldown(self, header):
        if (header['X-RateLimit-Remaining']) == '0':
            sleep(float(header['X-RateLimit-Reset']))

    def get_groups(self, params):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/find/groups/
        self.get_items('find/groups', params)

    def get_events(self, params, urlname):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/:urlname/events/
        self.get_items(urlname + '/events', params)


    def find_past_events(self, start_date, end_date, group_table, event_table):
        '''
        inconsistant on how many 400 errors are returned, might depend on
        internet connection
        '''
        super_groups = group_table.find(no_cursor_timeout=True)
        for groups in super_groups:
            for group in groups['data']:
                group_name = group['urlname']
                params = {'fields': ','.join([
                              'event_hosts',
                              'featured',
                              'featured_photo',
                              'fee_options',
                              'group_category',
                              'group_join_info',
                              'group_key_photo',
                              'group_membership_dues',
                              'best_topics',
                              'group_past_event_count',
                              'group_photo',
                              'group_pro_network',
                              'group_topics',
                              'group_join_info',
                              'how_to_find_us',
                              'group_visibility',
                              'plain_text_no_images_description',
                              'rsvp_rules',
                              'series',
                              'answers']),
                          'no_earlier_than': start_date,
                          'no_later_than': end_date,
                          'status': 'past'}
                self.get_events(params, group_name)
