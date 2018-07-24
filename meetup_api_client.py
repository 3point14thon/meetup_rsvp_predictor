import requests
from api_key import api_key

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
    '''
    def __init__(self):
        self.meetup_url = 'https://api.meetup.com/'
        self.url_code_log = []

    def get_item(self, api_method, parameters):
        parameters['key'] = api_key()
        return requests.get(self.meetup_url + api_method, parameters)

    def get_groups(self, params):
        return self.get_item('2/groups', params)

    def get_events(self, params):
        return self.get_item('2/events', params)

    def find_past_events(self, location, start_date, end_date):
        '''
        inconsistant on how many 400 errors are returned, might depend on
        internet connection
        '''
        group_events_dict = {}
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
                      'group_urlname': group_name}
            response = self.get_events(params)
            self.url_code_log.append(response.status_code)
            group_events_dict[group_name] = response.json()
        return group_events_dict
