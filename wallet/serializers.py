from rest_framework import serializers
from .models import Trc20Data

class Trc20DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trc20Data
        fields = ['contract_address', 'count']
