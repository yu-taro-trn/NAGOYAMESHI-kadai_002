from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from base.forms.member_forms import MemberSignupForm
from base.models import MemberProfile

User = get_user_model()

@require_http_methods(["GET", "POST"])
def member_login(request): # ログイン
    if request.method == "GET":
        return render(request, "members/login.html")

    email = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(request, username=email, password=password)

    if user is None or user.is_staff:
        return render(request, "members/login.html", {"error": "メールアドレスまたはパスワードが違います。"})

    login(request, user)
    return redirect("home")


def member_logout(request): # ログアウト
    logout(request)
    return redirect("home")



@require_http_methods(["GET", "POST"])
def member_signup(request): # 会員登録
    if request.method == "GET":
        form = MemberSignupForm()
        return render(request, "members/signup.html", {"form": form})

    form = MemberSignupForm(request.POST)
    if not form.is_valid():
        return render(request, "members/signup.html", {"form": form})

    email = form.cleaned_data["email"]
    password = form.cleaned_data["password1"]

    with transaction.atomic():
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()

        MemberProfile.objects.create(
            user=user,
            full_name=form.cleaned_data["full_name"],
            full_name_kana=form.cleaned_data["full_name_kana"],
            birth_date=form.cleaned_data.get("birth_date"),
            gender=form.cleaned_data.get("gender") or MemberProfile.Gender.NONE,
            occupation=form.cleaned_data.get("occupation"),
            is_active=True,
        )

    login(request, user)
    return redirect("home")