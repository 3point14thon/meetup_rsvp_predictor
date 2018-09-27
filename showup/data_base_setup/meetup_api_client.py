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
        self.current_res = None
        self.prev_res = None
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

    def cache_if_new(self, table, id_, api_method, parameters):
        find_id = 'SELECT url FROM meta_data;'
        if not cur.execute(find_id):
            res = self.get_item(api_method, parameters)
            if res.status_code != 404:
                if api_method=='find/groups':
                    insert_meta(res)
                    insert_group(res)
                else:
                    insert_meta(res)
                    insert_event()
                self.api_cooldown(res.headers)
            return res.headers
        else:
            return table.find_one({'url': id_})['header']

    def insert_meta(self, res, cur, conn):
        values = (res.url, res.headers['link'],
                  res.status_code, res.headers['date'])
        cols = '(url, rel_links, url_code, req_date)'
        self.insert_values(cols, values)

    def insert_group(self, group, meta_data_url):
        group_id = self.cur.execute('SELECT id FROM meetup_group;')
        if not group_id or group['id'] not in group_id:
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
                self.insert_question()
                self.insert_values('group_questions', (group['id'], question['id']))
        if 'topics' in group:
            for topic in group['topics']:
                self.insert_topic(topic)
                self.insert_values('group_topics', (group['id'], topic['id']))
        return values

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

    def insert_pronet(self, net):
        self.cur.execute(f"SELECT urlname FROM pro_network WHERE urlname='{net['urlname']}';")
        net_urlname = self.cur.fetchone()
        if not net_urlname or net['urlname'] not in net_urlname:
            cols = ('name',
                    'urlname',
                    'number_of_groups',
                    'network_url')
            values = self.find_values(net, cols)
            self.insert_values('pro_network', values, cols)

    def insert_topic(self, topic):
        topic_ids = self.cur.execute('SELECT id FROM topic;')
        if not topic_ids or topic['id'] not in topic_ids:
            cols = ('id',
                    'name',
                    'urlkey',
                    'lang')
            values = self.find_values(topic, cols)
            self.insert_values('topic', values, cols)

    def insert_category(self, category):
        category_ids = self.cur.execute('SELECT id FROM category;')
        if not category_ids or category['id'] not in category_ids:
            cols = ('id',
                    'name',
                    'shortname',
                    'sortname')
            values = self.find_values(category, cols)
            self.insert_values('category', values, cols)

    def insert_photo(self, photo):
        photo_ids = self.cur.execute('SELECT id FROM photo;')
        if not photo_ids or photo['id'] not in photo_ids:
            cols = ('id',
                    'base_url',
                    'highres_link',
                    'photo_link',
                    'thumb_link',
                    'type')
            values = self.find_values(photo, cols)
            self.insert_values('photo', values, cols)

    def insert_question(self, question):
        question_ids = self.cur.execute('SELECT id FROM questions;')
        if not question_ids or ['id'] not in question_ids:
            cols = ('id',
                    'question')
            values = self.find_values(questions, cols)
            self.insert_values('questions', values, cols)

    def partition_link(self, header):
        return header['Link'].partition(',')[0].partition(';')

    def has_next(self, header):
        return self.partition_link(header)[2] == ' rel="next"'

    def next_link(self, header):
        return self.partition_link(header)[0].strip('<>')

    def get_items(self, api_method, parameters, table):
        id_ = self.make_group_key(api_method, parameters)
        api_method = self.meetup_url + api_method
        parameters['key'] = api_key()
        header = self.cache_if_new(table, id_, api_method, parameters)
        while 'Link' in header and self.has_next(header):
            self.prev_res = header
            header = self.cache_if_new(table=table, id_=self.next_link(header),
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

    def get_groups(self, params, table):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/find/groups/
        self.get_items('find/groups', params, table)

    def get_events(self, params, table, urlname):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/:urlname/events/
        self.get_items(urlname + '/events', params, table)


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
                self.get_events(params, event_table, group_name)
