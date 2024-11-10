from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/profile/', views.edit_profile, name='edit_profile'),
    path('user/list/', views.user_list, name='user_list'),
    path('user/add/', views.add_user, name='add_user'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/', views.delete_users, name='delete_users'),
]
