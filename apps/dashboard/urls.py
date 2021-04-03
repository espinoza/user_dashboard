from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.registration),
    path('logout', views.logout),
    path('dashboard/admin', views.dashboard_admin),
    path('dashboard', views.dashboard),
    path('users/edit/<int:id>', views.admin_edit_user, name='admin_edit_user'),
    path('users/edit/<int:id>/change_password', views.admin_change_password, name='admin_change_password'),
    path('users/edit/<int:id>/remove', views.admin_remove_user, name='admin_remove_user'),
    path('users/show/<int:id>', views.show_messages, name="show_messages"),
    path('users/show/<int:user_showing_id>/comment', views.new_comment, name="new_comment"),
]
