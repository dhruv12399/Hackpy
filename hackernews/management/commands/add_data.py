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
from nltk import ngrams


class Command(BaseCommand):
	help = 'adds data to index '

	def handle(self, *args, **options):
		
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

		response = requests.get('http://localhost:9200')

		i=1

		settings = {
			"settings" : {
				"analysis" : {
					"analyzer" : {
						"my_ngram_analyzer" : {
							"tokenizer" : "my_ngram_tokenizer"
						}
					},
					"tokenizer" : {
						"my_ngram_tokenizer" : {
							"type" : "ngram",
							"min_gram" : "3",
							"max_gram" : "3"
						}
					}
				}
			},
			"mappings": {
				"links":{
					"properties": {
						"title": {
							"type": "string",
							"fields": {
								"ngram": {
									"type": "string",
									"analyzer": "my_ngram_analyzer"
								}
							}
						}
					}
				}
			}
		}

		es.indices.create(index='index2', ignore=400, body=settings)
		# es.indices.get('newindex3')['newindex3']['settings']

		while response.status_code == 200:
			response = requests.get('http://localhost:8000/hackernews/links/' + str(i))
			es.index(index = 'index2', doc_type = 'links', id = i, body = json.loads(response.content))
			i = i+1

		print "indexed ",i," Links to ES"


		self.stdout.write(self.style.SUCCESS('Successfully added data'))