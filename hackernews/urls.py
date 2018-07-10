from django.conf.urls import url

from . import views
# from mysite.core import views as core_views
from django.contrib.auth import views as auth_views

app_name = 'hackernews'

urlpatterns = [

	url(r'^signup/$', views.signup, name='signup'),
	url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'hackernews/login.jinja'}, name='login'),
    url(r'^addnewlink/$', views.add_new_link, name='addnewlink'),
    url(r'^(?P<link_id>[0-9]+)/commentpage/$', views.comment_page, name='commentpage'),
    url(r'^(?P<link_id>[0-9]+)/(?P<comment_id>[0-9]+)/addreply/$', views.add_reply, name='addreply'),
    url(r'^(?P<link_id>[0-9]+)/upvote/$', views.upvote, name='upvote'),
    url(r'^search/$', views.search, name='search'),

]
