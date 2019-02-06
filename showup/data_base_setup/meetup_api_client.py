import requests
from time import sleep
from api_key import api_key
from db_info import db_info
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
        db = db_info()
        self.conn = pg2.connect(dbname=db['dbname'], user=db['username'],
                                password=db['password'], host=db['host'],
                                port=db['port'])
        self.cur = self.conn.cursor()

    def cache_if_new(self, api_method, parameters):
        res = self.get_item(api_method, parameters)
        if self.not_in_table('meta_data', 'url', res.url):
            if res.status_code == 200:
                if 'find/groups' in api_method:
                    insert = self.insert_group
                else:
                    insert = self.insert_event
                for item in res.json():
                    insert(item, res.url)
            self.insert_meta(res)
        if 'Link' in res.headers:
            return (res.headers['Link'], res.url)
        else:
            return (None, res.url)

    def insert_meta(self, res):
        if 'Link' in res.headers:
            link = res.headers['Link']
        else:
            link = None
        values = (res.url, link,
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
            if 'questions' in group['join_info']:
                for question in group['join_info']['questions']:
                    self.insert_question(question)
                    self.insert_values('group_questions', (group['id'], question['id']))
        if 'topics' in group:
            for topic in group['topics']:
                self.insert_topic(topic)
                self.insert_values('group_topics', (group['id'], topic['id']))
        return values

    def insert_event(self, event, metadata_url):
        if event and self.not_in_table('event', 'id', event['id']):
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
            values[cols.index('meta_data_url')] = metadata_url
            values = self.update_event_reltables(event, cols, values)
            self.insert_values('event', values, cols)

    def update_event_reltables(self, event, cols, values):
        if 'featured_photo' in event:
            values[cols.index('featured_photo_id')] = event['featured_photo']['id']
            self.insert_photo(event['featured_photo'])
        if 'group' in event:
            values[cols.index('meetup_group_id')] = event['group']['id']
        if 'key_photo' in event:
            values[cols.index('key_photo_id')] = event['key_photo']['id']
            self.insert_photo(event['key_photo'])
        if 'series' in event:
            values[cols.index('series_id')] = event['series']['id']
            self.insert_series(event['series'])
        if 'venue' in event:
            values[cols.index('venue_id')] = event['venue']['id']
            self.insert_venue(event['venue'])
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
            if 'monthly' in series:
                self.insert_monthly(series['monthly'], series['id'])
            if 'weekly' in series:
                self.insert_weekly(series['weekly'], series['id'])
            self.insert_values('series', values, cols)

    def insert_monthly(self, monthly, id):
        cols = ('series_id',
                'day_of_week',
                'series_interval',
                'week_of_month')
        values = self.find_values(monthly, cols)
        values[cols.index('series_id')] = id
        values[cols.index('series_interval')] = monthly['interval']
        self.insert_values('monthly_series', values, cols)

    def insert_weekly(self, weekly, id):
        cols = ('series_id',
                'series_interval',
                'monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday')
        dow = dict(zip(range(1, 8), cols[2:]))
        values = self.find_values(weekly, cols)
        values[cols.index('series_id')] = id
        values[cols.index('series_interval')] = weekly['interval']
        for day in weekly['days_of_week']:
            values[cols.index(dow[day])] = True
        self.insert_values('weekly_series', values, cols)

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

    def querry_table(self, table, id_name, condition, item):
        selection = f"SELECT {id_name} FROM {table}"
        condition = f" WHERE {condition}='{item}';"
        self.cur.execute(selection + condition)
        if self.cur.fetchone():
            return self.cur.fetchone()
        else:
            return (None,)

    def not_in_table(self, table, id_name, item):
        querry = self.querry_table(table, id_name, id_name, item)
        return not querry or item not in querry

    def insert_pronet(self, net):
        if self.not_in_table('pro_network', 'urlname', net['urlname']):
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

    def partition_link(self, link):
        return link.partition(',')[0].partition(';')

    def has_next(self, link):
        return self.partition_link(link)[2] == ' rel="next"'

    def next_link(self, link):
        return self.partition_link(link)[0].strip('<>')

    def get_items(self, api_method, parameters):
        parameters['key'] = api_key()
        api_method = self.meetup_url + api_method
        links = self.cache_if_new(api_method, parameters)
        while links[0]:
            if self.not_in_table('meta_data', 'url', links[1]):
                links = self.cache_if_new(api_method=self.next_link(links[0]),
                                           parameters={'key': api_key()})
            else:
                link = self.next_link(links[0])
                next_link = self.querry_table('meta_data', 'rel_links',
                                              'url',  link)
                links = (next_link[0], link)

    def get_item(self, api_method, parameters):
        n = 0
        response = requests.get(api_method, parameters)
        self.api_cooldown(response.headers)
        while (response.status_code == 400) and (n != 100):
            response = requests.get(api_method, parameters)
            self.api_cooldown(response.headers)
            n += 1
        return response

    def api_cooldown(self, header):
        if ('X-RateLimit-Remaining' in header and
            header['X-RateLimit-Remaining']) == '0':
            sleep(float(header['X-RateLimit-Reset']))
        else:
            sleep(0.5) #to compensate for when X-ratelimit isn't given

    def get_groups(self, params):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/find/groups/
        self.get_items('find/groups', params)

    def get_events(self, params, urlname):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/:urlname/events/
        self.get_items(urlname + '/events', params)
