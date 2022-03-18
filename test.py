import json,os
from web3 import Web3
from price import *



directory = './abi/'

# connecting to pcs factory
filename = "fac.json"
file_path = os.path.join(directory, filename)
with open(file_path) as json_file:
    factoryAbi = json.load(json_file)


#connecting to pcs
lplp = "lp.json"
file_path = os.path.join(directory, lplp)
with open(file_path) as json_file:
    lpAbi = json.load(json_file)

web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))  # connecting to binance

abis = [{"inputs":[{"internalType":"address[]","name":"addresses","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
  


pcsFactoryContract ="0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"  #pancakeswap factory address

def get_pair(address):
    try:
        main_Token = web3.toChecksumAddress(address)
        wbnb = web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")
        contract = web3.eth.contract(address=pcsFactoryContract, abi=factoryAbi)  # connecting to pancakeswap factory
        pair_address = contract.functions.getPair(main_Token,wbnb).call()  # getting the pair address of tokens
        
        return pair_address
    
    except Exception as error:
        return f"Issue occured\n\n{error}"
    
def deci(address):
    try:
        contract = web3.eth.contract(address=address, abi=abis)
        dec = contract.functions.decimals().call()
        return dec
    except Exception:
        return "0"
def getPriceUsd(address):
    try:
        main_Token = web3.toChecksumAddress(address)
        pair = get_pair(main_Token) #getting pair address
    
        pcs = web3.eth.contract(abi=lpAbi, address=pair) # getting tokens in pcs
        dec = int(deci(main_Token))
        reserves = pcs.functions.getReserves().call() 
        reserve0 = reserves[0]/9
        reserve1  = reserves[1]/18
        price = reserve1/reserve0
        
  
        
        price_usd = float(price)*float(bnbprice())
        return "{0:.12f}".format(float(price_usd))
    except Exception as error:
        return f"issues:\n\n{error}"


mul = getPriceUsd("0x5ba0ca8334FB6c64f5F6470C282AA859C3A4fCa8")

print(mul)
