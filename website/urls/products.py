from django.urls import path, re_path
from website import views

app_name = 'website'
urlpatterns = [
    re_path(r'^(?P<product_id>[0-9]+)/$', views.detail, name="detail"),
    path('', views.result, name="result"),
]
