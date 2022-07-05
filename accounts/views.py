from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from .form import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Profile
from django.views.generic.edit import CreateView


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        # تنظیمات لاگین
        if user_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            # برسی درخواست فرم و احراز هویت
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, 'نام کاربری یا رمز عبور صحیح نمیباشد')
                return redirect(reverse("account:login"))
            login(request, user)
            return redirect(reverse('blog:Home'))
    else:
        # برسی لاگین بودن کاربر
        if request.user.is_authenticated:
            return redirect('blog:Home')
        user_form = LoginForm()
    return render(request, 'registration/login.html', {'form': user_form})


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:login')
    form_class = UserRegistrationForm
    success_message = "ثبت نام با موفقیت انجام شد"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:Home')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


def profile_user(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    else:
        if request.method == 'POST':
            return redirect('blog:Home')
        else:
            return render(request, 'registration/profile.html')


def edit_profile(request):
    return render(request, 'registration/edit_profile.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8080',
                        'site_name': 'Iran Django',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'لینک بازیابی رمز عبور با موفقیت به ایمیل شما ارسال شد')
                    return redirect("account:login")
            messages.error(request, 'ایمیل وارد شده نامعتبر است')
    else:
        password_reset_form = PasswordResetForm()
        context = {
            'form': password_reset_form
        }
        return render(request, "registration/password_reset_form.html", context)
