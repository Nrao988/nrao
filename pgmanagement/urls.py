"""pgmanagement URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from pgmanage.views import pgm_create_view, pgm_update_view, pgm_delete_view,\
    pgmanagers_views, home_views, index_view, register_views, login_view, signout_view, current_datetime
from django.views.generic import TemplateView, ListView, CreateView,\
    UpdateView, DeleteView
from pgmanage.models import PG, Room


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pgmanager_create/', pgm_create_view),
    path('pgmanager_update/<int:pk>/', pgm_update_view),
    path('pgmanager_delete/<int:pk>/', pgm_delete_view),
    path('pgmanagers/', pgmanagers_views),
    path('home/',home_views),
    path('', index_view),
    path('register/',register_views),
    path('login/', login_view),
    path('signout/',signout_view),
    path('datetime/', current_datetime),
    url(r'^pgs/', ListView.as_view(
        model=PG,
        #template_name="pgmanager/",
        #queryset=PG.objects.all(),
        # fields=
        )),
    url(r'^pg_create/',CreateView.as_view(
        model=PG,
        fields="__all__",
        success_url='/pgs/'
        )),
    url(r'^pg_update/<int:pk>/',UpdateView.as_view(
        model=PG,
        fields="__all__",
        success_url='/pgs/'
        )),
    url(r'^pg_delete/<int:pk>/',DeleteView.as_view(
        model=PG,
        success_url='/pgs/'
        )),
url(r'^room_create/',CreateView.as_view(
        model=Room,
        fields="__all__",
        success_url='/rooms/'
        )),
    url(r'^room_update/<int:pk>/',UpdateView.as_view(
        model=Room,
        fields="__all__",
        success_url='/rooms/'
        )),
    url(r'^room_delete/<int:pk>/',DeleteView.as_view(
        model=Room,
        success_url='/rooms/'
        )),
    url(r'^rooms/',ListView.as_view(
        model=Room
        )),



]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

