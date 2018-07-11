from celery import Celery
from hackpy.tasks import ScanPage
from hackpy.tasks import CrawlLink
from hackpy.tasks import CrawlComment

for i in range(1,14):
	ScanPage(i)