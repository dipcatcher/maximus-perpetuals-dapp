import anvil.secrets
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
import os

#from web3.auto.infura import w3

@anvil.server.callable
def launch_record_results():
  for ticker in ['BASE', 'LUCKY', 'TRIO', 'DECI']:
    anvil.server.launch_background_task('record_results', ticker)
@anvil.server.background_task
@anvil.server.callable
def record_results(ticker):
  results = get_results(ticker)
  app_tables.dashboard.get(name=ticker).update(results=results)
  
@anvil.server.callable
def get_results(ticker):
  TEAM_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"declareSupportedTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"endStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"minter","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"current_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"penalty","type":"uint256"}],"name":"EndStake","type":"event"},{"inputs":[],"name":"finalizeMinting","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"d","type":"uint256"}],"name":"incrementTestDay","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"minter","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mintTEAM","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"prepareClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"rollForwardStakedTEAM","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"minter","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"bool","name":"is_roll_forward","type":"bool"}],"name":"Stake","type":"event"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"stakeTEAM","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"addressAmountStakedRunningTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"addressPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"amountUserRollForward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"user_address","type":"address"}],"name":"determine_penalty","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"didRecordPeriodEndBalance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"didUserClaim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ESCROW_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker_address","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"}],"name":"getAddressPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"current_period","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHexDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"},{"internalType":"uint256","name":"period","type":"uint256"}],"name":"getPeriodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getPoolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getSupportedTokens","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GLOBAL_TEAM_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"globalPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"IS_MINTING_ONGOING","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isStakingPeriod","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MYSTERY_BOX_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"periodAmountClaimed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"periodEndBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"periodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"periodStartBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"poolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_REWARD_DISTRIBUTION_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"supportedTokens","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TEAM_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"testcurrentDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
  TEAM_CONTRACT_ADDRESS = "0xcAcf8328D3E1e56E4060A8f9c7A4c09268D8D2a2"
      
  team_contract = w3.eth.contract(address=TEAM_CONTRACT_ADDRESS,
                                    abi=TEAM_ABI)
  pool_contract_address = team_contract.getSupportedTokens(ticker).toString()
  pool_abi=[{"inputs":[{"internalType":"uint256","name":"mint_duration","type":"uint256"},{"internalType":"uint256","name":"stake_duration","type":"uint256"},{"internalType":"address","name":"team_address","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"ticker","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeIndex","type":"uint256"},{"internalType":"uint40","name":"stakeIdParam","type":"uint40"}],"name":"endStakeHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"incrementPeriod","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeIndex","type":"uint256"},{"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"mintHedron","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"pledgeHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount_MAXI","type":"uint256"}],"name":"redeemHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stakeHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEndStaker","outputs":[{"internalType":"address","name":"end_staker_address","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHedronDay","outputs":[{"internalType":"uint256","name":"day","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHedronRedemptionRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHexDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHEXRedemptionRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMintingPhaseEndDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMintingPhaseStartDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getStakeEndDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getStakeStartDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
      
  hex_contract =w3.eth.contract(address=HEX_CONTRACT_ADDRESS,
                                    abi=HEX_ABI)
 
  maxi_contract =w3.eth.contract(address=pool_contract_address,
                                    abi=pool_abi)
  hedron_contract =w3.eth.contract(address=HEDRON_CONTRACT_ADDRESS,
                                    abi=HEDRON_ABI)
  
  results = {}
  liquid_hex = hex_contract.functions.balanceOf(MAXI_CONTRACT_ADDRESS).call()/units
  query='''{
  stakeStarts(first: 5, orderBy: stakeTShares, orderDirection: desc, where:{stakerAddr:"**"}) {
    stakeId
    stakeTShares
    stakedHearts
    startDay
    endDay
    stakedDays
  }
}'''.replace('**',pool_contract_address)
  url = 'https://api.thegraph.com/subgraphs/name/codeakk/hex'
  import requests
  import json
  r = requests.post(url, json={'query': query}).json()
  staked_hex = float(r['data']['stakeStarts'][0]['stakedHearts'])/(10**8)
  from .ServerModule3 import earnings_to_date
  print(r['data']['stakeStarts'][0])
  start=maxi_contract.functions.getStakeStartDay().call()
  end=maxi_contract.functions.getHexDay().call()
  t_shares = float(r['data']['stakeStarts'][0]['stakeTShares'])
  principal = staked_hex
  
  earned_hex = earnings_to_date(start, end, t_shares,principal)
  print(earned_hex)
  results['Total HEX']=liquid_hex+earned_hex
  
  scalar = results['Total HEX']/(150000000)
  
  effective_hex = (3*results['Total HEX'])+(float(results['Total HEX'])*float(scalar)*float(.10))
  t_share_rate=int(anvil.http.request('https://hexvisionpublicapi.azurewebsites.net/api/StakingInfo',json=True)["shareRate"])/10
  
  
  results['T Share Potential']=t_shares
  
  results['MAXI Supply']=maxi_contract.functions.totalSupply().call()/units
 
  results['Hedron Mintable'] = 5555*results['T Share Potential']*1000*5
  
  results['Hedron Minted'] = hedron_contract.functions.balanceOf(MAXI_CONTRACT_ADDRESS).call()/(10**9)
  
  results['Mint Phase Start Day']=maxi_contract.functions.getMintingPhaseStartDay().call()
  
  results['Mint Phase End Day']=maxi_contract.functions.getMintingPhaseEndDay().call()
  
  results['Stake Start Day']=maxi_contract.functions.getStakeStartDay().call()
  
  results['Stake End Day']=maxi_contract.functions.getStakeEndDay().call()
  
  results['Current HEX Day']=maxi_contract.functions.getHexDay().call()
  
  results['HEX Principal'] = staked_hex
  results['HEX Accrued'] = earned_hex-staked_hex
  mh, mu = get_maxi_price()
  results['MAXI Price USD'] = mu
  results['MAXI Price HEX'] = mh
  results['Premium']=(mh-(results['Total HEX']/results['MAXI Supply']))/(results['Total HEX']/results['MAXI Supply'])
  
 
  print(results)
  return results

def get_maxi_price():
  pair_url='https://api.dexscreener.io/latest/dex/pairs/ethereum/0x2ae4517b2806b84a576c10f698d6567ce80a6490'
  pair_r = anvil.http.request(pair_url,json=True)
  print(pair_r['pair']["priceUsd"])
  
  return float(pair_r['pair']['priceNative']), float(pair_r['pair']["priceUsd"])
@anvil.server.callable
def maxi_balance(address, contract_address):
  
  maxi_contract =w3.eth.contract(address=contract_address,
                                    abi=MAXI_ABI)
  return int(maxi_contract.functions.balanceOf(address).call())/100000000



@anvil.server.http_endpoint('/getMaxiData')
def getMaxiData():
  data = app_tables.dashboard.get(name='dashboard')
  return data['results']