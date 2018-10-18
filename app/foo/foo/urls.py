"""foo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from test1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/<int:user>", views.show_person),
    path("user/create", views.create_person_result),
    path("user/<int:user>/delete", views.person_delete),
    path("user/<int:user>/update", views.person_update),
    path('things/<int:id>/update', views.update_thing),
    path("things/<int:id>", views.show_thing),
    path("things/create", views.create_thing),
    path("things/<int:id>/delete", views.delete_thing),
    path("user/checknum", views.check_user_num)
]

