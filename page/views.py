from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.utils.safestring import mark_safe




def home(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())

@csrf_exempt
def signup(request):
    if request.method =="POST":
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']


        myuser=User.objects.create_user(username=username,email=email,password=pass1)
        myuser.first_name=firstname
        myuser.last_name=lastname
        myuser.save()

        messages.success(request,"Your account has been successfully created")
        return redirect('signin')

    template=loader.get_template('signup.html')
    return HttpResponse(template.render())

@csrf_exempt
def auth_signin(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            fname=user.first_name
             
             #temp=loader.get_template('index.html')
            return render(request,"index.html",{'fname':fname})
            # return HttpResponse(temp.render(),{'fname':fname})
        else:
            messages.info(request,"No Such User SignedUp")
            return redirect('/')

@csrf_exempt
def signin(request):

    template=loader.get_template('signin.html')
    return HttpResponse(template.render())
def signout(request):
    pass
# Create your views here.
