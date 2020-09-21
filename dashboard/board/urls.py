from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.get_homebase_data),
    url(r'^select_page',views.select_page),
]
