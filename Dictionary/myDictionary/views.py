from django.shortcuts import render,redirect
from django.contrib import messages
from myDictionary.models import User,History
from django.contrib.auth.models import User as InUser
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
ERROR = 40
SUCCESS = 25

def loginUser(request):
    return render(request,'index.html')

@login_required(login_url='/loginUser')
def history(request):
    if (request.user.is_anonymous):
        return redirect('loginUser')
    res=History.objects.filter(uname=request.user)
    context={
        "words" :[]
    }
    for i in res:
        context["words"].append(i.word)
    return  render(request,'history.html',context)

@login_required(login_url='/loginUser')
def searchHistory(request):
    if (request.user.is_anonymous):
        return redirect('loginUser')
    return redirect("/history")

@login_required(login_url='/loginUser')
def searchHome(request):
    if (request.user.is_anonymous):
        return redirect('loginUser')
    return redirect("/home")

@login_required(login_url='/loginUser')
def searchLogout(request):
    if (request.user.is_anonymous):
        return redirect('loginUser')
    return redirect("/logout")

@login_required(login_url='/loginUser')
def home(request):
    if(request.user.is_anonymous):
        return redirect('/loginUser')
    else:
        return render(request,'home.html')

@login_required(login_url='/loginUser')
def logoutUser(request):
    logout(request)
    messages.add_message(request, level=SUCCESS, message="Successfully Logged out!!")
    return redirect('/loginUser')


def validate(request):
    if(request.method=="POST"):
        level=SUCCESS
        msg='SUCCESS !!Account Created'
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        u1=User.objects.filter(uname=uname)
        if(uname=="Pranay" or len(u1)!=0 or len(password)<5 or len(phone)!=10 or len(name)<2 or password!=cpassword):
            level=ERROR
            msg='ERROR Occured!!'
            if(uname=="Pranay" or len(u1)!=0):
                msg+=" UserName already exists!"
            if(len(password)<5):
                msg+=" password should be >=5 character!"
            if(len(phone)!=10):
                msg+=" Invalid phone no.!"
            if(password!=cpassword):
                msg+=" Password don't match!"
            if(len(name)<2):
                msg+=" Name should be atleast 2 characters!"
        else:
            inuser=InUser.objects.create_user(username=uname,password=password)
            user = User(name=name,uname=uname,email=email,phone=phone,password=password,date=datetime.today())
            user.save()
            inuser.save()
        messages.add_message(request, level=level, message=msg)
        return redirect('loginUser')
    else:
        return redirect('loginUser')


def userverification(request):
    uname=request.POST['uname1']
    password=request.POST['password1']
    currUser= authenticate(request, username=uname, password=password)
    print(uname,password,currUser)
    if currUser is not None:
        login(request, currUser)
        return redirect('home')
    else:
        messages.add_message(request,level=ERROR,message='No Such User!')
        return redirect('loginUser')

w=""
@login_required(login_url='/loginUser')
def historySrc(request):
    if (request.user.is_anonymous):
        return redirect('loginUser')
    global w
    w = request.GET.get("data")
    res=redirect('/search/')
    return res

@login_required(login_url='/loginUser')
def search(request):
    if (request.user.is_anonymous):
        return redirect('loginUser')
    word=w
    # if (request.method == "GET"):
    #     word = request.GET.get("data")
    if(request.method=="POST"):
        word = request.POST.get("search")
        his=History(uname=request.user,word=word)
        his.save()
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term": word}
    headers = {
        'x-rapidapi-key': "28ffafc8ddmsh5a0aec3a058dae6p1ce13djsnde38c235885b",
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }
    data = requests.request("GET", url, headers=headers, params=querystring)
    data = data.json()
    if(len(data)==0):
        return redirect('home')
    context={
        'definition':[],
        'example':[],
        'word':word,
        'data':True
    }
    for i in data['list']:
        context['definition'].append(i['definition'])
        context['example'].append(i['example'])
    return render(request,'home.html',context)
