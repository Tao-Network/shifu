from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.urls.exceptions import NoReverseMatch
from django.conf import settings
import random
import string, json
from django.contrib.auth.models import User
from django.http import Http404
from web.models import Account, Reward
from web3 import Web3
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django import forms
from django.contrib.auth import authenticate, get_user_model

from django.utils.translation import ugettext_lazy as _
from .utils import validate_eth_address
import logging

log = logging.getLogger(__name__)


class LoginForm(forms.Form):
    signature = forms.CharField(widget=forms.HiddenInput, max_length=132)
    address = forms.CharField(widget=forms.HiddenInput, max_length=42, validators=[validate_eth_address])

    def __init__(self, token, *args, **kwargs):
        self.token = token
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_signature(self):
        sig = self.cleaned_data['signature']
        if len(sig) != 132 or (sig[130:] != '1b' and sig[130:] != '1c') or \
            not all(c in string.hexdigits for c in sig[2:]):
            raise forms.ValidationError(_('Invalid signature'))
        return sig


# list(set()) here is to eliminate the possibility of double including the address field
signup_fields = list(set(settings.WEB3AUTH_USER_SIGNUP_FIELDS + [settings.WEB3AUTH_USER_ADDRESS_FIELD]))

def get_redirect_url(request):
    if request.GET.get('next'):
        return request.GET.get('next')
    elif request.POST.get('next'):
        return request.POST.get('next')
    elif settings.LOGIN_REDIRECT_URL:
        try:
            url = reverse(settings.LOGIN_REDIRECT_URL)
        except NoReverseMatch:
            url = settings.LOGIN_REDIRECT_URL
        return url

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_api(request):
	if request.method == 'GET':
		token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(32))
		request.session['login_token'] = token
		return JsonResponse({'data': token, 'success': True})
	else:
		token = request.session.get('login_token')
		if not token:
			return JsonResponse({'error': _(
				"No login token in session, please request token again by sending GET request to this url"),
				'success': False})
		else:
			form = LoginForm(token, request.POST)
			if form.is_valid():
				signature, address = form.cleaned_data.get("signature"), form.cleaned_data.get("address")
				del request.session['login_token']
				user = authenticate(request, token=token, address=address, signature=signature)
				if user:
					login(request, user, 'web.backend.Web3Backend')
					Account.objects.update()
					account, created = Account.objects.get_or_create(address=address,defaults={
							'user':user,
							'address':user.username,
							'is_candidate':False,
						})
					if not created:
						account.user = user
					account.save()
					user.account = account
					return JsonResponse({'success': True, 'redirect_url': get_redirect_url(request)})
				else:
					addr_field = settings.WEB3AUTH_USER_ADDRESS_FIELD
					user = User.objects.create_user(username=address)
					user.save()
					user = authenticate(request, token=token, address=address, signature=signature)
					if user:
						login(request, user, 'web.backend.Web3Backend')
						Account.objects.update()
						account, created = Account.objects.get_or_create(address=address,defaults={
								'user':user,
								'address':user.username,
								'is_candidate':False,
							})
						if not created:
							account.user = user
						account.save()
						user.account = account
						return JsonResponse({'success': True, 'redirect_url': get_redirect_url(request)})
					else:
						return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})
			else:
				return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})

