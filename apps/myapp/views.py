from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
# from . import models
from .models import User, Trip

def index(request):
	return render(request, 'myapp/index.html')

def register_process(request):

	if request.method == "POST":
		result = User.objects.register(request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['password'], request.POST['confirm_password'])

		if result[0]==True:
			request.session['id'] = result[1].id
			print result, "***************"
			# request.session.pop('errors')
			return redirect('/success')
		else:

			# request.session['errors'] = result[1]
			messages.add_message(request, messages.WARNING, result[1][0])

			print result[1], "***************"
			return redirect('/')
	else:

		return redirect ('/')

def login_process(request):
	result = User.objects.login(request.POST['email'],request.POST['password'])

	if result[0] == True:
		request.session['id'] = result[1][0].id
		return redirect('/success')
	else:
		messages.add_message(request, messages.WARNING, result[1][0])
		return redirect('/')

def users(request, id):
	if not 'id' in request.session :
		return redirect('/')
	else:
		session = request.session['id']
		loggedInUser = User.objects.filter(id=session)
		user = User.objects.filter(id=session)
		userName = user[0].first_name

		allQuotes = Quote.objects.filter(user__id=id).order_by('-created_at')
		quoteCount = allQuotes.count()

		data = {
			'allQuotes': allQuotes,
			'userName': userName,
			'quoteCount': quoteCount,
			'loggedInUser': loggedInUser[0].first_name,
			'quotePosterUserName': allQuotes[0].user.first_name,
			'sessionID': session
		}

	return render(request, "myapp/users.html", data)

def success(request):

	if not 'id' in request.session :
		return redirect('/')
	else:
		session = request.session['id']

		loggedInUser = User.objects.filter(id=session)

		schedule=Trip.objects.filter(participant_id=session)
		all_trips=Trip.objects.all().exclude(participant_id=session)

		context = {

		'loggedInUser' : loggedInUser[0],
		'schedule' : schedule,
		'all_trips' : all_trips,

		}

		return render(request, 'myapp/success.html', context)


def new_trip(request):
	if not 'id' in request.session :
		return redirect('/')
	else:
		session = request.session['id']

		return render(request, 'myapp/new_trip.html')

def add_trip(request):
	if request.method == "POST":
		session = request.session['id']
		Trip.objects.add_trip(request.POST, session)

		return redirect('/success')


def destination(request, id):
	if not 'id' in request.session :
		return redirect('/')
	else:
		session = request.session['id']

		destination=Trip.objects.filter(id=id)

		context= {

		'destination' : destination[0]

		}

		print destination[0].start_date

		return render(request, 'myapp/destination.html', context)

def join_trip(request, id):

	session = request.session['id']
	Trip.objects.join_trip(session, id)


	return redirect('/success')


def logout(request)	:
	del request.session['id']
	return redirect ('/')







