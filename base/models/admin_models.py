from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
    
class CompanyInfo(models.Model): #会社情報
    company_name = models.CharField(max_length=200) 
    representative_name = models.CharField(max_length=200) 
    establishment_date = models.DateField(null=True, blank=True) 
    postal_code = models.CharField(max_length=8, blank=True) 
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20,blank=True)
    business_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "company_infos"
        verbose_name = "会社情報"
        verbose_name_plural = "会社情報"

    def __str__(self):
        return self.company_name 
    
    def clean(self):
        if not self.pk and CompanyInfo.objects.exists():
            raise ValidationError("会社情報は1件のみ登録できます。")

    def save(self, *args, **kwargs):
        if not self.pk and CompanyInfo.objects.exists():
            raise ValidationError("会社情報は1件のみ登録できます。")
        super().save(*args, **kwargs)

class TermsOfService(models.Model): # 会社規約
    version = models.CharField(max_length=50)
    body = models.TextField()
    published_on = models.DateField()
    updated_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "terms_of_services"
        verbose_name = "会員規約"
        verbose_name_plural = "会員規約"
        ordering = ["-published_on", "-id"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_active:
            TermsOfService.objects.exclude(pk=self.pk).filter(is_active=True).update(is_active=False)

    def __str__(self):
        return self.version