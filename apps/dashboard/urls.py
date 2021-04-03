from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('dashboard/admin', views.dashboard_admin),
    path('dashboard', views.dashboard),
    path('users/edit/<int:id>', views.admin_edit_user, name='admin_edit_user'),
    path('users/edit/<int:id>/change_password', views.admin_change_password, name='admin_change_password'),
    path('users/edit/<int:id>/remove', views.admin_remove_user, name='admin_remove_user'),
]
