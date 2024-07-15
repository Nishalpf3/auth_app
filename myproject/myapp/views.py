from django.http import HttpResponseRedirect, response
from multiprocessing import context
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
from django.urls import reverse


@never_cache
def HomePage(request):
    if 'username' in request.session and 'username' in request.COOKIES:
        return render(request, 'home.html')
    return redirect('login')



def LoginPage(request):
    if 'username' in request.session:
        if 'username' in request.COOKIES:
            if request.session['username'] == request.COOKIES['username']:
                return redirect('home')


    if request.method == 'POST':
        response = redirect('home')
        usrname=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=usrname,password=pass1)
        if user is not None:
            response.set_cookie('username', usrname)
            request.session['username'] = usrname
            return response
        else:
            return render(request, 'login.html', {'error_msg': "Invalid Credentials!!!!"})
            return render(request, 'login.html')

    return render(request,'login.html')

def SignupPage(request):
    if request.method=='POST':
        usname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("please enter the same password on both fields")
        else:
            my_user=User.objects.create_user(usname,email,pass1)
            my_user.save()
            return redirect('login')


    return render(request,'signup.html')

def AdminPage(request):
    if 'username' in request.session:
        if 'username' in request.COOKIES:
            if request.session['username'] == request.COOKIES['username']:
                return redirect('admin_home')

    if request.method == 'POST':
        response = redirect('admin_home')
        usrname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=usrname, password=pass1)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_home')
            else:
                return redirect('admin_login')
        else:
            messages.info(request, 'username Or Password is Incorrect!')
            return redirect('admin_login')

    return render(request, 'admin_login.html')

@login_required(login_url='admin_login')
def admin_home(request):
    if request.user.is_superuser:
        context = {'user_details': User.objects.all()}  # show user details
        return render(request, 'admin_home.html', context)  # show list
    else:
        return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def LogoutPage(request):
    response = HttpResponseRedirect(reverse('login'))
    request.session.flush()
    response.delete_cookie('username')
    return HttpResponseRedirect(reverse('login'))



def users(request):
    if request.user.is_superuser:
        context={'user_details':User.objects.all()}
        return render(request,'admin_home.html',context)
    else:
        return redirect('admin_login')
def user_insert(request,id=0):
    if request.user.is_superuser:
        if request.method=="GET":
            if(id==0):
                form=CreateUserForm()
            else:
                u=User.objects.get(pk=id)
                form=CreateUserForm(instance=u)
            return render(request,'signup.html',{'form':form})
        else:
            if id==0:
                form=CreateUserForm(request.POST)
            else:
                u=User.objects.get(pk=id)
                form=CreateUserForm(request.POST,instance=u)
            response=redirect('users')
            if form.is_valid():
                form.save()
            return response
    else:
        return redirect('admin_login')
def user_delete(request,id):
    if request.user.is_superuser:
        u=User.objects.get(pk=id)
        u.delete()
        return redirect('users')
    else:
        return redirect('admin_login')
def search(request):
    if request.user.is_superuser:
        query=request.GET['query']
        user_details=User.objects.filter(username__icontains=query)
        context={'user_details':user_details}
        return render(request,'search.html',context)
    else:
        return redirect('admin_login')