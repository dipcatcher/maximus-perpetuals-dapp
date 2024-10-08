from ._anvil_designer import stake_listTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
try:
  from anvil.js.window import ethers, ethereum, Web3
except:
  pass
from ..stake_record_card import stake_record_card
class stake_list(stake_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    '''in MAIN: 
    self.dh_contract
    self.dh_contract_write
    self.pool_contract
    self.pool_contract_write
    self.reward_bucket_contract
    self.reward_bucket_contract_write
    self.srd_contract
    self.srd_contract_write'''
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    self.stake_page = properties['stake_page']
    #self.dh_contract, self.pool_contract, self.team_contract = self.stake_page.get_contract_data(self.main.provider, self.stake_page.ticker)
    self.dh_contract = self.main.dh_contract
    self.pool_contract = self.main.pool_contract
    self.team_contract = self.main.team_contract
    self.write_dh_contract =self.main.dh_contract_write
    
    self.write_pool_contract = self.main.pool_contract_write
    self.write_team_contract = self.main.team_contract_write
    self.refresh_page()
    
    
    '''try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract, self.team_contract, self.reward_contract , self.dh_contract=self.main.web3_wallet.connect_contracts(self.main.provider)
        
        self.write_maxi_contract, self.write_hex_contract, self.write_team_contract, self.write_reward_contract, self.write_dh_contract = self.main.web3_wallet.connect_contracts(self.main.signer)
        self.refresh_page()
    except Exception as e:
      raise e'''
  def get_stake_record_data(self, user, stakeID):
    stake_record = self.dh_contract.stakes(user, stakeID)
    d_stake_record = {}
    d_stake_record['address']=stake_record[0]
    d_stake_record['balance']=int(stake_record[1].toString())
    d_stake_record['stakeID']=stake_record[2].toNumber()
    d_stake_record['stake_expiry_period']=stake_record[3].toNumber()
    d_stake_record['initiated']=stake_record[4]
    print(d_stake_record)
    b = {}
    for m in range(d_stake_record['stakeID'],d_stake_record['stake_expiry_period']+1):
      
      b[m]=int(self.dh_contract.getAddressPeriodEndTotal(user, m, d_stake_record['stakeID']).toString())
      
    d_stake_record['stakedTokensPerPeriod'] = b
    d_stake_record['amount_actively_staked']=d_stake_record['balance']
    d_stake_record['current_period']=self.current_period
    return d_stake_record
  def refresh_page(self):
    self.current_period = self.pool_contract.getCurrentPeriod().toNumber()
    self.stake_records = []
    for n in range(self.current_period+3):
      
      stake_record = self.get_stake_record_data(self.address, n)
      if stake_record['initiated']:
        self.label_day.text='Your Stakes'
        self.stake_records.append(stake_record)
        self.column_panel_1.add_component(stake_record_card(stake_record=stake_record, team_contract=self.dh_contract, write_team_contract=self.write_dh_contract, address=self.address, read_reward_contract=self.main.srd_contract, write_reward_contract=self.main.srd_contract_write, main=self.main, stake_page=self.stake_page, dh_contract = self.dh_contract))
  
    
      
    # Any code you write here will run when the form opens.
