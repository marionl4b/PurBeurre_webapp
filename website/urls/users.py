from django.urls import path
from django.contrib.auth import views as auth_views
from website import views


urlpatterns = [
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('login/',
         auth_views.LoginView.as_view(template_name="website/login.html"),
         name="login"),
    path('logout/',
         auth_views.LogoutView.as_view(template_name="website/logout.html"),
         name="logout"),

    path('my-products/', views.favorites, name="favorites"),
    ]
