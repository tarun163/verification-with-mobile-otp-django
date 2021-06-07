from django.shortcuts import render,HttpResponse,redirect
from .models import Profile
from django.contrib.auth.models import User
import http.client
import random
from django.conf import settings

# Create your views here.
def home(request):
    return render(request,'index.html')

def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        verify = Profile.objects.filter(mobile = mobile).first()
        if not verify:
            context = {
                'success':True,
                'messege':'user is not found ',
                'class':'alert-danger'
            }
            return render(request,'login.html',context)
        otp = str(random.randint(1000,9999))
        verify.otp = otp
        verify.save()
        send_otp(mobile,otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')
    return render(request,'login.html')

def login_otp(request):
    mobile = request.session['mobile']

    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        verify = Profile.objects.filter(otp = otp ).first()
        
        print(Profile.mobile)
        if verify:
            context = {
                'success':True,
                'messege':'Welcome',
                'class':'alert-success'
            }
            return render(request,'index.html',context)         

    return render(request,'otp.html',context)  

def register(request):
   
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        q = Profile.objects.filter(mobile = mobile).first()
        if not q:
            user = User(username = username,email=email)
            user.save()
            otp = str(random.randint(1000,9999))
            profile = Profile(user = user,mobile=mobile,otp=otp)
            profile.save()
            send_otp(mobile,otp)
            request.session['mobile'] = mobile
           
            return redirect('otp')
        else:
            context = {
                'success':True,
                'messege':'user is already exist',
                'class':'alert-danger'
            }
            return render(request,'register.html',context)        
                
    return render(request,'register.html')        

def otp(request):
    mobile = request.session['mobile']

    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        verify = Profile.objects.filter(otp = otp, mobile=mobile ).first()
        print(verify.user)
        
        print(Profile.mobile)
        if verify:
            context = {
                'success':True,
                'messege':'Welcome',
                'class':'alert-success',
                'user':verify.user
            }
            return render(request,'index.html',context)         

    return render(request,'otp.html',context)  

def send_otp(mobile,otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY 
    headers = { 'content-type': "application/json" }
    url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message"+"rambabu%20otp%20is%20"+otp+"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None