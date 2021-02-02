from rest_framework import serializers
from .models import Reward, Account
class _Vote:
	def __init__(self, block_number, amount, candidate, voter):
		self.block_number = block_number
		self.amount = amount
		self.candidate = candidate
		self.voter = voter

class VoteSerializer(serializers.Serializer):
	block_number = serializers.IntegerField(default=0)
	amount = serializers.DecimalField(default=0,max_digits=99,decimal_places=18)
	candidate = serializers.CharField(max_length=42,default=None)
	voter = serializers.CharField(max_length=42,default=None)
	class Meta:
		model = _Vote

class _Roi:
	def __init__(self,timestamp,block,epoch,is_candidate,locked,earnings,avg_daily_roi,avg_weekly_roi,avg_monthly_roi,avg_yearly_roi,lifetime_roi):
		self.timestamp = timestamp
		self.block = block
		self.epoch = epoch
		self.is_candidate = is_candidate
		self.locked = locked
		self.earnings = earnings
		self.avg_daily_roi = avg_daily_roi
		self.avg_weekly_roi = avg_weekly_roi
		self.avg_monthly_roi = avg_monthly_roi
		self.avg_yearly_roi = avg_yearly_roi
		self.lifetime_roi = lifetime_roi

class RoiSerializer(serializers.Serializer):
	timestamp = serializers.DateTimeField()
	block = serializers.IntegerField()
	epoch = serializers.IntegerField()
	is_candidate = serializers.BooleanField()
	locked = serializers.IntegerField()
	earnings = serializers.DecimalField(default=0,max_digits=99,decimal_places=18)
	avg_daily_roi = serializers.DecimalField(default=0,max_digits=99,decimal_places=2)
	avg_weekly_roi = serializers.DecimalField(default=0,max_digits=99,decimal_places=2)
	avg_monthly_roi = serializers.DecimalField(default=0,max_digits=99,decimal_places=2)
	avg_yearly_roi = serializers.DecimalField(default=0,max_digits=99,decimal_places=2)
	lifetime_roi = serializers.DecimalField(default=0,max_digits=99,decimal_places=2)
	class Meta:
		model = _Roi

class _NetworkInfo:
	def __init__(self, current_block, block_timestamp, epoch, epoch_start_time, validator_count, voter_count, locked, voter_avg_roi, validator_avg_roi):
		self.current_block=current_block
		self.block_timestamp=block_timestamp
		self.epoch=epoch 
		self.epoch_start_time=epoch_start_time
		self.validator_count=validator_count
		self.voter_count=voter_count
		self.locked=locked
		self.voter_avg_roi=voter_avg_roi
		self.validator_avg_roi=validator_avg_roi

class NetworkInfoSerializer(serializers.Serializer):
	current_block = serializers.IntegerField()
	block_timestamp = serializers.DateTimeField()
	epoch = serializers.IntegerField()
	epoch_start_time=serializers.DateTimeField()
	validator_count=serializers.IntegerField()
	voter_count=serializers.IntegerField()
	locked=serializers.DecimalField(max_digits=99,decimal_places=18)
	voter_avg_roi=serializers.DecimalField(max_digits=99,decimal_places=2)
	validator_avg_roi=serializers.DecimalField(max_digits=99,decimal_places=2)
	class Meta:
		model = _NetworkInfo

class _Candidate:
	def __init__(self,rank,address,voters,status,roi):
		self.rank=rank
		self.address=address
		self.voters=voters
		self.status=status
		self.roi=roi

class CandidateSerializer(serializers.Serializer):
	rank=serializers.IntegerField()
	address=serializers.CharField(max_length=42)
	status=serializers.CharField(max_length=20)
	voters=serializers.IntegerField()
	roi=serializers.DecimalField(max_digits=99,decimal_places=2)
	class Meta:
		model=_Candidate
		
class _AllCandidates:
	def __init__(self,candidates):
		self.candidates=candidates

class AllCandidatesSerializer(serializers.Serializer):
	candidates=serializers.ListField()

class _OwnedCandidate:
	def __init__(self,address,status,roi):
		self.address=address
		self.status=status
		self.roi=roi

class OwnedCandidateSerializer(serializers.Serializer):
	address=serializers.CharField(max_length=42)
	status=serializers.CharField(max_length=20)
	roi=serializers.DecimalField(max_digits=99,decimal_places=2)
	class Meta:
		model = _OwnedCandidate

class _OwnedCandidates:
	def __init__(self,candidates):
		self.candidates=candidates

class OwnedCandidatesSerializer(serializers.Serializer):
	candidates=serializers.ListField()
	class Meta:
		model = _OwnedCandidates

class _Earnings:
	def __init__(self, is_candidate, total_earnings, earnings):
		self.is_candidate=is_candidate
		self.total_earnings=total_earnings
		self.earnings=earnings

class _DailyEarnings:
	def __init__(self,date,total):
		self.date=date
		self.total=total

class DailyEarningsSerializer(serializers.Serializer):
	date=serializers.DateTimeField()
	total=serializers.DecimalField(max_digits=99,decimal_places=18)
	class Meta:
		model=_DailyEarnings

class EarningsDetailsSerializer(serializers.ModelSerializer):
	candidate = serializers.StringRelatedField()
	account = serializers.StringRelatedField()
	class Meta:
		model = Reward
		fields=['account','candidate','amount','epoch','awarded']

class EarningsSerializer(serializers.Serializer):
	is_candidate=serializers.BooleanField()
	total_earnings=serializers.DecimalField(max_digits=99,decimal_places=18)
	earnings=serializers.ListField()
	class Meta:
		model = _Earnings