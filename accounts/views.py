from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from .form import UserRegistrationForm, LoginForm
from django.contrib import messages
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        # تنظیمات لاگین
        if user_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            #برسی درخواست فرم و احراز هویت
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect(reverse("account:login"))
            login(request, user)
            return redirect(reverse('blog:Home'))
    else:
        #برسی لاگین بودن کاربر
        if request.user.is_authenticated:
            return redirect('blog:Home')
        user_form = LoginForm()
    return render(request, 'registration/login.html', {'form': user_form})


def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            message = messages.success(request, 'ثبت نام شما با موفقیت انجام شد')
        return redirect('account:login')
    else:
        if request.user.is_authenticated:
            return redirect('blog:Home')
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})