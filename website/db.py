from pymongo import MongoClient

def get_db():
    client=MongoClient("mongodb+srv://Ncet_ApplicationForm_Payments:Ncet_ApplicationForm(Payments)@cluster0.bok10.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db=client["Ncet_ApplicationForm(Payments)"] #db name
    return db

db=get_db()
# collections
users_collection=db["users"]#users name of collection
temp_users_collection=db["temp_users"]
page1_collection=db["page1_collection"]
page2_collection = db["page2_collection"] 
page3_collection=db["page3_collection"]

counters_collection=db['counters']
def initialize_app_number_counter():
    if not counters_collection.find_one({"_id":"application_number"}):
        counters_collection.insert_one({"_id":"application_number","sequence_value":0})
initialize_app_number_counter()
