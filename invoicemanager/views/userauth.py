from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout



# User login
def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if (user is not None):
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			context = {
				'error_message' : 'Unable to login! Please check username and password then try again.',
				}
			return render(request, 'login.html', context)
	else:
		return render(request, 'login.html')



# User logout
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
