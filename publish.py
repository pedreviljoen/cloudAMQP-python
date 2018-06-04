# publish.py
# python environment dependancies
import pika, os
import json
import time
import datetime
import uuid
from envirophat import light, weather, leds

count = 0
sleep_time = 30  # seconds

# declare method for taking measurements
def take_reading():
    # take reading of temp, pressure & lux
    temp_r = round(weather.temperature(),2)
    press_r = round(weather.pressure()/100,2)
    lux_r = round(light.light(),2)
    # build timestamp
    now = round(time.time()*1000)
    time_stamp = int(now)
    # generate random uuid
    UUID = str(uuid.uuid4())
    # build message object
    measurement_object = {
        'measurement': {
            'temperature': temp_r,
            'pressure': press_r,
            'lux': lux_r
            },
        'created_at': time_stamp,
        'updated_at': time_stamp,
        'id': UUID
        }
    # convert to string using json dump & return
    return json.dumps(measurement_object)

# main program
try:
    # establish connection to cloudAMQP
    url = 'amqp://bgwwribe:_nNVuHac4WlIMUqRlUr3nEN12K3paelX@wombat.rmq.cloudamqp.com/bgwwribe'
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='measurement', durable=True)
    # take readings and publish to queue
    while True:
        # take reading
        reading = take_reading()
        # publish message
        channel.basic_publish(exchange='',
                              routing_key='measurement',
                              body=reading)
        print("[publish] Sent message to cloudAMQP")
        print(reading)
        # sleep for n seconds
        time.sleep(sleep_time)
except KeyboardInterrupt:
    connection.close()
    exit()
    

