from django.apps import AppConfig
from django.apps import AppConfig
import logging, sys
import time, os

class WebConfig(AppConfig):
    name = 'web'

class CrawlerConfig(AppConfig):
	name = 'web'
	verbose_name = "Blockchain Crawler"

	def ready(self):
		if 'runserver' not in sys.argv:
			return True
		# you must import your modules here 
		# to avoid AppRegistryNotReady exception 
		from .tasks import Start
		log = logging.getLogger('console')
		#Start.delay()
		return True
