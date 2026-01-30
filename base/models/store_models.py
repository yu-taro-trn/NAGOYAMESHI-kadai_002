from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Category(models.Model): # カテゴリ
  name = models.CharField(max_length=50)
  sort_order = models.PositiveIntegerField(default=0)
  is_active = models.BooleanField(default=True)

  class Meta:
    db_table = 'categories'
    verbose_name = 'カテゴリ'
    verbose_name_plural = 'カテゴリ'
    ordering = ['sort_order', 'id']

  def __str__(self):
    return self.name
    
class Store(models.Model): # 店舗
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    business_day = models.CharField(max_length=100)
    business_hour = models.CharField(max_length=100)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stores'
        verbose_name = '店舗'
        verbose_name_plural = '店舗'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    

class StoreCategory(models.Model): # 店舗カテゴリ(中間テーブル)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="店舗")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="カテゴリ")

    class Meta:
        db_table = 'store_categories'
        verbose_name = '店舗カテゴリ'
        verbose_name_plural = '店舗カテゴリ'
        constraints = [
            models.UniqueConstraint(
                fields=['store', 'category'],
                name='uniq_store_category'
            )
        ]

    def __str__(self):
        return f'{self.store.name} - {self.category.name}'


class Review(models.Model): # レビュー
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='店舗')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='会員')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=100)
    comment = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['store', 'user'],
                name='uniq_review_store_user'
            )
        ]

    def __str__(self):
        return f'{self.store.name} ({self.rating})'


class Reservation(models.Model): # 予約
   
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    canceled_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservations'
        verbose_name = '予約'
        verbose_name_plural = '予約'
        ordering = ['-reserved_at']

    def __str__(self):
        return f'{self.store.name} {self.reserved_at}'