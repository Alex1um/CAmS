from django.urls import path
from . import views

urlpatterns = [
    path('login', views.simple_login, name='user_login'),
    path('login?next=<path:next_path>', views.simple_login, name='user_login_next'),
    path('register', views.register, name='user_register'),
    path('register?next=<path:next_path>', views.register, name='user_register_next'),
    path('edit', views.NotAllowedPath, name='user_edit'),
    path('logout', views.simple_logout, name='user_logout'),
    path('logout?next=<path:next_path>', views.simple_logout, name='user_logout_next'),
    path('<int:id>', views.NotAllowedPath, name='user_profile')
]