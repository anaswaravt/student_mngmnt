from django.shortcuts import render,redirect
from .models import Contact,Staff,Course
from django.contrib import messages




# Create your views here.
def index(request):
    return render(request,'index.html')
def mainhome(request):
    return render(request,'mainhome.html')

def contact(request):
    
    if request.method == 'POST':
   
        if request.POST['name'] is not None:
         
            enq=Contact.objects.create(name=request.POST['name'],email=request.POST['email'],phno=request.POST['phno'])
            enq.save()
            # print(enq)
            dicts={'out':1,'name':request.POST['name']}
            # print(dicts)
            return render(request,'contact.html',dicts)
    return render(request,'contact.html')


def course(request):
    courses={
        'course':Course.objects.all()
        }
    return render(request,'course.html',courses)

def gallery(request):
    return render(request,'gallery.html')


def logout(request):
    request.session.pop('email',None)
    request.session.pop('name',None)
    request.session.pop('phno',None)

    return render(request,'index.html')

def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        try:
            check_user=Staff.objects.get(email=email,password=password)
            request.session['email']=check_user.email
            request.session['name']=check_user.name
            request.session['phno']=check_user.phno
            return redirect('home')
        except Staff.DoesNotExist:
            messages.error(request,'invalid username and password')
            return redirect('login')
    return render(request,'index.html')
    
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phno = request.POST['phno']
        password2 = request.POST['password2']
        if password == password2 :
            if Staff.objects.filter(email = email).exists():
                messages.info(request,'email taken')
                return redirect ('signup')
            else:
                customer =  Staff.objects.create(email = email,name = name,password = password,phno = phno)
                customer.save()
                messages.info(request,'user created')
                return redirect('login')
        else:
            messages.info(request,'password is not match')
            return  redirect('signup')
    else:
        return render(request,'signup.html')


def forgot(request):
    if request.method == "POST":
        email = request.POST['email']
        password=request.POST['pass1']
        if Staff.objects.filter(email=email).exists():
            Staff.objects.filter(email=email).update(password=password)
            return redirect('login')
        else:
            messages.error(request,'invalid email id')
            return redirect('forgot')
    return render(request,'forgot.html')
