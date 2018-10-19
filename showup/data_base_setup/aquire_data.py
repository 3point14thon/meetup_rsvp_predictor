def get_groups_in_area(mac, zip_code):
    params = {'fields': ','.join([
                      'join_info',
                      'past_event_count']),
              'country': 'US',
              'radius': 100,
              'zip': zip_code}
    mac.get_groups(params)

def find_past_events(mac, start_date, end_date):
    '''
    inconsistant on how many 400 errors are returned, might depend on
    internet connection
    '''
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
    mac.curs.execute('SELECT urlname FROM meetup_group;')
    groups = mac.curs.fetchall()
    for group in groups:
        group_name = group[0]
        mac.get_events(params, group_name)

def find_events_in_US():
    get_groups_in_area()
    find_past_events(mac, blah, blah)
