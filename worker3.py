import time
import json
import pika
import psycopg2


class Request(object):
	def __init__(self, j):
		self.__dict__ = json.loads(j)
def add_to_db(body):
	try:
		conn = psycopg2.connect("dbname='help_desk' user='ak' host='localhost' password='1'")
	except:
		print "Cannot connect to db"
	cur = conn.cursor()
	try:
		cur.execute("UPDATE login_Requests SET status='final' WHERE person_id=(%s) AND status=(%s);",(Request(body).username,"process",))
		conn.commit()
	except:
		print("cannot insert")
		pass
	conn.close()
def executeSomething():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='queue3')

	def callback(ch, method, properties, body):
		add_to_db(body)

	channel.basic_consume(callback,queue='queue3',no_ack=True)
	channel.start_consuming()

while True:
    executeSomething()