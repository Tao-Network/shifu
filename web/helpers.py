from django.conf import settings  # noqa
import requests,json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Avg
from datetime import datetime, timedelta

from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_utils import to_bytes, to_hex, from_wei, to_int,is_hex_address
import json, time, pytz
import sha3, ethereum
from django import forms
from django.utils.translation import ugettext_lazy as _

rpc = None
for _ in range(settings.MAX_RETRIES):
	try:
		rpc = Web3(Web3.HTTPProvider(settings.RESTFUL_ENDPOINT))
		rpc.middleware_onion.inject(geth_poa_middleware, layer=0)
		break	
	except:
		time.sleep(1)
import logging

log = logging.getLogger(__name__)

with open('{0}/abis/TaoValidator.abi'.format(settings.BASE_DIR), 'r') as f:
	ValidatorABI = json.load(f)
validatorABI = rpc.eth.contract(abi=ValidatorABI, address=settings.VALIDATOR_CONTRACT_ADDRESS)

with open('{0}/json/network_validators.json'.format(settings.BASE_DIR), 'r') as f:
	network_validators = json.load(f)

with open('{0}/json/known_accounts.json'.format(settings.BASE_DIR), 'r') as f:
	known_accounts = json.load(f)

def sig_to_vrs(sig):
    #    sig_bytes = bytes.fromhex(sig[2:])
    r = int(sig[2:66], 16)
    s = int(sig[66:130], 16)
    v = int(sig[130:], 16)
    return v, r, s


def hash_personal_message(msg):
    padded = "\x19Ethereum Signed Message:\n" + str(len(msg)) + msg
    return sha3.keccak_256(bytes(padded, 'utf8')).digest()


def recover_to_addr(msg, sig):
    msghash = hash_personal_message(msg)
    vrs = sig_to_vrs(sig)
    return '0x' + sha3.keccak_256(ethereum.utils.ecrecover_to_pub(msghash, *vrs)).hexdigest()[24:]


def validate_eth_address(value):
    if not is_hex_address(value):
        raise forms.ValidationError(
            _('%(value)s is not a valid Ethereum address'),
            params={'value': value},
        )

def getBalance(address):
	if address is None:
		return 0
	for _ in range(settings.MAX_RETRIES):
		try:
			return rpc.eth.getBalance(address)
		except:
			time.sleep(1)
	return 0

def getBlock(identifier):
	if identifier is None:
		return None
	for _ in range(settings.MAX_RETRIES):
		try:
			return rpc.eth.getBlock(identifier)
		except:
			time.sleep(1)
	return None

def getVoters(c):
	if c is None:
		return None
	for _ in range(settings.MAX_RETRIES):
		try:
			return validatorABI.functions.getVoters(c).call()
		except:
			import time
			time.sleep(1)
	return None

def getCandidateOwner(c):
	if c is None:
		return None
	for _ in range(settings.MAX_RETRIES):
		try:
			return validatorABI.functions.getCandidateOwner(c).call()
		except:
			import time
			time.sleep(1)
	return None

def getVoteAmount(c,v):
	if c is None or v is None:
		return None
	for _ in range(settings.MAX_RETRIES):
		try:
			return validatorABI.functions.getVoterCap(c,v).call()
		except:
			import time
			time.sleep(1)
	return None

def getCandidates():
	for _ in range(settings.MAX_RETRIES):
		try:
			return callRpc({
			'method': 'eth_getCandidates',
			'params': [ 'latest' ],
			'id': settings.CHAIN_ID,
			})
		except:
			import time
			time.sleep(1)
	return None

def getCandidateCapacity(c):
	if c is None:
		return None
	for _ in range(settings.MAX_RETRIES):
		try:
			return validatorABI.functions.getCandidateCap(c).call()
		except:
			import time
			time.sleep(1)
	return None

def getRewardsByHash(block_hash):
	if block_hash is None:
		return None
	for _ in range(settings.MAX_RETRIES):
		try:
			return callRpc({
			'method': 'eth_getRewardByHash',
			'params': [block_hash],
			'id': settings.CHAIN_ID,
			})
		except:
			import time
			time.sleep(1)
	return None

def calculateROIByTime(start,block_number,account,epoch_rewards,votes):
	now = pytz.utc.localize(datetime.now())
	days_from_now = (now - start).days

	start_block = block_number - (days_from_now * settings.BLOCKS_PER_DAY)
	end_block = block_number 

	total = epoch_rewards.filter(awarded__gte=start,awarded__lte=now).aggregate(total=Sum('amount'))

	vote_total = votes.filter(block_number__gte=start_block,block_number__lte=end_block).aggregate(total=Sum('amount'))

	staked = 0
	if account.is_owner:
		staked = (account.candidates_owned.count() * 100000)
	if account.is_candidate:
		staked = 100000

	if vote_total['total'] is None:
		vote_total['total'] = staked 
	else:
		vote_total['total'] = vote_total['total'] + staked

	result="{:.2f}".format((total['total'] / vote_total['total']) * 100)

	return result

def calculateActualROI(address):
	from .models import Crawler, Account, Reward, Vote 
	config = Crawler.objects.get(id=0)
	block_number = config.block_number - 1
	account=None
	if address is not None:
		account = Account.objects.get(address__iexact=address)
		if account.is_candidate:
			epoch_rewards = Reward.objects.select_related('account').filter(candidate=account).order_by('-awarded')
			votes = Vote.objects.filter(candidate=account)
		else:
			epoch_rewards = Reward.objects.select_related('candidate').filter(account=account).order_by('-awarded')
			votes = Vote.objects.filter(account=account)
	else:
		epoch_rewards = Reward.objects.select_related('account','candidate').order_by('-awarded')
		votes = Vote.objects

	if epoch_rewards is not None:
		start = pytz.utc.localize(datetime.now() - timedelta(hours=24))
		yesterday_result = calculateROIByTime(start,block_number,account,epoch_rewards,votes)

		start = pytz.utc.localize(datetime.now() - timedelta(days=7))
		last_week_result = calculateROIByTime(start,block_number,account,epoch_rewards,votes)

		start = pytz.utc.localize(datetime.now() - timedelta(days=30))
		last_month_result = calculateROIByTime(start,block_number,account,epoch_rewards,votes)
	else:
		yesterday_result="{:.2f}".format(0.00)
		last_week_result="{:.2f}".format(0.00)
		last_month_result="{:.2f}".format(0.00)

	result={
		'y':yesterday_result,
		'lw':last_week_result,
		'lm':last_month_result,
	}

	return result

def calculateROI(address):
	if address is None:
		return None
	from .models import Crawler, Account, Reward, Vote 
	config = Crawler.objects.get(id=0)
	block_number = config.block_number - 1
	epoch = block_number // settings.BLOCKS_PER_EPOCH

	avg_daily_roi = 0
	avg_weekly_roi = 0
	avg_yearly_roi = 0
	lifetime_roi = 0
	staked = float(0)
	earnings = float(0)

	#try:
	account = Account.objects.get(address__iexact=address)
	if account.is_candidate:
		rewards = Reward.objects.filter(candidate=account)
		votes = Vote.objects.filter(candidate=account)
		staked += 100000
	else:
		rewards = Reward.objects.filter(account=account)
		votes = Vote.objects.filter(account=account)
		if account.is_owner:
			staked += (account.candidates_owned.count() * 100000)

	stake_total = votes.aggregate(total=Sum('amount'))
	if stake_total['total'] is None:
		stake_total = 0
	else:
		stake_total = float(stake_total['total'])
	staked += stake_total

	reward_total = rewards.aggregate(total=Sum('amount'))
	if reward_total['total'] is None:
		reward = 0
	else:
		reward = float(reward_total['total'])
	earnings += reward

	avg_daily_rewards = earnings / 48
	avg_weekly_rewards = avg_daily_rewards * 7
	avg_yearly_rewards = avg_weekly_rewards * 52
	avg_monthly_rewards = avg_yearly_rewards / 12

	if staked > 0:
		avg_daily_roi = (avg_daily_rewards / staked) * 100
		avg_weekly_roi = (avg_weekly_rewards / staked) * 100
		avg_yearly_roi = (avg_yearly_rewards / staked) * 100
		avg_monthly_roi = (avg_monthly_rewards / staked) * 100
		lifetime_roi = (earnings / staked) * 100
	else:
		avg_daily_roi = 0
		avg_weekly_roi = 0
		avg_yearly_roi = 0
		avg_monthly_roi = 0
		lifetime_roi = 0

	data = {
		"timestamp" : datetime.now(),
		"block" : block_number,
		"epoch" : epoch,
		"is_candidate" : account.is_candidate,
		"locked" : staked,
		"earnings" : earnings,
		"avg_daily_roi" : "{:.2f}".format(avg_daily_roi),
		"avg_weekly_roi" : "{:.2f}".format(avg_weekly_roi),
		"avg_monthly_roi" : "{:.2f}".format(avg_monthly_roi),
		"avg_yearly_roi" : "{:.2f}".format(avg_yearly_roi),
		"lifetime_roi" : "{:.2f}".format(lifetime_roi),
		}
	return 	data
	#except:
	#	return Http404()

def callRpc(data):
	"""
	Make a standard geth style RPC call

	"""
	if data is None:
		return None

	method = data['method']
	params = data['params']
	chain_id = data['id']
	geth_req = {
			'jsonrpc': '2.0',
			'method': method,
			'params': params,
			'id': chain_id,
	}
	#result = requests.post(url='{0}/{1}'.format(settings.RESTFUL_ENDPOINT,method), json=geth_req)
	#return result.json()['result']
	for _ in range(settings.MAX_RETRIES):
		try:
			result = requests.post(url='{0}/{1}'.format(settings.RESTFUL_ENDPOINT,method), json=geth_req)
			return result.json()['result']
		except:
			import time
			time.sleep(1)

	return None