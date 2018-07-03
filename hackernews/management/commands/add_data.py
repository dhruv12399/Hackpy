from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests
from bs4 import BeautifulSoup
import sys
from django.contrib.auth.models import User
from hackernews.models import Link, Comments 
import datetime
from django.utils import timezone
from elasticsearch import Elasticsearch
import requests
import json


class Command(BaseCommand):
	help = 'adds data to index '
	
	def handle(self, *args, **options):
		
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

		response = requests.get('http://localhost:9200')

		i=1

		while response.status_code == 200:
			response = requests.get('http://localhost:8000/hackernews/links/' + str(i))
			es.index(index = 'hackernews', doc_type = 'links', id = i, body = json.loads(response.content))
			i = i+1

		print "indexed ",i, "Links to ES"


		self.stdout.write(self.style.SUCCESS('Successfully added data'))