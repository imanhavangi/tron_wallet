from django.shortcuts import render

import requests
from rest_framework import generics
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import TRX as SYMBOL
from typing import Optional
import json
from tronapi import Tron
from rest_framework.response import Response
from rest_framework import status


class WalletListCreateView(generics.ListCreateAPIView):
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

        private_key = request.data.get('private_key')
        address = request.data.get('address')
        
        print(private_key)
        print(address)

        # Initialize the Tron object
        tron = Tron()

        try:

            # Set your private key
            tron.private_key = private_key
            tron.default_address = address

            # Get the balance
            balance = tron.trx.get_balance()
        
            print(f'The balance is: {balance / 10 ** 6} TRX')
            
            return Response({
                "balance": balance / 10 ** 6,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
            return Response({
                "message": "Error",
            }, status=status.HTTP_400_BAD_REQUEST)