# base/urls.py
from django.urls import path
from base.views.store_views import store_list, store_detail
from base.views.auth_views import member_login, member_logout, member_signup
from base.views.member_views import account_edit, mypage, member_edit, password_change_view

urlpatterns = [
    path('stores/', store_list, name='store_list'),
    path('stores/<int:store_id>/', store_detail, name='store_detail'),

    path('login/', member_login, name='member_login'),
    path('logout/', member_logout, name='member_logout'),
    path('signup/', member_signup, name='member_signup'),
    path('mypage/', mypage, name='mypage'),
    path('mypage/edit',member_edit, name='member_edit'),
    path("mypage/account/edit/", account_edit, name="account_edit"),
    path("mypage/password/change/", password_change_view, name="password_change"),
]
