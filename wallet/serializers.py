from rest_framework import serializers
from .models import Trc20Data
from .models import TransferData
from .models import TransactionData
from .models import TempTransaction

class Trc20DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trc20Data
        fields = ['contract_address', 'count']
        
class TransactionDataSerializer(serializers.ModelSerializer):
    class Meta:
      model = TransactionData
      fields = '__all__'

class TransferDataSerializer(serializers.ModelSerializer):
    class Meta:
      model = TransferData
      fields = '__all__'

class TempTransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = TempTransaction
    fields = '__all__'