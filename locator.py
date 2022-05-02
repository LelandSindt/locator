#!/usr/bin/python3

import os
import json
import traceback
import time
from datetime import datetime
from locationsharinglib import Service
from Adafruit_IO import Client, Feed, RequestError

#import logging
#logging.basicConfig(level=logging.DEBUG)

cookies_file = os.environ['COOKIES_FILE'] 
google_email = os.environ['GMAIL_EMAIL'] 

ADAFRUIT_IO_KEY = os.environ['ADAFRUIT_IO_KEY'] 
ADAFRUIT_IO_USERNAME = os.environ['ADAFRUIT_IO_USERNAME'] 

personFeed = os.environ['PERSON_FEED'] 

loop_delay = int(os.getenv('LOOP_DELAY', default = '900'))

dateTimeFormat = '%Y-%m-%dT%H:%M:%SZ'


service = Service(cookies_file=cookies_file, authenticating_account=google_email)
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try:
  location = aio.feeds(personFeed)
except RequestError: # Doesn't exist, create a new feed
  feed = Feed(name=personFeed)
  location = aio.create_feed(feed)

try:
  lastDateTime = aio.receive(location.key).created_at
  print('Using last date from adafruit io', lastDateTime)
except:
  lastDateTime = datetime.now().strftime(dateTimeFormat)
  print('Using using current date ', lastDateTime)



while True:
  try:
    person = service.get_person_by_nickname(personFeed)
    if lastDateTime == person.datetime.strftime(dateTimeFormat):
      print('already have record for', person.datetime.strftime(dateTimeFormat))
    else:
      lastDateTime = person.datetime.strftime(dateTimeFormat)
      metadata = { 'lat':person.latitude, 'lon':person.longitude, 'ele': 0, 'created_at':person.datetime.strftime(dateTimeFormat)}
      print('battery:', person.battery_level, 'location:', metadata)
      values = {'battery_level':person.battery_level, 'accuracy':person.accuracy, 'address': person.address, 'charging':person.charging,'country_code':person.country_code }
      aio.send_data(location.key,json.dumps(values),metadata)
  except:
    traceback.print_exc()
  time.sleep(loop_delay)
