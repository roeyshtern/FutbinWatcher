import random
import requests
import time
from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer, Date, Binary
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os
db_string = "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_string_lite = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

db = create_engine(db_string_lite)  
base = declarative_base()

Session = sessionmaker(db)  
session = Session()

class PlayersMonitor(base):
    __tablename__ = 'PlayersMonitor'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    min_price = Column(Integer)
    max_price = Column(Integer)
    current_price = Column(Integer)
    date_created = Column(Date)
    last_updated = Column(Date)
    last_alerted_time_min = Column(Date)
    last_alerted_price_min = Column(Integer)
    last_alerted_time_max = Column(Date)
    last_alerted_price_max = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

class User(base):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)
    ifttt_code = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)



def get_price_by_id(player_id: int) -> int:
    return random.randint(0, 15)


def send_alert(ifttt_code: str, player_name: str, player: PlayersMonitor, alert_type: str):
    alerted_price = 0
    if alert_type == "min":
        alerted_price = player.min_price
    else:
        alerted_price = player.max_price
    response = requests.post(f"https://maker.ifttt.com/trigger/Test/with/key/{ifttt_code}", data={"value1":player_name, "value2":player.current_price, "value3":alerted_price})


def main():
    while(True):
        time.sleep(5)
        players = session.query(PlayersMonitor)
        for player in players:
            price = get_price_by_id(player.player_id)
            player.current_price = price
            session.commit()
            print(str(price) + "-" + str(player.player_id))
            if(price < player.min_price):
                send_alert("ceKpjTpqxGUTviB3mDnnkL", str(player.player_id), player, "min")
                    

main()

