from django.shortcuts import redirect, render
from base.forms.account_forms import AccountEmailForm
from base.models import MemberProfile, Reservation, Review
from django.contrib.auth.decorators import login_required
from base.forms.member_edit_forms import MemberProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


@login_required(login_url="member_login")
def mypage(request):

  if request.user.is_staff:
    return render(request, 'members/mypage_forbidden.html', status=403)
  
  profile = MemberProfile.objects.filter(user=request.user).select_related("occupation").first()

  reservations = (
        Reservation.objects
        .filter(user=request.user)
        .select_related("store")
        .order_by("-reserved_at")
    )
  
  reviews = (
        Review.objects
        .filter(user=request.user)
        .select_related("store")
        .order_by("-created_at")
    )
  
  return render(
        request,
        "members/mypage.html",
        {
            "profile": profile,
            "reservations": reservations,
            "reviews": reviews,
        },
    )

def member_edit(request):
    if request.user.is_staff:
        return render(request, "members/mypage_forbidden.html", status=403)

    profile, _created = MemberProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MemberProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("mypage")
    else:
        form = MemberProfileForm(instance=profile)

    return render(request, "members/member_edit.html", {"form": form})

@login_required(login_url="member_login")
def account_edit(request):
    if request.user.is_staff:
        return render(request, "members/mypage_forbidden.html", status=403)

    if request.method == "POST":
        form = AccountEmailForm(request.POST, user=request.user)
        if form.is_valid():
            email = form.cleaned_data["email"]

            request.user.email = email
            request.user.username = email
            request.user.save(update_fields=["email", "username"])

            return redirect("mypage")
    else:
        form = AccountEmailForm(user=request.user)

    return render(request, "members/account_edit.html", {"form": form})

@login_required(login_url="member_login")
def password_change_view(request):
    if request.user.is_staff:
        return render(request, "members/mypage_forbidden.html", status=403)

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # パスワード更新（ハッシュ化も自動）
            update_session_auth_hash(request, user)  # ログイン状態を維持
            return redirect("mypage")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "members/password_change.html", {"form": form})

