# consume.py
import pika
import time
from envirophat import light, weather, leds

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
params = pika.URLParameters('amqp://bgwwribe:_nNVuHac4WlIMUqRlUr3nEN12K3paelX@wombat.rmq.cloudamqp.com/bgwwribe')
params.socket_timeout = 5
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

channel.queue_declare(queue='light_command', durable=True)

def callback(ch, method, properties, body):
  print(" [x] Received %r" % body)
  if(body == 'off'):
    leds.off()
  else:
    leds.on()

channel.basic_consume(callback,
                      queue='light_command',
                      no_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
