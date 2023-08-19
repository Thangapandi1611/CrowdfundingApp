from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.utils.safestring import mark_safe
from Crowd import settings
from django.core.mail import send_mail

#home page
def home(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())

@csrf_exempt
def signup(request):
    #storing in default db-User
    if request.method =="POST":
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"User Already Exists ! Try Someother username")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request,"Email Id Already Exists ! Try Someother Email Id")
            return redirect('home')
        if pass1!=pass2:
            messages.error(request,"Password doesn't match")
            return redirect('home')
            
        #Saving info in db and rendering to signin

        myuser=User.objects.create_user(username=username,email=email,password=pass1)
        myuser.first_name=firstname
        myuser.last_name=lastname
        myuser.save()

        messages.success(request,"Your account has been successfully created")
        
    
        #WELCOME EMAIL
        sub="WELCOME TO CROUWDFUNDING PLATFORM"
        msg="Hello"+myuser.first_name+"Your Account has been created successfully"+"\n Welocome to our platform "+"Please Check the Verification Mail sent to you "+"/n/n/n Thank You /n Thangapandi.V"
        from_email=settings.EMAIL_HOST_USER
        to_email=[myuser.email]
        send_mail(sub,msg,from_email,to_email,fail_silently=True)


        
        return redirect('signin')


    template=loader.get_template('signup.html')
    return HttpResponse(template.render())

@csrf_exempt
#Signin page rendering via home page 
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
#Signin page rendering via sign up
def signin(request):

    template=loader.get_template('signin.html')
    return HttpResponse(template.render())
def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')
# Create your views here.
