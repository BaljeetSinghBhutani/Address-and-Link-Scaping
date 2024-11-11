from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-details/', views.scrape_address_with_selenium, name='fetch_details'),
]
