# Hackpy
Django based project similar to hacker news to understand and implement django framework.

## Main python Libraries Used:

- **Rest Framework** as API framework
- **Elasticsearch** to implement search
- **Memcached** for caching
- **Beautifulsoup4** for parsing html while crawling data
- **Celery** to run crawling tasks parallelly 
- **Jinja2** as template language


## Installation
To get this project running on your own system, refer to the steps as following:
1. Clone the repository 
```
	git clone https://github.com/dhruv12399/Hackpy.git
```
2. Set up mySQL database
```
	apt-get install mysql-server
```
3. Create a new database (from the mysqlclient)
```
	create database hackpydb
```
4. Run migrations
```
	python manage.py migrate
```
5. Start the celery worker and crawl data
```
	celery -A hackpy worker
	python crawl.py
```
6. Install and configure elasticsearch
```
	systemctl enable elasticsearch.service
	python manage.py add_data
```
7. Runserver and you are good to go! :smile:
```
	python manage.py runserver
```

