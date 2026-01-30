from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountEmailForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields["email"].initial = user.email or user.username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        qs = User.objects.exclude(pk=self.user.pk)
        if qs.filter(username=email).exists() or qs.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")

        return email