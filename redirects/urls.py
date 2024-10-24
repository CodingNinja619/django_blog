from django.urls import path
from . import views
app_name = "redirect"

urlpatterns = [
    path('', views.redirects, name='redirects')
]