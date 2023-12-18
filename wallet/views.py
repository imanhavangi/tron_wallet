from django.shortcuts import render

import requests
from rest_framework import generics
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import TRX as SYMBOL
from typing import Optional
import json
# from tronapi import Tron
from rest_framework.response import Response
from rest_framework import status
from .models import TronAccount
from django.http import JsonResponse
from .models import Trc20Data
from .serializers import Trc20DataSerializer
from .models import TransactionData
from .serializers import TransactionDataSerializer

class CreateWallet(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        # Choose strength 128, 160, 192, 224 or 256
        STRENGTH: int = 160  # Default is 128
        # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
        LANGUAGE: str = "english"  # Default is english
        # Generate new entropy hex string
        ENTROPY: str = generate_entropy(strength=STRENGTH)
        # Secret passphrase for mnemonic
        PASSPHRASE: Optional[str] = None  # "meherett"
        hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
        hdwallet.from_entropy(
            entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
        )
        # Generate HD wallet and get Tron address, mnemonic, and private key
        hdwallet.from_path("m/44'/195'/0'/0/0")
        
        walletjson = hdwallet.dumps()
        
        tron_address = walletjson['addresses']['p2pkh']
        private_key = walletjson['private_key']
        
        return Response({
            "tron_address": tron_address,
            "private_key": private_key
        }, status=status.HTTP_201_CREATED)

class WalletBalance(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            url = "https://api.trongrid.io/wallet/getaccount"
            payload = {
                "address": request.data.get('address'),
                "visible": True
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if data == {}:
                return Response({
                    "balance": 0,
                }, status=status.HTTP_200_OK)
            
            try:
                tron_account = TronAccount.objects.create(
                    address=data["address"],
                    balance=data["balance"],
                    create_time=data["create_time"],
                    net_window_size=data["net_window_size"],
                    net_window_optimized=data["net_window_optimized"],
                )
                
                try:
                    return Response({
                        "balance": tron_account.balance,
                    }, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({
                        "message": f"Data Can't send: {e}",
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    "message": f"Data Can't save: {e}",
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": f"Data Can't recieve: {e}",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class AllContractBalance(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            url = f"https://api.shasta.trongrid.io/v1/accounts/{request.data.get('address')}"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            # print(data)
            trc20_data = data.get("data")[0].get("trc20")
            
            if data == {}:
                return Response({
                    []
                }, status=status.HTTP_200_OK)
            
            try:
                for item in trc20_data:
                    for contract_address, count in item.items():
                        Trc20Data.objects.create(contract_address=contract_address, count=int(count))
                trc20_data_object = Trc20Data.objects.all()
                serializer = Trc20DataSerializer(trc20_data_object, many=True)
                try:
                    return JsonResponse(serializer.data, safe=False)
                except Exception as e:
                    return Response({
                        "message": f"Data Can't send: {e}",
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    "message": f"Data Can't save: {e}",
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": f"Data Can't recieve: {e}",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllTransactions(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            url = f"https://api.shasta.trongrid.io/v1/accounts/{request.data.get('address')}/transactions/trc20"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            # print(data)
            transaction_data = data.get("data")
            print(transaction_data)
            
            if data == {}:
                return Response({
                    "balance": 0,
                }, status=status.HTTP_200_OK)
            
            try:
                for item in transaction_data:
                    transaction_id = item['transaction_id']
                    symbol = item['token_info']['symbol']
                    address = item['token_info']['address']
                    decimals = item['token_info']['decimals']
                    name = item['token_info']['name']
                    block_timestamp = item['block_timestamp']
                    _from = item['from']
                    _to = item['to']
                    _type = item['type']
                    value = item['value']
                    
                    if not TransactionData.objects.filter(transaction_id=transaction_id).exists():
                        TransactionData.objects.create(
                            transaction_id = transaction_id,
                            token_symbol = symbol,
                            token_address = address,
                            token_decimals = int(decimals),
                            token_name = name,
                            block_timestamp = block_timestamp,
                            from_address = _from,
                            to_address = _to,
                            transaction_type = _type,
                            value = value
                        )

                transaction_data_object = TransactionData.objects.all()
                serializer = TransactionDataSerializer(transaction_data_object, many=True)
                try:
                    return JsonResponse(serializer.data, safe=False)
                except Exception as e:
                    return Response({
                        "message": f"Data Can't send: {e}",
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    "message": f"Data Can't save: {e}",
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": f"Data Can't recieve: {e}",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)