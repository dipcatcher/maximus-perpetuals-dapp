from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home

import datetime
import webbrowser
import time
try:
  from ..mint_page import mint_page
  from ..dashboard_page import dashboard_page
  from ..redeem_page import redeem_page
  from ..connect_page import connect_page
  from ..calculator_page import calculator_page
  from ..disclaimer import disclaimer
  from ..disclaimer_copy import disclaimer_copy
  from ..chain_interface import chain_interface
  from ..Main_copy import Main_copy
  from ..perpetuals_dashboard import perpetuals_dashboard
except:
  
  pass

import anvil.js
anvil.js.report_all_exceptions(False, reraise=False)
try:
  from anvil.js.window import ethers, ethereum
  is_ethereum=True
except:
  Notification('This dapp may only be used with a browser with MetaMask Wallet enabled.').show()
  is_ethereum=False


class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.address=None
    self.current=self.link_mint
    self.ongoing = True
    self.provider=None
    self.target = properties['target']
    for t in self.drop_down_1.items:
      if self.target in t:
        self.drop_down_1.selected_value=t
    if not is_ethereum:
      open_form('Main_copy')
    else:   
      try:
        self.provider = anvil.js.await_promise(ethers.providers.Web3Provider(ethereum))
        try:
          anvil.js.await_promise(ethereum.request({"method": 'eth_requestAccounts' }))
        except anvil.js.ExternalError as e:
          print(e)
        self.signer= self.provider.getSigner()
        self.address=self.signer.getAddress()
        
        self.web3_wallet =chain_interface()
        self.add_component(self.web3_wallet)
        try:
          self.button_connect_dapp_click()
        except:
          import time
          time.sleep(1)
          self.button_connect_dapp_click()
      except Exception as e:
        print(e)
      
      self.TEAM_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EarlyEndStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"EndExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"ExtendStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"minter","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"staking_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"RestakeExpiredStake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"staker","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"current_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stakeID","type":"uint256"},{"indexed":False,"internalType":"bool","name":"is_initial","type":"bool"}],"name":"Stake","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"ESCROW_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GLOBAL_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"IS_MINTING_ONGOING","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_PHASE_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MYSTERY_BOX_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"STAKE_REWARD_DISTRIBUTION_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"USER_AMOUNT_STAKED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"earlyEndStakeTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"endCompletedStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"extendStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"finalizeMinting","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker_address","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getAddressPeriodEndTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"string","name":"ticker","type":"string"},{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"getClaimableAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentPeriod","outputs":[{"internalType":"uint256","name":"current_period","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"},{"internalType":"uint256","name":"period","type":"uint256"}],"name":"getPeriodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getPoolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"getSupportedTokens","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"globalStakedTeamPerPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isStakingPeriod","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mintTEAM","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"periodRedemptionRates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"poolAddresses","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker","type":"string"}],"name":"prepareClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeID","type":"uint256"}],"name":"restakeExpiredStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"stakeTeam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakes","outputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"stakeID","type":"uint256"},{"internalType":"uint256","name":"stake_expiry_period","type":"uint256"},{"internalType":"bool","name":"initiated","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
      self.TEAM_CONTRACT_ADDRESS = "0xB7c9E99Da8A857cE576A830A9c19312114d9dE02"
      
      self.team_contract = ethers.Contract(self.TEAM_CONTRACT_ADDRESS,self.TEAM_ABI,self.provider)
      self.pool_address = self.team_contract.getPoolAddresses(self.drop_down_1.selected_value.split(' ')[1])
      self.drop_down_1_change(sender= self.drop_down_1)

  def button_connect_dapp_click(self, **event_args):
    a=False
    chain_id='0x1'
    self.is_connected = self.web3_wallet.connect_network(chain_id)
    if self.address is not None:
      abbr = '{}...{}'.format(self.address[0:5], self.address[-5:])
      self.button_connect_dapp.text=abbr
      self.button_connect_dapp.remove_from_parent()
      self.button_connect_dapp.background='#202F52'
      self.button_connect_dapp.foreground='#8E97CD'
      self.navbar_links.add_component(self.button_connect_dapp)
      self.panel_connect.clear()
      self.menu_click(sender=self.link_mint)
      
  def menu_click(self, **event_args):
    """This method is called when the link is clicked"""
    b = event_args['sender'].text
    self.current = event_args['sender']
    if b=='Mint':
      self.content_panel.clear()
      self.m = mint_page(main=self, pool_address=self.pool_address) if self.ongoing else Label(foreground='white', text='MAXI Minting Phase is over.')
      self.content_panel.add_component(self.m)
      

    if b=='Redeem':
      self.content_panel.clear()
      self.r = redeem_page(main=self, pool_address = self.pool_address) if self.ongoing else Label(foreground='white', text='MAXI Minting Phase is over.')
      self.content_panel.add_component(self.r)
      

    if b =='Dashboard':
      self.content_panel.clear()
      from ..offline_dashboard import offline_dashboard
      self.d = perpetuals_dashboard(main=self, pool_address=self.pool_address, ticker=self.ticker)#offline_dashboard(main=self) #dashboard_page(main=self)
      self.content_panel.add_component(self.d)
    if b=='Calculator':
      self.content_panel.clear()
      self.c=calculator_page()
      self.content_panel.add_component(self.c)

  def link_disclaimer_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(disclaimer_copy(),large=True, title='IMPORTANT DISCLAIMER')

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.ticker = self.drop_down_1.selected_value.split(' ')[1]
    self.pool_address = self.team_contract.getPoolAddresses(self.ticker)
    self.mm = app_tables.media.get(ticker=self.ticker)
    self.image_1.source = self.mm['logo']
    self.link_mint.icon=self.mm['logo'].url #"{}/token/logo/{}".format(anvil.server.get_api_origin(), self.ticker)
    print(self.link_mint.icon)
    self.menu_click(sender=self.current)
    print(self.pool_address)
    


  




  



