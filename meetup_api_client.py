import requests
from time import sleep
from api_key import api_key
import pymongo

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
        self.url_code_log = []

    def get_items(self, api_method, parameters, table):
        api_method = self.meetup_url + api_method
        parameters['key'] = api_key()
        if not table.find_one({'url': api_method}):
            res = self.get_item(api_method, parameters)
            header = res.headers
            table.insert_one({'url': api_method,
                              'header': res.headers,
                              'data': res.json(),
                              'urlcode': res.status_code})
        else:
            header = table.find_one({'url': api_method})['header']
        while ('Link' in header and
               header['Link'].partition(',')[0].partition(';')[2] == ' rel="next"'):
            next = header['Link'].partition(';')[0].strip('<>')
            if not table.find_one({'url': next}):
                res = self.get_item(next, {'key': api_key()})
                header = res.headers
                table.insert_one({'url': next,
                                  'header': res.headers,
                                  'data': res.json(),
                                  'urlcode': res.status_code})
            else:
                header = table.find_one({'url': next})['header']

    def get_item(self, api_method, parameters):
        n = 0
        response = self.stage(api_method, parameters)
        while (response.status_code == 400) and (n != 100):
            response = self.stage(api_method, parameters)
            n += 1
        return response

    def stage(self, api_method, parameters):
        res = requests.get(api_method, parameters)
        if (res.headers['X-RateLimit-Remaining']) == '0':
            sleep(float(res.headers['X-RateLimit-Reset']))
        return res

    def get_groups(self, params, table):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/2/groups/
        return self.get_items('find/groups', params, table)

    def get_events(self, params, table, urlname):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/2/events/
        return self.get_items(urlname + '/events', params, table)


    def find_past_events(self, start_date, end_date, group_table, event_table):
        '''
        inconsistant on how many 400 errors are returned, might depend on
        internet connection
        '''
        super_groups = group_table.find()
        for groups in super_groups:
            for group in groups['data']:
                group_name = group['urlname']
                params = {'fields': '''description_images,
                                       event_hosts,
                                       featured,
                                       featured_photo,
                                       fee_options,
                                       group_category,
                                       group_join_info,
                                       group_key_photo,
                                       group_membership_dues,
                                       meta_category,
                                       best_topics,
                                       group_past_event_count,
                                       group_photo,
                                       group_pro_network,
                                       group_topics,
                                       group_join_info,
                                       how_to_find_us,
                                       group_visibility,
                                       plain_text_no_images_description,
                                       rsvp_rules,
                                       series,
                                       answers
                                       ''',
                          'no_earlier_than': start_date,
                          'no_later_than': end_date,
                          'status': 'past'}
                self.get_events(params, event_table, group_name)
