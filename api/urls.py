from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'api'

urlpatterns = [

    url(r'^links/$', views.LinkList.as_view()),
    url(r'^links/(?P<pk>[0-9]+)/$', views.LinkDetail.as_view()),
    url(r'^comments/$', views.CommentList.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view()),
]
