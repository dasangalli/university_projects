import csv
import datetime
import time
import requests
import json
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from kafka import KafkaConsumer,KafkaProducer
import sys

HERE_APP_ID="B93QbhRRNtRuEoD24lKT"
HERE_CODE="4iQZzY41qxJ0la1nTs6HAg"

file_date=datetime.datetime.now()
day_string=file_date.day

def setup_kafka(topic_name):
    producer=KafkaProducer(bootstrap_servers="localhost:9092",api_version=(0, 10, 1))
    consumer=KafkaConsumer(bootstrap_servers="localhost:9092",api_version=(0, 10, 1),
                        auto_offset_reset="latest",consumer_timeout_ms=1000)
    consumer.subscribe(topic_name)
    return producer,consumer,topic_name

def get_coordinates_origin(origin):
    try:
        geolocator = Nominatim(user_agent="real_time_traffic_app")
        origin_coord = geolocator.geocode(origin,timeout=100)
        return origin_coord.latitude,origin_coord.longitude
    except GeocoderTimedOut as e:
        print("Error: Geocode TimedOut: retrying...")
        get_coordinates_origin(origin)

def get_coordinates_destination(destination):
    try:
        geolocator = Nominatim(user_agent="real_time_traffic_app")
        destination_coord = geolocator.geocode(destination,timeout=100)
        return destination_coord.latitude,destination_coord.longitude
    except GeocoderTimedOut as e:
        print("Error: Geocode TimedOut: retrying...")
        get_coordinates_destination(destination)



def parse_json(content):

    timestamp=content["response"]["metaInfo"]["timestamp"]
    first=timestamp.split("T")
    first_part=first[0]
    second=first[1].split("Z")
    second_part=second[0]
    time_stamp=first_part +" "+ second_part
    distance=content["response"]["route"][0]["summary"]["distance"]
    base_time=content["response"]["route"][0]["summary"]["baseTime"]
    traffic_time=content["response"]["route"][0]["summary"]["trafficTime"]

    return time_stamp,distance,base_time,traffic_time


def get_traffic_real_time(origin,destination):

    origin_lat,origin_long = get_coordinates_origin(origin)
    dest_lat,dest_long = get_coordinates_destination(destination)

    file_date_2=datetime.datetime.now()
    response=requests.get("https://route.api.here.com/routing/7.2/calculateroute.json?waypoint0={}%2C{}&waypoint1={}%2C{}&mode=shortest%3Bcar%3Btraffic%3Aenabled&app_id={}&app_code={}&departure=now".
                   format(origin_lat,origin_long,dest_lat,dest_long,HERE_APP_ID,HERE_CODE))

    if response.status_code==200:
        status="Connection Established"
    else:
        status="Connection Failed"

    test=response.json()
    timestamp,distance,base_time,traffic_time=parse_json(test)

    return status,timestamp,distance,base_time,traffic_time


def create_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)


def write_file(origin,destination,highway,content):
    file_date_2=datetime.datetime.now()

    directory_name="DM_project/{}".format(highway)

    create_directory(directory_name)

    if(str(file_date_2.day)==day_string):
        with open("{}/traffic_data_{}-{}-{}-{}-{}.csv".format(directory_name,origin,destination,
        file_date_2.day,file_date_2.month,file_date_2.year),'a+') as csv_file:
            writer = csv.writer(csv_file)
            if(os.stat(csv_file.name).st_size==0):
                writer.writerows([["TIMESTAMP","DISTANCE (in meters)","BASE TIME (in seconds)","TRAFFIC TIME (in seconds)"]])

            writer.writerows([[content]])
    else:
        with open("{}/traffic_data_{}-{}-{}-{}-{}.csv".format(directory_name,origin,destination,
        file_date_2.day,file_date_2.month,file_date_2.year),'a+') as csv_file:
            writer = csv.writer(csv_file)
            if(os.stat(csv_file.name).st_size==0):
                writer.writerows([["TIMESTAMP","DISTANCE (in meters)","BASE TIME (in seconds)","TRAFFIC TIME (in seconds)"]])

            writer.writerows([[content]])


def run_script(origin,destination,highway):
    producer,consumer,topic_name=setup_kafka(highway)
    while(True):
        send_list=[]
        status,timestamp,distance,base_time,traffic_time=get_traffic_real_time(origin,destination)
        if(status=="Connection Established"):
            print("Everything went fine :)")
            send_list.append(timestamp)
            send_list.append(distance)
            send_list.append(base_time)
            send_list.append(traffic_time)
            producer.send(highway,str.encode(str(send_list)))
        else:
            print("Something went wrong...please retry")
            break

        write_file(origin,destination,highway,response.value)

        time.sleep(300)

if __name__ == '__main__':
    if(len(sys.argv)==4):
        origin=sys.argv[1]
        destination=sys.argv[2]
        highway=sys.argv[3]
        run_script(origin,destination,highway)

        write_file(origin,destination,highway,send_list)
