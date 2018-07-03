# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Link, Comments 
from .forms import LinkForm, CommentForm
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import sys
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LinkSerializer
from elasticsearch import Elasticsearch

# Create your views here.

def signup(request):
	form = UserCreationForm()
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return HttpResponseRedirect(reverse('hackernews:home'))

	return render(request, 'hackernews/signup.jinja', {'form': form})

def calculate_score(votes, item_hour_age, gravity=1.8):
	return (votes - 1) / pow((item_hour_age+2), gravity)

@login_required
def home(request):
	print 'here1'
	linklist = Link.objects.all()
	for link in linklist:
		ith = (timezone.now() - link.added_time).seconds/3600
		if (timezone.now() - link.added_time).days > 0 :
			ith += (timezone.now() - link.added_time).days*24
		link.score = calculate_score(link.votes, ith)
		link.save()
	linklist = linklist.order_by('-score')
	nowtime = timezone.now()
	return render(request, 'hackernews/home.jinja', {'linklist':linklist, 'nowtime':nowtime})

@login_required
def add_new_link(request):
	form_link = LinkForm()
	if request.method == 'POST':
		form_link = LinkForm(request.POST)
		if form_link.is_valid():
			form_instance = form_link.save(commit = False)
			form_instance.added_by = request.user
			form_instance.added_time = timezone.now()
			form_instance.parent = form_instance.url.split('/')[2]
			form_instance.save()

		return HttpResponseRedirect(reverse('hackernews:home'))

	else:
		return render(request, 'hackernews/addnewlink.jinja', {'form': form_link})

@login_required
def comment_page(request, link_id):
	link = get_object_or_404(Link, pk = link_id)
	com_list = Comments.objects.filter( linked_to = link)
	nowtime = timezone.now()
	form_com = CommentForm()
	if request.method == 'POST':
		form_com = CommentForm(request.POST)
		if form_com.is_valid():
			form_instance = form_com.save(commit = False)
			form_instance.added_by = request.user
			form_instance.linked_to = link
			form_instance.parent = None
			form_instance.save()
		return HttpResponseRedirect(reverse('hackernews:commentpage',args = (link_id, )))

	else:
		return render(request, 'hackernews/commentpage.jinja', {'form':form_com, 'com_list':com_list, 'link':link, 'nowtime':nowtime})


@login_required
def add_reply(request, comment_id, link_id):
	comment = get_object_or_404(Comments, pk = comment_id)
	link = get_object_or_404(Link, pk = link_id)
	com_list = Comments.objects.filter( linked_to = link)
	form_reply = CommentForm()
	if request.method == 'POST':
		form_reply = CommentForm(request.POST)
		if form_reply.is_valid():
			form_instance = form_reply.save(commit = False)
			form_instance.added_by = request.user
			form_instance.linked_to = link
			form_instance.parent = comment
			form_instance.save()
		return HttpResponseRedirect(reverse('hackernews:commentpage',args = (link_id, )))

	else:
		return render(request, 'hackernews/addreply.jinja', {'form':form_reply, 'com_list':com_list})


@login_required
@csrf_exempt
def upvote(request, link_id):
	print "link_id"
	link = get_object_or_404(Link, pk=link_id)
	print "link found"
	link.upvoted_users.add(request.user)
	link.votes += 1
	link.save()		
	return

class LinkList(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

def search(request):
	print "here"
	tobesearched = request.GET.get('search')
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	res = es.search(index="hackernews", body={"query": {"prefix": {'title':tobesearched}}})
	res = res['hits']['hits']
	print "here1"
	data = render(request, 'hackernews/searchresult.jinja', {'res':res})
	return data