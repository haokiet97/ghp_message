from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
  return render(request, 'accounts/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in!")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:index'))

def user_login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
      login(request, user)
      return HttpResponseRedirect(reverse('accounts:index'))
    else:
      return HttpResponse("Invalid")
  else:
    return render(request, 'accounts/login.html', {})

def register(request):
  registered = False
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(data=request.POST)
    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()
      profile = profile_form.save(commit=False)
      profile.user = user 
      if 'profile_pic' in request.FILES:
        print('found it')
        profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        registered = True 
      login(request, user)
      return HttpResponseRedirect(reverse('accounts:index'))
    else:
      print(user_form.errors, profile_form.errors)
  else:
    user_form = UserForm()
    profile_form = UserProfileInfoForm()
  return render(request, 'accounts/sign-up.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
