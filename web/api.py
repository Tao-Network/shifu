from django.http import JsonResponse
from web.models import *
from django.db.models import Sum, Avg
from django.db.models.functions import Cast
from django.db.models import DecimalField
from django.conf import settings
from datetime import datetime, timedelta
from django.http import Http404
import pytz, json
from django.db.models import Q
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_utils import to_bytes, to_hex, from_wei, to_int
from web.helpers import *
from web.serializers import *
from rest_framework.decorators import api_view
from rest_framework import response, schemas
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers import serialize
from rest_framework import status, generics, viewsets
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from web.serializers import _Vote, _Roi, _Earnings, _DailyEarnings, _NetworkInfo, _OwnedCandidates, _OwnedCandidate, _Candidate, _AllCandidates
import logging

log = logging.getLogger(__name__)

class VotesList(APIView):
	"""
	Returns the current votes for an account

	If the address is a validator, it returns the votes for that validator.  If the address is an account, it returns the votes placed by that account.
	"""
	def get(self, request, address, format=None):
		config = Crawler.objects.get(id=0)
		block_number = config.block_number - 1
		epoch = block_number // settings.BLOCKS_PER_EPOCH
		try:
			account = Account.objects.get(address=address)
		except:
			return Http404()

		if account.is_candidate:
			votes = Vote.objects.filter(candidate=account)
		else:
			votes = Vote.objects.filter(account=account)
		data = []
		for vote in votes:
			vote_total = votes.aggregate(votes=Sum('amount'))
			data.append(_Vote(
				block_number=vote.block_number,
				amount=float(vote.amount),
				candidate=vote.candidate.address,
				voter=vote.account.address,
				))
		serializer = VoteSerializer(data, many=True)
		return Response(serializer.data)

class RoiApi(APIView):
	def get(self, request, address, format=None):
		"""
		Return the ROI for a given address

		There are 48 epochs in a day, 7 days in a week, 52 weeks in a year. ROI is calculated as (Earnings / 48) * Timeframe.
		"""
		config = Crawler.objects.get(id=0)
		block_number = config.block_number - 1
		epoch = block_number // settings.BLOCKS_PER_EPOCH
		profile = calculateROI(address)
		serializer = RoiSerializer(_Roi(
			datetime.now(),
			block_number,
			epoch,
			profile['is_candidate'],
			profile['locked'],
			profile['earnings'],
			profile['avg_daily_roi'],
			profile['avg_weekly_roi'],
			profile['avg_monthly_roi'],
			profile['avg_yearly_roi'],
			profile['lifetime_roi'],
		))
		return Response(serializer.data)
		#except:
		#	return Http400()

class NetworkInfoApi(APIView):
	def get(self, request, format=None):
		"""
		Get network information
		"""
		config = Crawler.objects.get(id=0)
		block_number = config.block_number - 1
		block = rpc.eth.getBlock(block_number)
		epoch = block_number // settings.BLOCKS_PER_EPOCH

		last_epoch = epoch - 1
		last_epoch_block = rpc.eth.getBlock(last_epoch * settings.BLOCKS_PER_EPOCH)

		current_participants = 0
		current_validators = 0
		current_voters = 0

		validators = Validator.objects.all()
		current_validators = 0 
		voters = Vote.objects.filter(amount__gt=0).distinct('account')
		current_voters = voters.count()
		current_participants = current_validators + current_voters
		
		total_validator_reward = 0
		total_voter_reward = 0
		total_locked = 0
		total_reward = 0

		validator_avg_roi = []
		voter_avg_roi = []
		for validator in validators:
			address=validator.candidate.address
			if not any(address.lower() in d for d in known_accounts) and not (address.lower() in network_validators):
				current_validators += 1
				v_roi = calculateROI(validator.candidate.address)
				reward_total = float(v_roi['earnings'])
				stake_total = float(v_roi['locked'])

				total_reward += reward_total

				if stake_total > 0:
					voter_roi = (float(total_reward) / stake_total)
				else:
					voter_roi = 0
				voter_avg_roi.append(float(voter_roi))

				validator_avg_roi.append(float(v_roi['lifetime_roi']))

				total_locked += stake_total

		if len(voter_avg_roi) > 0:
			voter_avg = float(sum(voter_avg_roi)) / float(len(voter_avg_roi))
		else:
			voter_avg = 0
		if len(validator_avg_roi) > 0:
			validator_avg = float(sum(validator_avg_roi)) / float(len(validator_avg_roi))
		else:
			validator_avg = 0
		serializer = NetworkInfoSerializer(_NetworkInfo(
				block.number,
				pytz.utc.localize(datetime.fromtimestamp(float(block.timestamp))),
				epoch,
				pytz.utc.localize(datetime.fromtimestamp(float(last_epoch_block.timestamp))),
				current_validators,
				current_voters,
				"{:.0f}".format(total_locked),
				"{:.2f}".format(voter_avg),
				"{:.2f}".format(validator_avg),
		))
		return Response(serializer.data)

class EarningsApi(APIView):
	"""

	Get the earnings for an address.

	The address may be a validator or an account.
	"""
	def get(self, request, address=None, format=None):
		epoch_rewards = None
		account=None
		start_time=pytz.utc.localize(datetime.now())
		start_time = pytz.utc.localize(datetime.today() - timedelta(days=30))
		date_to_calculate = start_time

		if address is not None:
			account = Account.objects.get(address__iexact=address)
			if account.is_candidate:
				epoch_rewards = Reward.objects.filter(candidate=account).order_by('-awarded')
			else:
				epoch_rewards = Reward.objects.filter(account=account).order_by('-awarded')
		else:
			epoch_rewards = Reward.objects.order_by('-awarded')
		results = {
			'is_candidate': account.is_candidate if account is not None else False,
			'total_earnings': 0,
			'earnings':[],
		}
		daily_earnings = []
		total_earnings = 0
		while date_to_calculate <= pytz.utc.localize(datetime.today() - timedelta(days=1)):
			total_awarded_by_day = epoch_rewards.filter(awarded__year=date_to_calculate.year,
										   awarded__month=date_to_calculate.month,
										   awarded__day=date_to_calculate.day).aggregate(total=Sum('amount'))
			date_string = date_to_calculate.strftime("%Y-%m-%d")
			s = DailyEarningsSerializer(_DailyEarnings(
				date=date_string,
				total=total_awarded_by_day['total'] if total_awarded_by_day['total'] is not None else 0
			))
			date_to_calculate = date_to_calculate + timedelta(days=1)
			total_earnings+=total_awarded_by_day['total'] if total_awarded_by_day['total'] is not None else 0
			daily_earnings.append(s.data)
		serializer = EarningsSerializer(_Earnings(
			is_candidate=account.is_candidate if account is not None else False,
			total_earnings=total_earnings,
			earnings=daily_earnings,
		))
		return Response(serializer.data)

class EarningsPagination(PageNumberPagination):
	page_size=10
	draw=1
	def get_paginated_response(self, data):
		return Response({
			'draw': self.draw,
			'recordsFiltered': self.page.paginator.count,
			'recordsTotal': self.page.paginator.count,
			'data': data
		})

class EarningsDetailsApi(generics.ListAPIView):
	queryset = Reward.objects
	serializer_class=EarningsDetailsSerializer

	def get(self,request,address):
		"""
		Details for earnings for a specified account or validator
		"""
		epoch_rewards = None
		account=None
		if address is not None:
			account = Account.objects.get(address__iexact=address)
			if account.is_candidate:
				epoch_rewards = Reward.objects.select_related('account').filter(candidate=account).order_by('-awarded')
			else:
				epoch_rewards = Reward.objects.select_related('candidate').filter(account=account).order_by('-awarded')
		else:
			epoch_rewards = Reward.objects.select_related('account','candidate').order_by('-awarded')

		paginator = EarningsPagination()
		page = request.GET.get('page')
		if page is None:
			# now you can edit it
			start = request.GET.get('start')
			page = (int(start) // 10) + 1
		else:
			page = int(page)
		if not request.GET._mutable:
		   request.GET._mutable = True
		request.GET['page'] = page
		paginator.draw = page
		epoch_rewards = paginator.paginate_queryset(epoch_rewards, request)

		serializer = EarningsDetailsSerializer(epoch_rewards,many=True)
		return paginator.get_paginated_response(serializer.data)

class OwnedCandidatesApi(APIView):
	def get(self,request,address):
		"""
		Get a list of the validators owned by an address
		"""
		candidates = Validator.objects.select_related('candidate').filter(candidate__owner__address__iexact=address).order_by('-status').order_by('created').order_by('-last_seen')
		data = []
		for candidate in candidates:
			address=candidate.candidate.address
			if not any(address.lower() in d for d in known_accounts) and not (address.lower() in network_validators):
				c = OwnedCandidateSerializer(_OwnedCandidate(
					address=candidate.candidate.address,
					status=candidate.status,
					roi=candidate.roi['lifetime_roi'],
				)) 
				data.append(c.data)
		s = OwnedCandidatesSerializer(_OwnedCandidates(data))		
		return Response(s.data)

class AllCandidatesApi(APIView):
	def get(self,request):
		"""
		Get all validators
		"""
		config = Crawler.objects.get(id=0)
		block_number = config.block_number - 1

		block = getBlock(block_number)
		epoch = block.number // settings.BLOCKS_PER_EPOCH

		last_epoch = epoch - 1
		last_epoch_block = rpc.eth.getBlock(last_epoch * settings.BLOCKS_PER_EPOCH)

		candidates = Validator.objects.order_by('-status').order_by('created').order_by('-last_seen')
		voter_count = 0
		staked = 0
		rewards_last_epoch = 0
		last_signed_block = 0
		total_signed_blocks = 0
		data = []
		rank = 1

		active=[]
		offline=[]
		for candidate in candidates:
			address=candidate.candidate.address
			if not any(address.lower() in d for d in known_accounts) and not (address.lower() in network_validators):
				r = Reward.objects.filter(epoch=last_epoch,candidate=candidate.candidate)
				voters = Vote.objects.filter(amount__gt=0,candidate=candidate.candidate)
				voter_count = voters.distinct('account').count()

				roi = calculateROI(candidate.candidate.address)
				c=CandidateSerializer(_Candidate(
					rank=rank,
					address=candidate.candidate.address,
					status=candidate.status,
					voters=voter_count,
					roi=float(roi['lifetime_roi']),
					))
				if c.data['status'] == 'SLASHED' or c.data['status'] == 'RESIGNED':
					offline.append(c.data)
				else:
					rank += 1
					active.append(c.data)
		sorted_data = sorted(active, key=lambda k: k['roi'], reverse=False) 

		rank = 1
		for x in range(0,len(sorted_data)-1):
			sorted_data[x].rank=rank
			rank += 1
		sorted_data = sorted_data + offline
		s=AllCandidatesSerializer(_AllCandidates(candidates=sorted_data))
		return Response(s.data)
