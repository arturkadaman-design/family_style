"""
URL configuration for family_style project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),

    # Аутентификация
    path("accounts/login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("accounts/register/", views.register, name="register"),

    # Услуги
    path("services/", views.service_list, name="service_list"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("appointments/new/<slug:slug>/", views.appointment_create, name="appointment_create"),
    path("appointments/my/", views.my_appointments, name="my_appointments"),
    path("appointments/<int:pk>/cancel/", views.appointment_cancel, name="appointment_cancel"),
       # Мастера
    path("masters/", views.master_list, name="master_list"),
    path("masters/<int:pk>/", views.master_detail, name="master_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)