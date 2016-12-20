from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
# from . import models
from .models import User

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

	return render(request, 'myapp/success.html')

def logout(request)	:
	del request.session['id']
	return redirect ('/')


	# -------login/registration--------

# Create your views here.
