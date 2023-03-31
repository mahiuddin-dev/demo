from django.shortcuts import redirect, render
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('product:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        check_username = User.objects.filter(username=username)

        if check_username:
            return render(request,'register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        # add the user to a group
        group_name = 'user'
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            pass
        user.groups.add(group)
        user.save()
        return redirect('account:login')
    else:
        return render(request,'register.html')


def loginView(request):
    if request.user.is_authenticated:
        return redirect('product:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        # return render(request,'login.html')
        if user is not None:
            login(request,user)
            return redirect('product:index')
        else:
            return render(request,'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request,'login.html')

@login_required
def logoutView(request):
    logout(request)
    return redirect('account:login')