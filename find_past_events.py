import requests
import numpy as np
from meetup_api_client import MeetupApiClient

def find_past_events(location, start_date, end_date):
    '''
    inconsistant on how many 400 errors are returned
    '''
    group_events_dict = {}
    mac = MeetupApiClient()
    content = mac.get_groups(location)
    if content.status_code != requests.codes.ok:
        raise ValueError(str(response.status_code) +
                         ' response code from meetup when requesting groups')
    groups = content.json()['results']
    err_log = np.zeros(len(groups))
    group_log = []
    for i, group in enumerate(groups):
        if group['visibility'] != 'public':
            continue
        group_name = group['urlname']
        params = {'time': '{},{}'.format(start_date, end_date),
                  'status': 'past',
                  'group_urlname': group_name}
        response = mac.get_events(params)
        err_log[i] = response.status_code
        if response.status_code == 400:
            group_log.append(group)
        #group_events_dict[group_name] = response.json()
    return err_log, group_log
