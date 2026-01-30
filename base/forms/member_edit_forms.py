from django import forms
from base.models import MemberProfile


class MemberProfileForm(forms.ModelForm):
    class Meta: 
        model = MemberProfile
        fields = [
            "full_name",
            "full_name_kana",
            "birth_date",
            "gender",
            "occupation",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }
