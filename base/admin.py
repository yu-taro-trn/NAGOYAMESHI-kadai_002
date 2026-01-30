from django.contrib import admin
from base.models import CompanyInfo, TermsOfService, Category, Store, StoreCategory, Review, Reservation
from base.models.member_models import MemberProfile, Occupation
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

# -----------------------------
# admin_models.py
# -----------------------------

User = get_user_model()

admin.site.unregister(User)

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'representative_name', 'updated_at')
    search_fields = ('company_name', 'representative_name')
    ordering = ('-updated_at',)

    def has_add_permission(self, request):
        return not CompanyInfo.objects.exists()


@admin.register(TermsOfService)
class TermsOfServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'is_active', 'published_on', 'updated_on')
    search_fields = ('version',)
    ordering = ('-published_on', '-id')

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=True)  # 管理者だけ表示
    
# -----------------------------
# store_models.py
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'sort_order')
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ('sort_order', 'id')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'business_day', 'is_published', 'created_at')
    search_fields = ('name', 'address', 'phone_number')
    list_filter = ('is_published',)
    ordering = ('-created_at', '-id')


@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'category')
    search_fields = ('store__name', 'category__name')
    ordering = ('-id',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('store', 'user', 'rating', 'title', 'is_published', 'created_at')
    search_fields = ('store__name', 'user__username', 'user__email', 'title')
    list_filter = ('is_published', 'rating')
    ordering = ('-created_at', '-id')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('store', 'user', 'reserved_at', 'number_of_people', 'status', 'canceled_at')
    search_fields = ('store__name', 'user__username', 'user__email')
    list_filter = ('status',)
    ordering = ('-reserved_at', '-id')

# -----------------------------
# member_models.py
# -----------------------------
@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user', 'occupation', 'is_active', 'updated_at')
    search_fields = ('full_name', 'full_name_kana', 'user__username', 'user__email')
    list_filter = ('is_active', 'occupation')
    ordering = ('-updated_at', '-id')