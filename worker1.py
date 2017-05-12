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

	channel1.queue_declare(queue='queue2')

	channel1.basic_publish(exchange='',routing_key='queue2',body=body)
	connection1.close()
def add_to_db(body):
	try:
		conn = psycopg2.connect("dbname='help_desk' user='ak' host='localhost' password='1'")
	except:
		print "Cannot connect to db"
	cur = conn.cursor()
	tup1 = (Request(body).username,Request(body).title,"init")
	try:
		cur.execute("INSERT INTO login_Requests (person_id, title, status) VALUES (%s, %s, %s);",(Request(body).username,Request(body).title,"init",))
		conn.commit()
	except:
		print("cannot insert")
		pass
	conn.close()
def executeSomething():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='queue1')

	def callback(ch, method, properties, body):
		add_to_db(body)
		time.sleep(5)
		add_to_queue(body)

	channel.basic_consume(callback,queue='queue1',no_ack=True)
	channel.start_consuming()

while True:
    executeSomething()