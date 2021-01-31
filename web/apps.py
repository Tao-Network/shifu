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
		return True
