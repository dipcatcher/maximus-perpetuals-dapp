from ._anvil_designer import diamond_handsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
try:
  from anvil.js.window import ethers, ethereum, Web3
except:
  pass
'''
GLOBAL_AMOUNT_STAKED()
PERPETUAL_POOL_ADDRESS()
REWARD_BUCKET_ADDRESS()
STAKE_REWARD_DISTRIBUTION_ADDRESS()
TEAM_CONTRACT_ADDRESS()
TICKER_SYMBOL()
USER_AMOUNT_STAKED(_address)
calculatePenalty(amount_uint256)
deployRewardBucketContract()
deployStakeRewardDistributionContract()
earlyEndStakeToken(stakeID_uint256, amount_uint256)
endCompletedStake(stakeID_uint256, amount_uint256)
extendStake(stakeID_uint256)
getAddressPeriodEndTotal(staker_address_address, period_uint256, stakeID_uint256)
getCurrentPeriod()
getglobalStakedTokensPerPeriod(period_uint256)
globalStakedTokensPerPeriod(_uint256)
isStakingPeriod()

'''

def get_contract_data(provider, ticker):
  DH_CONTRACT_ABI = [{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EarlyEndStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EndExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"ExtendStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"RestakeExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"current_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"},{"indexed":False,"internalType":"bool","name":"is_initial","type":"bool"}],"name":"Stake","type":"event"},{"inputs":[],"name":"GLOBAL_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERPETUAL_POOL_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_BUCKET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_REWARD_DISTRIBUTION_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TEAM_CONTRACT_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TICKER_SYMBOL","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"USER_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"calculatePenalty","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deployRewardBucketContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"deployStakeRewardDistributionContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"earlyEndStakeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"endCompletedStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"extendStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker_address","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getAddressPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"current_period","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"period","type":"uint256"}],"name":"getglobalStakedTokensPerPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"globalStakedTokensPerPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isStakingPeriod","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"joinClub","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"restakeExpiredStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakes","outputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"stake_expiry_period","type":"uint256"},{"internalType":"bool","name":"initiated","type":"bool"}],"stateMutability":"view","type":"function"}]
  
  DH_ADDRESSES = {"BASE":"0xd0859C292Ce9aF524640B6AB621b9E22C01abF9E", 
                  "TRIO":"", 
                  "LUCKY":"", 
                  "DECI":""}
  dh_contract= ethers.Contract(DH_ADDRESSES[ticker],DH_CONTRACT_ABI,provider)
  a='''DH_CONTRACT_ADDRESS
  
  RB_CONTRACT_ABI
  RB_CONTRACT_ADDRESS
  
  RDCA_CONTRACT_ABI
  RDCA_CONTRACT_ADDRESS'''
  return dh_contract


class diamond_hands(diamond_handsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.pool_address = properties['pool_address']
    self.main = properties['main']
    self.label_1.text=self.pool_address
    self.ticker=self.main.drop_down_1.selected_value.split(' ')[1]
    self.dh_contract = get_contract_data(self.main.provider, self.ticker)
    alert("{:,.1f}".format(int(self.dh_contract.globalStakedTokensPerPeriod(1).toString())/(10**8)))
    # Any code you write here will run when the form opens.
  def refresh_page(self):
    self.team_balance =int(self.base_contract.balanceOf(self.address).toString())
    self.label_team_balance.text = '{:,.8f} ❇️'.format(int(self.team_balance)/100000000)
    self.team_staked = int(self.dh_contract.USER_AMOUNT_STAKED(self.address).toString())
    self.label_team_staked.text = '{:,.8f} ❇️'.format(int(self.team_staked)/100000000)
    self.team_supply = self.base_contract.totalSupply().toString()
    self.label_total_liquid.text = '{:,.8f} ❇️'.format(int(self.team_balance)/100000000)
    self.team_staked_total = self.dh_contract.GLOBAL_AMOUNT_STAKED().toString()
    self.label_total_staked.text = '{:,.8f} ❇️'.format(int(self.team_staked_total)/100000000)
    self.current_period = int(self.team_contract.getCurrentPeriod().toNumber())
   
    
    y=(int(1+(self.current_period+1)/2))
    last_day = self.base_contract.RELOAD_PHASE_END().toNumber()
    current_day = self.base_contract.getHexDay().toNumber()
    
    days_remaining = (last_day-current_day)+1
    deadline = datetime.datetime.utcnow().date()+ datetime.timedelta(days=days_remaining)
    self.label_stake_deadline.text = 'Stake before {} to earn rewards from Staking Year {}'.format(deadline.strftime('%m/%d/%Y @ %H:%M UTC'), y)
   
    
    year_text=  "Year {}".format(y)
    self.label_next_year.text = year_text
    #self.label_stake_deadline.text ="calculate days remaining" # base_contract.STAKE_START_DAY - base_contract.getHexDay()
    self.next_staking_period = self.current_period +1 if self.current_period%2==0 else self.current_period+2
    self.label_global_amount_staked.text = "{:,.1f}".format(int(self.dh_contract.globalStakedTokensPerPeriod(self.next_staking_period).toString())/(10**8))
    self.column_panel_stake_list.clear()
    self.column_panel_stake_list.add_component(stake_list(main=self.main, stake_page=self))
    # Any code you write here will run when the form opens.