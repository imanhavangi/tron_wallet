from rest_framework import serializers
from .models import Trc20Data
from .models import TransactionData

class Trc20DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trc20Data
        fields = ['contract_address', 'count']

class TransactionDataSerializer(serializers.ModelSerializer):
    class Meta:
      model = TransactionData
      fields = '__all__'
