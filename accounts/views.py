from django.shortcuts import render, get_object_or_404
from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import generic 
from accounts.models import UserProfileInfo
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q

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

def register(request, backend='django.contrib.auth.backends.ModelBackend'):
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
      login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return HttpResponseRedirect(reverse('accounts:index'))
    else:
      print(user_form.errors, profile_form.errors)
  else:
    user_form = UserForm()
    profile_form = UserProfileInfoForm()
  return render(request, 'accounts/sign-up.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_list(request):
  context = {}
  url_params = request.GET.get("q")
  if url_params:
    users = User.objects.filter(Q(username__icontains=url_params) | Q(email__icontains=url_params))
  else:
    users = User.objects.all()
  context["users"] = users
  
  if request.is_ajax():
    html = render_to_string(
      template_name="accounts/includes/users.html", 
      context={"users": users}
      )
    data_dict = {"html_from_view": html}
    return JsonResponse(data=data_dict, safe=False)   
  return render(request, 'accounts/user_list.html', {'users': users})

def user_detail(request, pk):
  user = User.objects.get(pk=pk)
  user_profile = user.profile
  return render(request, 'accounts/user_detail.html', {'user': user, 'user_profile': user_profile})

@login_required
def change_avatar(request, pk):
  user_profile = get_object_or_404(UserProfileInfo, pk=pk)
  user = user_profile.user
  if user == request.user:
    if request.method == 'POST':
      profile_form = UserProfileInfoForm(data=request.POST, instance=user_profile)
      if profile_form.is_valid():
        if 'profile_pic' in request.FILES:
          user_profile.profile_pic = request.FILES['profile_pic']
        user_profile.save()
        return render(request, 'accounts/user_detail.html', {'user': user, 'user_profile': user_profile})
    else:
      profile_form = UserProfileInfoForm()
    return render(request, 'accounts/change_avatar.html', {'profile_form': profile_form})
  else:
    return HttpResponse("invalid")

@login_required
def edit_profile(request, pk):
  user = get_object_or_404(User, pk=pk)
  user_profile = user.profile
  if(user == request.user):
    if request.method == 'POST':
      user_form = UserForm(data=request.POST, instance=request.user)
      if user_form.is_valid():
        user_form.save()
        user_profile.user = user 
        return render(request, 'accounts/user_detail.html', {'user': user, 'user_profile': user_profile})
    else:
      user_form = UserForm()
    return render(request, 'accounts/edit_profile.html', {'user_form': user_form})
  else:
    return HttpResponse("Invalid")

