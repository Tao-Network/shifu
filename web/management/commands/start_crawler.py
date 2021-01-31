from django.core.management.base import BaseCommand
from django.utils import timezone
from web.tasks import Start
import os,logging
class Command(BaseCommand):
	help = 'Starts the crawler'

	def handle(self, *args, **kwargs):
		if not os.path.exists('crawler.pid'): 
			from web.tasks import Start
			log = logging.getLogger('console')
			log.warning('Crawler firing up')
			Start()
			log.warning('Crawler started')
