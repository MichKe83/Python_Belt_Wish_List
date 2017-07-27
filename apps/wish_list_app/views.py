from django.shortcuts import render, redirect, HttpResponse
from .models import User, Wish
from django.db.models import Count
from django.contrib import messages
import bcrypt
from datetime import datetime
  
def dashboard(request):
	if 'user_id' in request.session:
		user = currentUser(request)
		wishes = Wish.objects.all()
		my_wishes = user.items.all()
		wishes = Wish.objects.exclude(id__in=my_wishes)
	
		context = {
		"user": user,
		'wishes': wishes,
		'my_wishes': my_wishes,
		}

	return render(request, 'wish_list_app/dashboard.html', context)

def addItem(request):
# this is for a user to add a new item to the database

	if 'user_id' in request.session:
		user = currentUser(request)

		context = {
		"user": user,
		}

	return render(request, 'wish_list_app/addItem.html', context)

def submitItem(request):
	if request.method == 'POST':
		errors = Wish.objects.validateWish(request.POST)

		if not errors:
			user = currentUser(request)

			wish = Wish.objects.create(item=request.POST['item'], user=user)

			user.items.add(wish)

			return redirect('/dashboard')

		for error in errors:
			messages.error(request, error)

		
		
		return redirect('/addItem')

	return redirect('/dashboard')

def addWish(request, id):
# this is to add another user's item/wish to my wish list
	if 'user_id' in request.session:
		user = currentUser(request)

		wish = Wish.objects.get(id=id)

		wish.wishers.add(user)

		return redirect('/dashboard')

def removeWish(request, id):
# this is to remove another user's item/wish from my wish list
	if 'user_id' in request.session:
		user = currentUser(request)

		wish = Wish.objects.get(id=id)

		wish.wishers.remove(user)

		return	redirect('/dashboard')

def item(request, id):
	if 'user_id' in request.session:
		user = currentUser(request)
		

		context = {
		'user': user,
		'wish': Wish.objects.get(id=id)		
		}

	return render(request, 'wish_list_app/item.html', context)

def index(request):
  
	return render(request, 'wish_list_app/index.html')

def currentUser(request):		
	user = User.objects.get(id=request.session['user_id'])

	return user

def register(request):
	if request.method == 'POST':
		
		errors = User.objects.validateRegistration(request.POST)

		if not errors:
			user = User.objects.createUser(request.POST)

			request.session['user_id'] = user.id

			return redirect('/dashboard')

		for error in errors:
			messages.error(request, error)
		print errors

	return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.validateLogin(request.POST)

		if not errors:
			user = User.objects.filter(email = request.POST['email']).first()

			if user:
				password = str(request.POST['password'])
				user_password = str(user.password)

				hashed_pw = bcrypt.hashpw(password, user_password)

				if hashed_pw == user.password:
					request.session['user_id'] = user.id
					# request.session['first_name'] = first_name
					
					return redirect('/dashboard')

			errors.append('Invalid account information.')
		
		for error in errors:
			messages.error(request, error)

		return redirect('/')

		print request.session['user_id']

		print errors

def delete(request, id):
	wish = Wish.objects.get(id=id)
	wish.delete()

	return redirect('/dashboard')

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')

	return redirect('/')