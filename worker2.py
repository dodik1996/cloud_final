import time
import json
import pika
import psycopg2


class Request(object):
	def __init__(self, j):
		self.__dict__ = json.loads(j)
def add_to_queue(body):
	connection1 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel1 = connection1.channel()

	channel1.queue_declare(queue='queue3')

	channel1.basic_publish(exchange='',routing_key='queue3',body=body)
	connection1.close()
def add_to_db(body):
	try:
		conn = psycopg2.connect("dbname='help_desk' user='ak' host='localhost' password='1'")
	except:
		print "Cannot connect to db"
	cur = conn.cursor()
	try:
		cur.execute("UPDATE login_Requests SET status='process' WHERE person_id=(%s) AND status=(%s);",(Request(body).username,"init",))
		conn.commit()
	except:
		print("cannot insert")
		pass
	conn.close()
def executeSomething():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='queue2')

	def callback(ch, method, properties, body):
		add_to_db(body)
		time.sleep(7)
		add_to_queue(body)

	channel.basic_consume(callback,queue='queue2',no_ack=True)
	channel.start_consuming()

while True:
    executeSomething()