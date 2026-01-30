from django.conf import settings
from django.db import models


class Occupation(models.Model): #職業
    name = models.CharField('職業名', max_length=50)
    
    class Meta:
        db_table = 'occupations'
        verbose_name = '職業'
        verbose_name_plural = '職業'

    def __str__(self):
        return self.name

class MemberProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', '男性'
        FEMALE = 'female', '女性'
        OTHER = 'other', 'その他'
        NONE = 'none', '未回答'
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='会員'
    )
    full_name = models.CharField(max_length=100)
    full_name_kana = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.NONE)
    occupation = models.ForeignKey(
        Occupation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'member_profiles'
        verbose_name = '会員'
        verbose_name_plural = '会員'

    def __str__(self):
        return self.full_name