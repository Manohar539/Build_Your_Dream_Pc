from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('builder/', views.builder_view, name="builder"),

    path('save-config/', views.save_configuration, name="save_config"),

    path('checkout/', views.checkout_view, name="checkout"),

    path('my-builds/', views.my_builds, name="my_builds"),
    path('delete-build/<int:build_id>/', views.remove_build, name="delete_build"),

    path('my-orders/', views.my_orders, name="my_orders"),

    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),

    path('accounts/signup/', views.signup, name="signup"),
    path('accounts/login/', views.user_login, name="login"),
    path('accounts/logout/', views.user_logout, name="logout"),
]