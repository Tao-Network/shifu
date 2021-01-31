from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.conf import settings
import random
import string, json
from django.contrib.auth.models import User
from django.http import Http404
from web.models import Account, Reward
from web3 import Web3
from django.db.models import Sum
from web.helpers import * 
from operator import itemgetter

def logout_view(request):
	logout(request)
	return redirect('/')

def web_login(request):
	if not request.user.is_authenticated:
		return redirect('/auto_login')
	else:
		return redirect('/profile')

def index(request):
	if request.user.is_authenticated:
		request.user.account = Account.objects.get(address=Web3.toChecksumAddress(request.user.username)) 
	else:
		request.user.account = None

	result = Reward.objects.select_related('account').values('account__address').order_by('account__address').annotate(total_reward=Sum('amount')).order_by('-total_reward')
	resa = []
	for r in result:
		address=r['account__address'].lower()
		if not any(address in d for d in known_accounts):
			resa.append(address)
	request.top5_accounts = resa[:3]
	result = Reward.objects.select_related('candidate').values('candidate__address').order_by('candidate__address').annotate(total_reward=Sum('amount')).order_by('-total_reward')	
	resb = []
	for r in result:
		address=r['candidate__address'].lower()
		if not any(address in d for d in known_accounts):
			resb.append(address)
	request.top5_candidates = resb[:3]
	return render(request, 'index.html')

def auto_login(request):
	if not request.user.is_authenticated:
		return render(request, 'web3auth/autologin.html')
	else:
		return redirect('/profile')

def account_profile(request,address=None):
	if address is None:
		if request.user.is_authenticated:
			address = request.user.username
		else:
			raise Http404()
	request.account = Account.objects.filter(address__iexact=address).first()
	if request.account is None:
		raise Http404() 
	return render(request, 'profile.html')
