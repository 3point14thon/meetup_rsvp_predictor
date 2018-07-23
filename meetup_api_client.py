import requests
from api_key import api_key

class MeetupApiClient:

    def __init__(self):
        self.meetup_url = 'https://api.meetup.com/'

    def get_item(self, api_method, parameters):
        parameters['key'] = api_key()
        return requests.get(self.meetup_url + api_method, parameters)

    def get_groups(self, params):
        return self.get_item('2/groups', params)

    def get_events(self, params):
        return self.get_item('2/events', params)
