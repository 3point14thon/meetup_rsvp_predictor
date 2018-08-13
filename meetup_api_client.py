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

    def get_item(self, api_method, parameters):
        parameters['key'] = api_key()
        res = requests.get(self.meetup_url + api_method, parameters)
        if res.headers['X-RateLimit-Remaining'] == 0:
            sleep(float(res.headers['X-RateLimit-Reset']))
        return res

    def get_groups(self, params):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/2/groups/
        return self.get_item('find/groups', params)

    def get_events(self, params):
        #possible parameters are described here:
        #https://www.meetup.com/meetup_api/docs/2/events/
        return self.get_item('2/events', params)


    def find_past_events(self, location, start_date, end_date, table):
        '''
        inconsistant on how many 400 errors are returned, might depend on
        internet connection
        '''
        group_events_dict = {}
        location['only'] = 'lat,lon,urlname'
        content = self.get_groups(location)
        if content.status_code != requests.codes.ok:
            raise ValueError(str(response.status_code) +
                             ' response code from meetup when requesting groups')
        groups = content.json()['results']
        group_log = []
        for group in groups:
            group_name = group['urlname']
            params = {'time': '{},{}'.format(start_date, end_date),
                      'status': 'past',
                      'group_urlname': group_name,
                      'fields': '''event_hosts,
                                   membership_d...,
                                   series,
                                   group_approved,
                                   group_photo,
                                   photo_album_id,
                                   photo_count,
                                   rsvp_rules,
                                   survey_questions,
                                   timezone,
                                   comment_count'''}
            if not table.find_one({'urlname': group_name}):
                #consider putting a while not urlcode 200 here but be carful
                response = self.get_events(params)
                n = 0
                while response.status_code == 400 and n != 100:
                    response = self.get_events(params)
                    n += 1
                self.url_code_log.append(response.status_code)
                table.insert_one({'urlname': group_name,
                                  'data': response.json(),
                                  'urlcode': response.status_code})
        return group_events_dict
