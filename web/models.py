from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import UniqueConstraint

class Link(models.Model):
	created 		= models.DateTimeField(auto_now_add=True)
	url 			= models.URLField(max_length=42,blank=True,default=None,null=True, db_index=True)
	verified		= models.BooleanField(default=False)
	verify_timestamp= models.DateTimeField(auto_now_add=True)

class Account(models.Model):
	# Accounts are voters and validator owners
	user 			= models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		default=None, blank=True, null=True
	)
	address 		= models.CharField(max_length=42,blank=True,default=None,null=True, db_index=True)
	created 		= models.DateTimeField(blank=True,default=None,null=True)
	last_login 		= models.DateTimeField(blank=True,default=None,null=True)
	last_seen 		= models.DateTimeField(auto_now_add=True)
	last_seen_block = models.IntegerField(default=0)
	balance 		= models.DecimalField(default=0,max_digits=99,decimal_places=18)

	is_candidate 	= models.BooleanField(default=False)
	owner 			= models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True
	)

	name 			= models.CharField(max_length=255,blank=True)
	email  			= models.EmailField(max_length=254,blank=True)
	github 			= models.ForeignKey(
		'Link',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True,
		related_name='github'
	)

	linkedin 		= models.ForeignKey(
		'Link',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True,
		related_name='linkedin'
	)
	website 		= models.ForeignKey(
		'Link',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True,
		related_name='website'
	)
	telegram 		= models.CharField(max_length=255,blank=True)
	twitter 		= models.ForeignKey(
		'Link',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True,
		related_name='twitter'
	)
	facebook 		= models.ForeignKey(
		'Link',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True,
		related_name='facebook'
	)

	@property
	def candidates_owned(self):
		return Account.objects.filter(owner=self)
	
	@property
	def is_owner(self):
		return self.candidates_owned.count() > 0
	

class Epoch(models.Model):
	number 			= models.AutoField(primary_key=True)
	block_number 	= models.IntegerField(default=0)
	timestamp 		= models.DateTimeField()
	created 		= models.DateTimeField(blank=True,default=None,null=True)

class Status(models.Model):
	candidate 		=  models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True
	)
	status 			= models.CharField(max_length=10,blank=True,default=None,null=True)
	block_number 	= models.IntegerField(default=0,db_index=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)

class Validator(models.Model):
	candidate 		=  models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True
	)
	capacity 		= models.DecimalField(default=0,max_digits=99,decimal_places=18)
	created 		= models.DateTimeField(blank=True,default=None,null=True)
	last_seen 		= models.DateTimeField(auto_now_add=True)
	first_block 	= models.IntegerField(default=0)
	block_number 	= models.IntegerField(default=0)
	epoch 			=  models.ForeignKey(
		'Epoch',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True
	)

	@property
	def status_history(self):
		return Status.objects.filter(candidate=self.candidate).order_by('-block_number')

	@property
	def status(self):
		status = self.status_history.first()
		if status is None:
			return None
		else:
			return status.status


class Vote(models.Model):
	account =  models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True
	)
	epoch 			=  models.ForeignKey(
		'Epoch',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True
	)
	created 		= models.DateTimeField(auto_now_add=True)
	amount 			= models.DecimalField(default=0,max_digits=99,decimal_places=18)
	block_number 	= models.IntegerField(default=0)
	tx 				= models.CharField(max_length=132,blank=True,default=None,null=True)
	candidate 		=  models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True,
		related_name='vote_candidate'
	)

class Reward(models.Model):
	account 		=  models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True
	)
	candidate 		=  models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True,
		related_name='reward_candidate'
	)
	amount 			= models.DecimalField(default=0,max_digits=99,decimal_places=18)
	awarded 		= models.DateTimeField(blank=True,default=None,null=True)
	epoch 			=  models.ForeignKey(
		'Epoch',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True,
	)
	class Meta:
		index_together = ("account", "epoch","candidate")

class Signers(models.Model):
	account 		=  models.ForeignKey(
		'Account',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True,
	)
	amount 			= models.DecimalField(default=0,max_digits=99,decimal_places=18)
	awarded 		= models.DateTimeField(auto_now_add=True)
	sign 		 	= models.IntegerField(default=0)
	epoch 			=  models.ForeignKey(
		'Epoch',
		on_delete=models.CASCADE,
		default=None, blank=True, null=True, db_index=True,
	)
	class Meta:
		index_together = ("account", "epoch",)

class Crawler (models.Model):
	block_number 	= models.IntegerField(default=0)
	last_run_roi 	= models.DateTimeField(default=None, blank=True, null=True)
