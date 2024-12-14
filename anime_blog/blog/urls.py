from django.urls import path
from .views import post_list, post_detail, search_posts, user_login, user_logout, register

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('search/', search_posts, name='search_posts'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
]
