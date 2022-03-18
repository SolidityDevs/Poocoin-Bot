from telegram.ext import *
from telegram import *
import telegram

from web3 import Web3
import json,requests,cryptonator,time,os
from classes import *
from pythonpancakes import PancakeSwapAPI

from price import *
ps = PancakeSwapAPI()





bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))


#---------------------------------------------------------------------------   
# import some important abi
abis = [{"inputs":[{"internalType":"address[]","name":"addresses","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
  

directory = './abi/'
filename = "fac.json"
file_path = os.path.join(directory, filename)
with open(file_path) as json_file:
    factoryAbi = json.load(json_file)


bolo = "joe.json"

file_path = os.path.join(directory, bolo)
with open(file_path) as json_file:
    joeRouter = json.load(json_file)
    
 
jok = "bal.json"   
file_path = os.path.join(directory, jok)
with open(file_path) as json_file:
    balance_abi = json.load(json_file)
    
lplp = "lp.json"

file_path = os.path.join(directory, lplp)
with open(file_path) as json_file:
    lpAbi = json.load(json_file)
    
    
client = Web3(Web3.HTTPProvider(bsc))


routerAddress = Web3.toChecksumAddress("0x10ED43C718714eb63d5aA57B78B54704E256024E")
factoryAddress = Web3.toChecksumAddress("0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73")

routerContract = client.eth.contract(address=routerAddress, abi=joeRouter)
factoryContract = client.eth.contract(address=factoryAddress, abi=factoryAbi)
   
"""
NAME AND SYMBOL
   
"""
def name_contract(address):
    address = Web3.toChecksumAddress(address) 
    contract = web3.eth.contract(address=address, abi=abis)
    name = contract.functions.name().call()
    return name


def symbol_contract(address):
  try:
      contract = web3.eth.contract(address=address, abi=abis)
      symbol = contract.functions.symbol().call()
      name = name_contract(address)
      lover = f"<b>ℹ️ {name} ({symbol})</b>"
      return lover
  except Exception:
      return ""
  
def sss(address):
  try:
      contract = web3.eth.contract(address=address, abi=abis)
      symbol = contract.functions.symbol().call()
      return symbol
  except Exception:
      return ""
#---------------------------------------------------------------
"""

SUPPLY OF THE CONTRACT

"""
def price_contract(address):
    dates = "%Y-%m-%d %H:%M:%S"
    query = """
    query
    {
      ethereum(network: bsc) {
        dexTrades(
        exchangeName: {in:["Pancake","Pancake v2"]},
        baseCurrency: {is: "%s"}
        quoteCurrency: {is: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"}
        options: {desc: ["block.height", "transaction.index"], limit: 1}
        ) {
        block {
            height
            timestamp {
            time(format: "%s")
            }
        }
        transaction {
            index
        }
        baseCurrency {
            symbol
        }
        quoteCurrency {
            symbol
        }
        quotePrice
       }
      }
    }
    """ % (address, dates)

    d = {'query': query, 'variables': {}}
    payload = json.dumps(d)
    url = "https://graphql.bitquery.io"
    headers = {
            'X-API-KEY': 'BQYxBh0DXYCwroM9PKnGS2tZXWDZhNEx',
            'Content-Type': 'application/json'
        }
    
    try:
        di = requests.request("POST", url, headers=headers, data=payload).json()['data']['ethereum']['dexTrades'][0]['quotePrice']
        pp = "{0:.15f}".format(float(di))
        bnb = bnbprice()
        price = float(pp)*float(bnb)
        pps = "{0:.12f}".format(float(price))
        return pps
    except Exception:
        try:
            pup = ps.tokens(address)['data']['price']
            return "{0:.12f}".format(float(pup))
        except Exception:
            return "0.0000"
          
 

def supply_contract(address):
    try:
        contract = web3.eth.contract(address=address, abi=abis)
        decimal = decimals_contract(address)
        c_name = float(contract.functions.totalSupply().call()/10 ** decimal)
        return c_name
    except Exception:
        return "0.0000"

def decimals_contract(address):
    try:
        contract = web3.eth.contract(address=address, abi=abis)
        dec = contract.functions.decimals().call()
        return dec
    except Exception:
        return "0"
    
    
def dead(address):
    try:
        contract = web3.eth.contract(address=address, abi=abis)
        decimal = decimals_contract(address)
        wal = Web3.toChecksumAddress("0x000000000000000000000000000000000000dEaD") 
        dead1 = float(contract.functions.balanceOf(wal).call({'from': address})/10 ** decimal)
        return dead1
    except Exception:
        return "0"
    
def main_supply(address):
    try:
        supply_coins = supply_contract(address)
        burn_coin = dead(address)
        supply = float(supply_coins)-float(burn_coin)
        return supply
    except Exception:
        return "0.0000"
    
#------------------------------------


def mcap_contract(address):
    try:
        token_supply = main_supply(address=address)
        token_price = price_contract(address=address)
        mcap = float(token_supply)*float(token_price)
        mcap = "{0:,.4f}".format(float(mcap))
        return mcap
    except Exception:
        return "0.0000"   

#------------------------------------------------------------------------------


def fetch_pair(inToken):
    
    weth_address = Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c") 
    pair = factoryContract.functions.getPair(inToken, weth_address ).call()
    pair_contract = web3.eth.contract(address=pair, abi=lpAbi)
    
    fees_tax = fees_contract(inToken)
    gas_fees = gas_contract(inToken)
    balance_check_contract = client.eth.contract(address=weth_address, abi=balance_abi)
    balance_now = balance_check_contract.functions.balanceOf(pair).call({'from': weth_address})
    liquiditys = web3.fromWei(balance_now, "ether")
    liquidity = "{:0,.4f}".format(liquiditys)
    lp = "${0:,.4f}".format(float(bnbprice())*float(liquidity))
    lover = f"<b>{liquidity} WBNB ({lp})</b>\n\n" \
            f"<b>{fees_tax}</b>\n" \
            f"<b>{gas_fees}</b>"
    return lover
  


unixtime = int(time.time())


#----------------------------------------------------------------------------------------------
def fees_contract(address):
  try:
    buy = requests.get(f"https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token={address}").json()
    buy_tax = buy["BuyTax"]
    sell_tax = buy["SellTax"]
    msg = f"Buy: {buy_tax}% || Sell: {sell_tax}%"
    return msg
  except Exception:
    return "0.0"
  
  
def gas_contract(address):
  try:
    buy = requests.get(f"https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token={address}").json()
    buy_gas = '{0:,}'.format(buy["BuyGas"])
    sell_gas = '{0:,}'.format(buy["SellGas"])
    msg = f"⛽️ Buy Gas: {buy_gas}\n⛽️ Sell Gas: {sell_gas}"
    return msg
  except Exception:
    return "0.0"




def refresh(update,context) -> None:
    query : CallbackQuery = update.callback_query
    texty = update.callback_query.data
    user = update.effective_chat.id
    
    elo = texty.split()
    query.answer()
    if len (elo) ==1:
        query.answer()
        address = Web3.toChecksumAddress(texty)
        text = query.edit_message_text(text="<b>Getting price</b>",parse_mode='html',disable_web_page_preview=True)
        start = Token(sss(address),symbol_contract(address),price_contract(address),mcap_contract(address),main_supply(address),fetch_pair(address))
        best = start.check()
        keymap = [[InlineKeyboardButton("🔸 Bscscan", url=f"https://bscscan.com/token/{address}#balances"),InlineKeyboardButton("💩 Chart",url=f"https://poocoin.app/tokens/{address}"),InlineKeyboardButton("🥞 PCS", url=f"https://pancakeswap.finance/swap#/swap?outputCurrency={address}")]]
        reply_markto = InlineKeyboardMarkup(keymap)
        text.edit_text(best,parse_mode="html",reply_markup=reply_markto,disable_web_page_preview=True)
        
    elif elo[0] == "del":
        id = int(elo[1])
        print(id)
        query.answer("Contract Deleted ✅")
        with open("./user.json","r") as popo:
            jk = json.load(popo)
        context.bot.deleteMessage (message_id = query.message.message_id,
                           chat_id = user)
        # checking user id
        for i in jk:
            if i['id'] == int(user):
                ci = i['ca']
                del ci[id]
                with open("./user.json", 'w') as json_file:
                    json.dump(jk, json_file, 
                                 indent=4,  
                               separators=(',',': '))
                
                

    
    
