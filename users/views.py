from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # sửa 'home' nếu bạn muốn chuyển hướng khác
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
    return render(request, 'users/login.html')  # tạo template này nếu chưa có

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    return render(request, 'users/profile.html')  # đảm bảo template này tồn tại

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # hoặc redirect('home') nếu bạn có
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})