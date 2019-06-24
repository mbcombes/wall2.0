from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def index(request):     # GET /
    return render(request, 'wall/index.html')

def create(request):    # POST /create
    # to check if there are errors.
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':    # if no errors were detected.
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user=User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        request.session['username']=new_user.first_name
        request.session['id']=new_user.id
        print("this is the submit path")
        print(new_user)
        return redirect('/show')

def login(request):    # POST /login
    # to check if there are errors.
    print(request.POST['email'])
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':    # if no errors were detected.
        user=User.objects.get(email=request.POST['email'])
        request.session['username']=user.first_name
        request.session['id']=user.id
    return redirect('/show')

def show(request):   # GET /show
    if 'id' in request.session:
        comments=[]
        messages=Message.objects.all().order_by('-id')
        comments=Comment.objects.all()
        context={
            "messages": messages,
            "comments": comments,
        }
        print("These are the comments")
        print(comments)
        return render(request, 'wall/show.html', context)
    else:
        messages.error(request, 'Please Log In.', extra_tags='fail')
        return redirect('/')

def destroy(request):
    del request.session['username']
    del request.session['id']
    print('session cleared')
    return redirect('/')

def message(request):
    if request.method == "POST":
        Message.objects.create(message=request.POST["message"], user=User.objects.get(id=request.session["id"]))
        return redirect('/show')

def comment(request):
    if request.method == "POST":
        Comment.objects.create(comment=request.POST["comment"], user=User.objects.get(id=request.session["id"]), message=Message.objects.get(id=request.POST["messageid"]))
        print('comment made!')
        return redirect('/show')

def delete(request):
    if request.method == 'POST':
        comment=Comment.objects.get(id=request.POST['commentid'])
        comment.delete()
    return redirect('/show')

def deletemessage(request):
    if request.method == 'POST':
        message=Message.objects.get(id=request.POST['messageid'])
        message.delete()
    return redirect('/show')
