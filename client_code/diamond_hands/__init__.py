from ._anvil_designer import diamond_handsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..stake_list import stake_list
try:
  from anvil.js.window import ethers, ethereum, Web3
except:
  pass
import time
import datetime


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



class diamond_hands(diamond_handsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    h = HtmlTemplate(
      html="""<p><span style="font-size:26px"><strong>Maximus</strong> Diamond Hands</span></p>"""
    )
    self.flow_panel_2.add_component(h)
    self.pool_address = properties['pool_address']
    print('pool:')
    print(self.pool_address)
    self.main = properties['main']
    self.ticker=self.main.drop_down_1.selected_value.split(' ')[1]
    
    self.address =self.main.address
    self.init_components(**properties)
    self.rich_text_2.content = self.rich_text_2.content.format(ticker=self.ticker)
    self.label_5.text="{} Staking Rules".format(self.ticker)
    self.rich_text_2_copy.content=self.rich_text_2_copy.content.format(ticker=self.ticker)
  def form_show(self, **event_args):
    self.main.build_connection()
    self.dh_contract, self.pool_contract, self.team_contract = self.get_contract_data(self.main.provider, self.ticker)
    
    self.refresh_page()
    #alert("{:,.1f}".format(int(self.dh_contract.globalStakedTokensPerPeriod(1).toString())/(10**8)))
    # Any code you write here will run when the form opens.
  def get_contract_data(self, provider, ticker):
    '''DH_CONTRACT_ABI = [{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EarlyEndStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EndExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"ExtendStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"RestakeExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"current_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"},{"indexed":False,"internalType":"bool","name":"is_initial","type":"bool"}],"name":"Stake","type":"event"},{"inputs":[],"name":"GLOBAL_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERPETUAL_POOL_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_BUCKET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_REWARD_DISTRIBUTION_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TEAM_CONTRACT_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TICKER_SYMBOL","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"USER_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"calculatePenalty","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deployRewardBucketContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"deployStakeRewardDistributionContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"earlyEndStakeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"endCompletedStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"extendStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker_address","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getAddressPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"current_period","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"period","type":"uint256"}],"name":"getglobalStakedTokensPerPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"globalStakedTokensPerPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isStakingPeriod","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"joinClub","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"restakeExpiredStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakes","outputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"stake_expiry_period","type":"uint256"},{"internalType":"bool","name":"initiated","type":"bool"}],"stateMutability":"view","type":"function"}]
    POOL_ABI=[{"inputs":[{"internalType":"uint256","name":"initial_mint_duration","type":"uint256"},{"internalType":"uint256","name":"stake_duration","type":"uint256"},{"internalType":"uint256","name":"reload_duration","type":"uint256"},{"internalType":"address","name":"team_address","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"ticker","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"CURRENT_PERIOD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CURRENT_STAKE_PRINCIPAL","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"END_STAKER","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"HEX_REDEMPTION_RATE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RELOAD_PHASE_DURATION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RELOAD_PHASE_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RELOAD_PHASE_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_END_DAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_IS_ACTIVE","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_LENGTH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_START_DAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TEAM_CONTRACT_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeIndex","type":"uint256"},{"internalType":"uint40","name":"stakeIdParam","type":"uint40"}],"name":"endStakeHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEndStaker","outputs":[{"internalType":"address","name":"end_staker_address","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHexDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeIndex","type":"uint256"},{"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"mintHedron","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"pledgeHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"redeemHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stakeHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
    TEAM_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EarlyEndStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EndExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"ExtendStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"minter","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"RestakeExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"current_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"},{"indexed":False,"internalType":"bool","name":"is_initial","type":"bool"}],"name":"Stake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"ESCROW_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GLOBAL_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"IS_MINTING_ONGOING","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MYSTERY_BOX_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_REWARD_DISTRIBUTION_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"USER_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"earlyEndStakeTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"endCompletedStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"extendStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"finalizeMinting","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker_address","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getAddressPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"string","name":"ticker","type":"string"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getClaimableAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"current_period","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"},{"internalType":"uint256","name":"period","type":"uint256"}],"name":"getPeriodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getPoolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getSupportedTokens","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"globalStakedTeamPerPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isStakingPeriod","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mintTEAM","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"periodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"poolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"prepareClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"restakeExpiredStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"stakeTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakes","outputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"stake_expiry_period","type":"uint256"},{"internalType":"bool","name":"initiated","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
            
    
    dh_contract= ethers.Contract(self.DH_ADDRESSES[ticker],self.DH_CONTRACT_ABI,provider)
    pool_contract = ethers.Contract(dh_contract.PERPETUAL_POOL_ADDRESS(), POOL_ABI, provider)
    team_contract = ethers.Contract(dh_contract.TEAM_CONTRACT_ADDRESS(), TEAM_ABI, provider)
    a=
    
    RB_CONTRACT_ABI
    RB_CONTRACT_ADDRESS
    
    RDCA_CONTRACT_ABI
    RDCA_CONTRACT_ADDRESS'''
    return self.main.dh_contract, self.main.pool_contract, self.main.team_contract

  def refresh_page(self):
    
    self.pool_balance =int(self.pool_contract.balanceOf(self.address).toString())
    self.label_team_balance.text = '{:,.8f} ❇️'.format(int(self.pool_balance)/100000000)
    self.team_staked = int(self.dh_contract.USER_AMOUNT_STAKED(self.address).toString())
    self.label_team_staked.text = '{:,.8f} ❇️'.format(int(self.team_staked)/100000000)
    self.team_supply = self.pool_contract.totalSupply().toString()
    #self.label_total_liquid.text = '{:,.8f} ❇️'.format(int(self.pool_balance)/100000000)
    self.team_staked_total = self.dh_contract.GLOBAL_AMOUNT_STAKED().toString()
    #self.label_total_staked.text = '{:,.8f} ❇️'.format(int(self.team_staked_total)/100000000)
    self.current_period = int(self.pool_contract.getCurrentPeriod().toNumber())
    
   
    
    y=(int(1+(self.current_period+1)/2))
    last_day = self.pool_contract.RELOAD_PHASE_END().toNumber()
    current_day = self.pool_contract.getHexDay().toNumber()
    
    days_remaining = (last_day-current_day)+1
    deadline = datetime.datetime.utcnow().date()+ datetime.timedelta(days=days_remaining)
    self.label_stake_deadline.text = 'Stake before {} to earn rewards from Stake Period {}'.format(deadline.strftime('%m/%d/%Y @ %H:%M UTC'), y)
   
    
    year_text=  "#{}".format(y)
    self.label_next_year.text = year_text
    #self.label_stake_deadline.text ="calculate days remaining" # pool_contract.STAKE_START_DAY - pool_contract.getHexDay()
    self.next_staking_period = self.current_period +1 if self.current_period%2==0 else self.current_period+2
    self.label_global_amount_staked.text = "{:,.1f}".format(int(self.dh_contract.globalStakedTokensPerPeriod(self.next_staking_period).toString())/(10**8))
    self.column_panel_stake_list.clear()
    self.column_panel_stake_list.add_component(stake_list(main=self.main, stake_page=self))
    # Any code you write here will run when the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.text_box_1.text in ['', None, 0]:
      self.button_2.text='Stake {}'.format(self.ticker)
      self.button_2.enabled = False
      self.column_panel_2.visible=False
      self.units=0
    else:
      self.button_2.text = 'Stake {} {}'.format(self.text_box_1.text, self.ticker)
      raw_units = float(self.text_box_1.text)
      self.units = int(raw_units*100000000)
      try:
        self.check_approval()
      except Exception as e:
        raise e
        Notification('You must first connect to MetaMask.').show()
        return False
      if self.units>self.approved_pool:
        self.column_panel_2.visible=True
        self.label_permission.visible=True
        self.link_3.visible=True
        self.column_panel_2.role='card'
        self.button_2.enabled = False
        self.label_permission.text="First, {} needs your permission to interact with {} of your {}.".format("Diamond Hands Contract",raw_units, self.ticker)
        self.button_2_copy.text = 'APPROVE {} {}'.format(raw_units, self.ticker)
        
      else:
        self.column_panel_2.visible=False
        self.button_2.enabled = True

  def check_approval(self):
    
    self.approved_pool = int(self.pool_contract.allowance(self.main.address, self.main.dh_address).toNumber() or 0)
    
    
    return self.approved_pool

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    raw_units = self.units
    self.button_2.enabled=False
    self.button_2.text='Staking {} {}'.format(raw_units/(10**8), self.ticker)
    existing_TEAM = self.pool_balance
    anvil.js.await_promise(self.main.dh_contract_write.joinClub(raw_units))
    while existing_TEAM==int(self.main.pool_contract.balanceOf(self.address).toString()):
      time.sleep(1)
    self.button_2.enabled=False
    self.button_2.text='Stake {}'.format(self.ticker)
    self.text_box_1.text=None
    self.text_box_1_change(sender=self.text_box_1)
    #self.button_2_copy.enabled=True
    #self.button_2_copy.background='#246BFD'
    #self.button_2.foreground='white'
    #self.button_2_copy.icon=''
    self.refresh_page()

  def link_maxi_balance_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_max_team_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.text_box_1.text=self.pool_balance/(10**8)
    self.text_box_1_change(sender=self.link_max_team)

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    if event_args['sender'].icon == 'fa:check':
      pass
    else:
      try:
        tokenSymbol = 'TEAM'
        tokenDecimals = 8
        tokenImage = 'https://perpetuals.anvil.app/_/api/token/logo/TEAM';

        from anvil.js.window import ethereum
        a = ethereum.request({
        'method': 'wallet_watchAsset',
        'params': {
          'type': 'ERC20', 
          'options': {
            'address': self.main.web3_wallet.TEAM_CONTRACT_ADDRESS, 
            'symbol': tokenSymbol, 
            'decimals': tokenDecimals, 
            'image': tokenImage, 
          },
        },
      })
        anvil.js.await_promise(a)
        
        event_args['sender'].icon = 'fa:check'
        event_args['sender'].text='TEAM Token Added'
      except Exception as e:
        print(e)
  def button_2_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    if 'APPROVE' in self.button_2_copy.text:
      
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVE", "APPROVING")
      self.button_2_copy.enabled=False
      self.approve_request(self.units)
    else:
      self.text_box_1_change()
  
  def approve_request(self, units):
    try:
      
      anvil.js.await_promise(self.main.pool_contract_write.approve(self.main.dh_address, units))
      
      while self.approved_pool<self.units:
        self.check_approval()
        time.sleep(1)
        
      #self.button_2.text='MINT {}'.format(self.symbol)
      
      #self.column_panel_2.visible=False
      self.label_permission.visible=False
      self.link_3.visible=False
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVING", "APPROVED")
      self.button_2_copy.background='green'
      self.column_panel_2.role=''
      self.button_2_copy.enabled=False
      self.button_2_copy.icon='fa:check'
      self.button_2.enabled=True
    except Exception as e:
      raise e
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVING", "APPROVE")
      self.text_box_1_change()

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    a='''Approvals are considered an industry standard across all decentralized finance smart contracts (like Uniswap, PancakeSwap, CowSwap etc.), and protect your wallet from being accessed by a smart contract without your permission. By design, smart contracts can’t access your tokens unless you approve access from your end. By ‘approving’ your tokens, you are give permission to the Maximus Diamond Hand smart contract to transact the amount that you approve. Read the contract code on etherscan to see exactly how the contract interacts with your tokens. Once the amount you approved is transacted, the approved amount gets automatically reset to 0.'''
    alert(Label(text=a), large=True)


  



  
    



  