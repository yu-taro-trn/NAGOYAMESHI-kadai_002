from django import forms
from django.contrib.auth import get_user_model
from base.models import Occupation, MemberProfile

User = get_user_model()


class MemberSignupForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    password1 = forms.CharField(label="パスワード", widget=forms.PasswordInput)
    password2 = forms.CharField(label="パスワード（確認）", widget=forms.PasswordInput)

    full_name = forms.CharField(label="氏名", max_length=100)
    full_name_kana = forms.CharField(label="氏名（カナ）", max_length=100)

    birth_date = forms.DateField(
        label="生年月日",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    gender = forms.ChoiceField(
        label="性別",
        required=False,
        choices=MemberProfile.Gender.choices,
    )

    occupation = forms.ModelChoiceField(
        label="職業",
        required=False,
        queryset=Occupation.objects.none(),   # ★ import時にDBアクセスしない
        empty_label="選択してください",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["occupation"].queryset = Occupation.objects.all().order_by("id")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "パスワードが一致しません。")
        return cleaned
