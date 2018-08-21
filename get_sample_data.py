from pymongo import MongoClient

def get_data_from_mongo():
    mc = MongoClient()
    db = mc['meetups']
    ed = db['events_data']
    num_events = ed.estimated_document_count()
    data = []
    count = 0
    for event in ed.find():
        if count in 
