from __future__ import absolute_import

from .models import *

from datetime import datetime 
from django.conf import settings  # noqa
from itertools import islice
import json, logging, pytz
import ast, time, requests
from django.db.models import Sum

import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_utils import to_bytes, to_hex, from_wei, to_int, to_wei
from .helpers import *
import time, os

log = logging.getLogger(__name__)

start_block = 3224520
def Start():
	config, created = Crawler.objects.get_or_create(id=0,defaults={'block_number': start_block},)
	log.warning('*** Crawler started')
	one_day = 48 * settings.BLOCKS_PER_EPOCH
	while True:
		current=getBlock('latest')
		if config.block_number == start_block:
			block_number = Sync(start_block,current.number,current)
			config.block_number = block_number
			config.save()
		if config.block_number <= current.number:
			config.block_number = config.block_number + 1
			config.save()
			ProcessBlock(config.block_number)
			if (config.block_number % settings.BLOCKS_PER_EPOCH == 0):
				ProcessEpoch(config.block_number)

def createEpoch(block_number,block):
	epoch_number =  block_number // settings.BLOCKS_PER_EPOCH
	Epoch.objects.update()
	e,created = Epoch.objects.get_or_create(number=epoch_number, defaults={
		'number' : epoch_number,
		'block_number' : block_number,
		'timestamp' : pytz.utc.localize(datetime.fromtimestamp(float(block.timestamp))),
		'created':pytz.utc.localize(datetime.utcnow())
		})
	e.save()
	return epoch_number,e,created

def createAccount(address,is_candidate,block_number):
	log.debug('create account {0}'.format(address))
	if address is None:
		return None, False
	Account.objects.update()
	#log.warning('create account {0}'.format(address))
	a, created = Account.objects.get_or_create(address=address, defaults={
				'is_candidate':is_candidate,
				'address':address,
				'created':pytz.utc.localize(datetime.utcnow())
			})
	a.last_seen = pytz.utc.localize(datetime.utcnow())
	a.last_seen_block = block_number
	log.debug('\tget balance')
	a.balance = from_wei(getBalance(a.address),'ether')
	log.debug('\tsave')
	a.save()
	return a, created

def createCandidate(candidate,c,block_number,e):
	log.debug('create validator {0}'.format(candidate))
	validator,created = createAccount(candidate,True,block_number)
	if created:
		log.debug('get validator owner {0}'.format(candidate))
		o = getCandidateOwner(candidate)
		log.debug('create validator owner {0}'.format(o))
		owner,created = createAccount(o,False,block_number)
		validator.owner=owner
		validator.save()
	cs,created = Validator.objects.get_or_create(candidate=validator, defaults={
			'candidate':validator,
			'capacity': 100000,
			'first_block':block_number,
			'created':pytz.utc.localize(datetime.utcnow()),
			'epoch':e,
		})			
	if c is not None:
		cs.status = c['status']		
		cs.block_number = block_number
		cs.save()
	return cs,created

def createVote(_vote,vote,block_number,e,unvote=False):
	v, created = Vote.objects.get_or_create(tx=vote.transactionHash)
	if created:
		log.debug('create voter')
		voter = rpc.toChecksumAddress(_vote._voter)
		vo,created = createAccount(voter,False,vote.blockNumber)
		candidate,created = createCandidate(_vote._candidate,None,block_number,e)
		v.candidate=candidate.candidate
		v.epoch=e
		v.account=vo
		v.tx=vote.transactionHash
		v.block_number=vote.blockNumber
		if unvote:
			v.amount=0 - from_wei(_vote._cap,'ether')
		else:
			v.amount=from_wei(_vote._cap,'ether')
		v.save()
	return v, created

def Sync(block_number, current_block, block):
	log.warning('Sync started.')
	log.debug('get all candidates')
	candidates = getCandidates()
	epoch_number,e,created = createEpoch(block_number,block)
	for candidate in candidates['candidates']:
		c = candidates['candidates'][candidate]
		candidate = rpc.toChecksumAddress(candidate)
		log.debug(c)
		createCandidate(candidate,c,block_number,e)

	log.debug('vote filter')
	ProcessVoteFilter(block_number,False)

	log.debug('filter unvote')
	ProcessVoteFilter(block_number,True)

	while block_number < current_block:
		ProcessEpoch(block_number)
		block_number += settings.BLOCKS_PER_EPOCH
	log.warning('Sync complete.')
	return block_number - settings.BLOCKS_PER_EPOCH

def ProcessVoteFilter(block_number,is_unvote):
	log.debug('vote filter')
	if is_unvote:
		vote_filter = validatorABI.events.Unvote.createFilter(fromBlock=block_number-1,toBlock='latest')
	else:
		vote_filter = validatorABI.events.Vote.createFilter(fromBlock=block_number-1,toBlock='latest')
	log.debug('log entries')
	log_entries = vote_filter.get_all_entries()
	for vote in log_entries:
		block_number = vote.blockNumber
		block = getBlock(block_number)
		epoch_number,e,created = createEpoch(block_number,block)
		_vote = vote.args
		log.debug('create vote')
		vote, created = createVote(_vote,vote,block_number,e,is_unvote)

def ProcessBlock(block_number):
	log.warning('Processing Block #{0}'.format(int(block_number) ))
	block = getBlock(block_number)
	log.debug('create eopch')
	epoch_number,e,created = createEpoch(block_number,block)

	log.debug('get all candidates')
	candidates = getCandidates()
	for candidate in candidates['candidates']:
		c = candidates['candidates'][candidate]
		candidate = rpc.toChecksumAddress(candidate)
		log.debug(c)
		createCandidate(candidate,c,block_number,e)

	log.debug('vote filter')
	ProcessVoteFilter(block_number,False)

	log.debug('filter unvote')
	ProcessVoteFilter(block_number,True)


def ProcessEpoch(block_number):
	block = getBlock(block_number)
	epoch_number,e,created = createEpoch(block_number,block)
	log.warning('Processing Epoch #{0}'.format(int(epoch_number)))

	rewards = getRewardsByHash(to_hex(block.hash))

	if rewards is None:
		return None

	if not 'rewards' in rewards:
		return None

	for candidate in rewards['rewards']:
		log.debug(candidate)
		candidate = rpc.toChecksumAddress(candidate)
		validator,created = createAccount(candidate,True,block_number)

		rs = rewards['rewards'][candidate.lower()]
		found_owner = False
		log.debug(rs)
		for voter in rs:
			log.debug('voter {0}'.format(voter))
			voter = rpc.toChecksumAddress(voter)
			vo,created = createAccount(voter,False,block_number)
			log.debug('creating {0}'.format(voter))
			r ,created= Reward.objects.get_or_create(account=vo,epoch=e,defaults={
					'account': vo,
					'epoch': e,
					'candidate': validator,
					'awarded':pytz.utc.localize(datetime.fromtimestamp(float(block.timestamp))),
					'amount':from_wei(rs[voter.lower()],'ether')
				})
			r.save()
			if created:
				log.debug("created")
