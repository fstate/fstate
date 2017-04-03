from pymongo import MongoClient
from pymongo.database import DBRef
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from createdatabase.config import db_name
from mongoengine import connect

ctc = connect(db_name,host=os.environ['FSTATE_MONGODB_1_PORT_27017_TCP_ADDR'],  port=27017)
db = ctc.temp_db
new_physics = db.new_physics # Auxilary collection for new physics
