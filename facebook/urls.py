from django.urls import path
from facebook import views

app_name = 'facebook'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
