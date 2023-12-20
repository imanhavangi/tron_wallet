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
from .models import TransferData
from .models import TransactionData
from .serializers import TransferDataSerializer
from .serializers import TransactionDataSerializer
from tronapi import Tron
import base64


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
        print(walletjson)
        
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
        TransactionData.objects.all().delete()
        try:
            url = f"https://api.shasta.trongrid.io/v1/accounts/{request.data.get('address')}/transactions"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            # print(data)
            transaction_data = data.get("data")
            
            if data == {}:
                return Response({
                    "balance": 0,
                }, status=status.HTTP_200_OK)
            
            try:
                for item in transaction_data:
                    contractRet = item['ret'][0]['contractRet']
                    fee = item['ret'][0]['fee']
                    signature = item['signature'][0]
                    txID = item['txID']
                    net_usage = item['net_usage']
                    raw_data_hex = item['raw_data_hex']
                    net_fee = item['net_fee']
                    energy_usage = item['energy_usage']
                    blockNumber = item['blockNumber']
                    block_timestamp = item['block_timestamp']
                    energy_fee = item['energy_fee']
                    energy_usage_total = item['energy_usage_total']
                    # amount = item['raw_data']['contract'][0]['parameter']['value']['amount']
                    owner_address = item['raw_data']['contract'][0]['parameter']['value']['owner_address']
                    # to_address = item['raw_data']['contract'][0]['parameter']['value']['to_address']
                    type_url = item['raw_data']['contract'][0]['parameter']['type_url']
                    _type = item['raw_data']['contract'][0]['type']
                    ref_block_bytes = item['raw_data']['ref_block_bytes']
                    ref_block_hash = item['raw_data']['ref_block_hash']
                    expiration = item['raw_data']['expiration']
                    timestamp = item['raw_data']['timestamp']
                    
                    if not TransactionData.objects.filter(txID=txID).exists():
                        TransactionData.objects.create(
                            contractRet = contractRet,
                            fee = fee,
                            signature = signature,
                            txID = txID,
                            net_usage = net_usage,
                            raw_data_hex = raw_data_hex,
                            net_fee = net_fee,
                            energy_usage = energy_usage,
                            blockNumber = blockNumber,
                            block_timestamp = block_timestamp,
                            energy_fee = energy_fee,
                            energy_usage_total = energy_usage_total,
                            # amount = amount,
                            owner_address = owner_address,
                            # to_address = to_address,
                            type_url = type_url,
                            _type = _type,
                            ref_block_bytes = ref_block_bytes,
                            ref_block_hash = ref_block_hash,
                            expiration = expiration,
                            timestamp = timestamp
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
            
class AllContractTransfers(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        TransferData.objects.all().delete()
        try:
            contract_address = request.data.get('contract_address', None)
            if contract_address:
                url = f"https://api.shasta.trongrid.io/v1/accounts/{request.data.get('address')}/transactions/trc20?contract_address={request.data.get('contract_address')}"
            else:
                url = f"https://api.shasta.trongrid.io/v1/accounts/{request.data.get('address')}/transactions/trc20"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            transfer_data = data.get("data")
            
            if data == {}:
                return Response({
                    "balance": 0,
                }, status=status.HTTP_200_OK)
            
            try:
                for item in transfer_data:
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
                    if not TransferData.objects.filter(transaction_id=transaction_id).exists():
                        TransferData.objects.create(
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

                transfer_data_object = TransferData.objects.all()
                serializer = TransferDataSerializer(transfer_data_object, many=True)
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
            
class CreateTransaction(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            tron = Tron(
                full_node="https://api.shasta.trongrid.io",
                solidity_node="https://api.shasta.trongrid.io",
                event_server="https://api.shasta.trongrid.io",
            )
            # tron.private_key = request.data.get('private_key')
            tron_address = request.data.get('tron_address')
            to_address = request.data.get('to_address')
            amount = float(request.data.get('amount'))
            
            sender_balance = tron.trx.get_balance(tron_address)
            # estimated_fee = tron.trx.get_transaction_fee({})
            # total_amount = amount + estimated_fee['fee']
            # if sender_balance < total_amount:
            #     return {'error': 'Insufficient balance'}
            
            transaction = tron.transaction_builder.send_transaction(to_address, amount, tron_address)
            if transaction:
                return Response({
                    "message": "Transaction Successful",
                    "transaction": dict(transaction)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Transaction Failed",
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": f"Data Can't recieve: {e}",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class TransactionInfo(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            tron = Tron(
                full_node="https://api.shasta.trongrid.io",
                solidity_node="https://api.shasta.trongrid.io",
                event_server="https://api.shasta.trongrid.io",
            )
            txID = request.data.get('txID')
            print(txID)
            info = tron.trx.get_transaction_info(txID)
            print(info)
            if info:
                return Response({
                    "message": "Successfully fetched data",
                    "data": dict(info),
                    })
            else:
                return Response({
                    "message": "failed to fetch data",
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": f"Data Can't recieve: {e}",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class CalculateFee(generics.ListCreateAPIView):
    def free_net_usage(request):
        url = "https://api.trongrid.io/wallet/getaccountresource"
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
        try:
            return int(data["freeNetLimit"])-int(data['freeNetUsed'])
        except:
            return 0
    def get(self, request, *args, **kwargs):
        try:
            # byte_array = base64.b16decode(request.data.get('rawdatahex'))
            print('sa')
            byte_array_length = len(request.data.get('rawdatahex'))
            bandwidth_points_balance = CalculateFee.free_net_usage(request)
            bandwidth_points_consumption = byte_array_length
            bandwidth_points_unit_price = 1000 # SUN
            transaction_fee = max(0, bandwidth_points_consumption - bandwidth_points_balance) * bandwidth_points_unit_price / 1000000 # TRX
            try:
                return Response({
                    "message": "Successfully get fee",
                    "fee": transaction_fee,
                    })
            except Exception as e:
                return Response({
                    "message": f"Data Can't send: {e}",
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": f"Data Can't recieve: {e}",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)