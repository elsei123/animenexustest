from django.urls import path
from .views import post_list, post_detail, user_login, user_logout, register, sobre

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    # Nova rota para a página "Sobre"
    path('sobre/', sobre, name='sobre'),
]
