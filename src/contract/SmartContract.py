from web3 import Web3
from web3.exceptions import InvalidAddress
from os import environ
import urllib
import urllib.request
import requests
import json
from utils.ParseArguments import parse_to_arg
import re

class SmartContract:
    
    def __init__(self, address, web3_instance):
        try:
            #Still need to write decompiler for contract bytecode, just use etherscan's API until then
            abi = requests.get(environ.get("ETHERSCAN_ABI_ENDPOINT") + address, proxies = urllib.request.getproxies()).json()["result"]
            try:
                self.contract = web3_instance.eth.contract(address = address, abi = abi)
            except InvalidAddress:
                #If you still want to use non checksum equivalent address, this will take care of it
                self.contract = web3_instance.eth.contract(address = Web3.toChecksumAddress(address), abi = abi)
            
            self.hasLoaded = True
        except Exception as e:
            self.hasLoaded = False
            print("Could not load " + address)
            print(e)
    
    def call_function(self, function_name):
        try:
            #Grabs function by name given
            function = self.contract.get_function_by_name(function_name)
            function_args = []

            #Parse string given arguments into valid arguments accepted by smart contract
            for arg in self.get_function_abi(function_name)['inputs']:
                input_arg = input(arg["name"] + ' ')
                function_args.append(parse_to_arg(input_arg, arg['type']))

            print("Calling Function: " + str(function(*function_args)))
            print("Function ABI: " + str(self.get_function_abi(function_name)))
            print("Gas Estimate: " + str(function(*function_args).estimateGas()))
            print(function(*function_args).call())
        except ValueError as e:
            print(e)
            print(function_name + " doesn't exist.")
        except TypeError as e:
            print(e)
            print("Invalid parameters for function.")

    def get_function_abi(self, function_name):
        return next(abi for abi in self.contract.abi if abi["name"] == function_name)


    def execute(self, args):
        contract_commands = {
            "functions": lambda : [re.findall(r'<Function (.+?)>', str(function))[0] for function in self.contract.all_functions()],
            "call" : lambda : self.call_function(function_name = args.pop(0)),
            "abi" : lambda : [json.dumps(self.contract.abi, indent=2)]
        }
        return contract_commands.get(args.pop(0), lambda : ["Invalid Smart Contract Command."])
