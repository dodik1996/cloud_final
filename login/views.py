from django.shortcuts import render
from login.forms import PersonForm,RequestsForm
from login.models import Person,Requests
import pika
import json

def signup(request):
    if request.method == 'POST':  
 
		form = PersonForm(request.POST)
		username = request.POST.get('username', '')
		request.session['username'] = username
		password = request.POST.get('password', '')
		person_obj = Person(username=username,password=password)
		person_obj.save()
		form1=RequestsForm()
		init=Requests.objects.filter(person=username,status="init")
		process=Requests.objects.filter(person=username,status="process")
		final=Requests.objects.filter(person=username,status="final")
		return render(request, 'login/main.html', {'username': username,'form':form1,'init':init,'process':process,'final':final}) 
 
    else:
        form = PersonForm()  
 
        return render(request, 'login/signup.html', {'form': form})


def makerequest(request):
	form1=RequestsForm()
	username="deafault"
	if request.session.has_key('username'):
		username = request.session['username']
	init=Requests.objects.filter(person=username,status="init")
	process=Requests.objects.filter(person=username,status="process")
	final=Requests.objects.filter(person=username,status="final")
	if request.method == 'POST':  
		form = RequestsForm(request.POST) 
		title = request.POST.get('title', '')
		obj=json.dumps({"username": username, "title": title,"status":"undefined"})
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()
		channel.queue_declare(queue='queue1')

		channel.basic_publish(exchange='',routing_key='queue1',body=obj)
		connection.close()
		return render(request, 'login/main.html', {'username': username,'form':form1,'init':init,'process':process,'final':final})
	else:
		form = RequestsForm()  
 		
		return render(request, 'login/main.html', {'username': username,'form':form1,'init':init,'process':process,'final':final})
