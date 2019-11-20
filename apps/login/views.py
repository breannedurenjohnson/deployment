from django.shortcuts import render, redirect
from .models import User, Quote
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'login/index.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1)
        last_user = User.objects.last()
        request.session['user_name'] = last_user.first_name
        request.session['user_id'] = last_user.id
    return redirect('/dashboard')

def login(request):
    errors = {}
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['user_name'] = logged_user.first_name
            return redirect('/dashboard')
        else: 
            errors['login_match'] = "Email and password do not match."
    else:
        errors['email_nonexist'] = "Email does not exist."
    for key, value in errors.items():
        messages.error(request, value)
        print(messages)
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_first_name =request.session['user_name']
    user_id = request.session['user_id']
    context = {
        "user_name": user_first_name,
        "user_id": user_id,
        "favorited_quotes": Quote.objects.filter(users_who_like = User.objects.get(id=request.session['user_id'])).order_by("-created_at"),
        "unfavorited_quotes": Quote.objects.exclude(users_who_like = User.objects.get(id=request.session['user_id'])).order_by("-created_at"),
    }
    return render(request, 'login/dashboard.html', context)

def profile(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=id)
    user_quotes = user.quotes.all()
    context = {
        "user": User.objects.get(id=id),
        "all_user_quotes": Quote.objects.all().order_by("-created_at"),
    }
    return render(request, 'login/profile.html', context)

def add_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        Quote.objects.create(quote=request.POST['quote'], author=request.POST['author'], user=User.objects.get(id=request.session['user_id']))
    return redirect('/dashboard')

def edit_quote(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_quote = Quote.objects.get(id=id)
    if this_quote.user.id != request.session['user_id']:
        return redirect('/dashboard')
    user_id = request.session['user_id']
    context = {
        "quote": Quote.objects.get(id=id)
    }
    return render(request, "login/edit_quote.html", context)

def update_quote(request, id):
    if request.method == "POST":
        this_quote = Quote.objects.get(id=id)
        if this_quote.user.id == request.session['user_id']:
            quote = Quote.objects.get(id=id)
            quote_id = quote.id
            errors = Quote.objects.quote_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/quotes/' + str(quote_id) + '/edit')
            else:
                quote = Quote.objects.get(id=id)
                quote.quote = request.POST['quote']
                quote.author = request.POST['author']
                quote.save()
    return redirect('/dashboard') 

def favorite_quote(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        this_quote = Quote.objects.get(id=id)
        this_user = User.objects.get(id=request.session['user_id'])
        this_quote.users_who_like.add(this_user)
    return redirect('/dashboard')

def remove_favorite(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        this_quote = Quote.objects.get(id=id)
        this_user = User.objects.get(id=request.session['user_id'])
        this_quote.users_who_like.remove(this_user)
    return redirect('/dashboard')

def delete_quote(request, id):
    if request.method == "POST":
        this_quote = Quote.objects.get(id=id)
        if this_quote.user.id == request.session['user_id']:
            this_quote.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')



