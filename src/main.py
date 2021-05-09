from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os
from contract.SmartContract import SmartContract
import json
import time
class SmartContractExplorer:

    def __init__(self):
        #.env file SHOULD be loaded in the same path as this file
        load_dotenv()
        #Infura endpoint isn't really needed if you have a local geth or eth2 client running
        self.web3 = Web3(HTTPProvider(os.environ.get("INFURA_ENDPOINT")))
        #Doesn't necessarily have to be your address
        self.web3.eth.defaultAccount = Web3.toChecksumAddress(os.environ.get("ETH_ADDRESS"))
        self.contracts = {}

        #Contracts json file should be located outside this directory, however, you can change the path of where this program looks for it
        with open(os.path.join(os.path.dirname(__file__), '../contracts.json')) as json_contracts:
            #Each key should be the name of the contract and the value should be the corresponding address
            contracts_to_load = json.load(json_contracts)
            for key in contracts_to_load.keys():
                self.add_contract([key, contracts_to_load[key]])
                time.sleep(1) #Rate limit, can be removed/changed
            print("Loaded " + str(len(self.contracts)) + " contracts.")

    def add_contract(self, args):
        #First arg should be name of contract, second arg should be it's address
        if len(args) != 2:
            print("Invalid number of arguments.")
        else:
            smartContract = SmartContract(args[1], self.web3)
            if smartContract.hasLoaded:
                self.contracts[args[0]] = smartContract

    def checksum(self, args):
        #We don't wanna be handling anything other than checksum addresses
        if len(args) != 1:
            print("Invalid number of arguments.")
        else:
            try:
                return "Checksum equivalent: " + Web3.toChecksumAddress(args[0]) + "\n" + "Is checksum?: " + str(Web3.isChecksumAddress(args[0]))
            except ValueError:
                return "Invalid address supplied."

    def execute(self, command, args):
        if command in list(self.contracts.keys()):
            return self.contracts[command].execute(args = args)
        else:
            #Python doesn't have switch statements yet
            commands = {
                "help" : lambda : list(commands.keys()),
                "explore": lambda : self.add_contract(args),
                "contracts": lambda : list(self.contracts.keys()),
                "checksum" : lambda : self.checksum(args),
                "exit" : lambda : quit()
            }
            return commands.get(command, lambda : ["Invalid command."])



if __name__ == "__main__":
    explorer = SmartContractExplorer()
    while True:
        args = input("> ").split()
        command = args.pop(0)
        retval = explorer.execute(command, args)()
        if retval is not None:
            print(*retval, sep = "\n")

