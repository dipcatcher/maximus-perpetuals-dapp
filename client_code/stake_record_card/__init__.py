from ._anvil_designer import stake_record_cardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
from anvil.js.window import ethers, ethereum
from ..early_end_stake import early_end_stake
class stake_record_card(stake_record_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.init_components(**properties)
    self.d_stake_record =properties["stake_record"]
    self.team_contract = properties['team_contract']
    self.dh_contract = properties['dh_contract']
    self.write_team_contract=properties['write_team_contract']
    self.read_reward_contract=properties['read_reward_contract']
    self.write_reward_contract=properties['write_reward_contract']
    self.address=properties['address']
    self.main=properties['main']
    self.stake_page=properties['stake_page']
    self.refresh_card()
    self.repeating_panel_2.set_event_handler('x-claim-function', self.claim_function)
  def refresh_card(self):
    d_stake_record=self.d_stake_record
    self.current_period = d_stake_record['current_period']
    buttons = []
    # if before or during stake expiry period
    print(self.current_period, d_stake_record['stake_expiry_period'])
    is_all_unstaked = d_stake_record['balance']==0
    is_before_expiry = self.current_period<=d_stake_record['stake_expiry_period']
    is_during_expiry = self.current_period==d_stake_record['stake_expiry_period']
    is_after_expiry = self.current_period>d_stake_record['stake_expiry_period']
    self.button_early_end_stake.visible = all([not is_all_unstaked, is_before_expiry])
    if self.button_early_end_stake.visible:
      self.button_early_end_stake.icon='fa:exclamation-triangle'
    self.button_extend_stake.visible = all([not is_all_unstaked, is_during_expiry])
    self.button_end_completed_stake.visible=all([not is_all_unstaked, is_after_expiry])
    self.button_restake_completed_stake.visible = all([not is_all_unstaked, is_after_expiry])
    self.button_claim_rewards.visible=True
    
    try:
      self.label_stake_end.text="{} Stake End".format(self.main.ticker)
    except:
      self.label_stake_end.text = "Stake Pool End"
    self.label_staked_amount.text="{0:,.2f}".format(float(self.d_stake_record['amount_actively_staked']/(10**8)))
    tt =[]
    for k,v in self.d_stake_record['stakedTokensPerPeriod'].items():
      if v>0:
        total = int(self.main.dh_contract.globalStakedTokensPerPeriod(k).toString())
        claimable_amounts = []
        for token in ['HEX','HDRN', 'MAXI', 'BASE', 'TRIO', 'LUCKY', 'DECI', 'TEAM']:
          claimable = int(self.main.reward_bucket_contract.getClaimableAmount(self.address, k, token, self.d_stake_record['stakeID'])[0].toString())
          d = 9 if token =='HDRN' else 8
          if claimable>0:
            claimable_amounts.append({'stakeID':self.d_stake_record['stakeID'], "token":token, "claimable":float(claimable/(10**d)),'period':k, 'claimed':self.read_reward_contract.didUserStakeClaimFromPeriod(self.address,d_stake_record['stakeID'],k,token )})
        tt.append({'period':int((k+1)/2), 'amount':"{:,}".format(int(float(v/(10**8)))), 'total':"{:,}".format(int(float(total/(10**8)))), 'claimable':claimable_amounts, 'stakeID':self.d_stake_record['stakeID'], 'current_period':self.current_period})
        
        #self.label_stake_id.text="Stake ID: {}".format(self.d_stake_record['stakeID'])
    self.team_balance =int(self.main.pool_contract.balanceOf(self.address).toString())
    #self.label_team_balance.text = '{:.8f} ❇️'.format(int(self.team_balance)/100000000)
    self.team_staked = int(self.main.dh_contract.USER_AMOUNT_STAKED(self.address).toString())
    #self.label_team_staked.text = '{:.8f} ❇️'.format(int(self.team_staked)/100000000)
    self.team_supply = self.main.pool_contract.totalSupply().toString()
    #self.label_total_liquid.text = '{:.8f} ❇️'.format(int(self.team_supply)/100000000)
    self.team_staked_total = self.main.dh_contract.GLOBAL_AMOUNT_STAKED().toString()
    self.repeating_panel_2.items=tt
    print('rp')
    alert(tt)
  def menu_click(self, **event_args):
    
      t = event_args['sender']
      if t==self.button_early_end_stake:
        existing_TEAM = self.team_balance
        
        l = Label(text='Since you are committed to stake through period {} you will experience a 20% penalty on any {} you end stake now. Are you sure you want to end stake?'.format(int((self.d_stake_record['stake_expiry_period']+1)/2), self.main.ticker))
        _ = alert(l, title='Important Early End Stake Penalty Information', buttons=[('Yes', True), ('Cancel', False)])
        if _:
          tb = early_end_stake(main=self.main,team_balance=self.d_stake_record['amount_actively_staked']/(10**8))
          a = alert(tb, title='Enter Amount to End Stake', buttons=[('End Stake', True), ('Cancel', False)])
          if a:
            raw_units=float(tb.raw_amount)
            print(self.d_stake_record['stakeID'])
            print(raw_units)
            anvil.js.await_promise(self.main.dh_contract_write.earlyEndStakeToken(self.d_stake_record['stakeID'],int(raw_units*100000000)))
            
            while existing_TEAM==int(ethers.Contract(self.main.dh_contract.PERPETUAL_POOL_ADDRESS(), self.main.POOL_ABI, self.main.provider).balanceOf(self.address).toString()):
              print(existing_TEAM, int(ethers.Contract(self.main.dh_contract.PERPETUAL_POOL_ADDRESS(), self.main.POOL_ABI, self.main.provider).balanceOf(self.address).toString()))
              time.sleep(1)
            self.stake_page.refresh_page()
      if t ==self.button_end_completed_stake:
        existing_TEAM = self.team_balance
        tb = TextBox(type='number')
        label = Label(foreground='grey',font_size=12,text='Available {}: {}'.format(self.main.ticker,int(self.d_stake_record['amount_actively_staked']/(10**8))))
        c = ColumnPanel()
        c.add_component(tb)
        c.add_component(label)
        a = alert(c, title='Enter Amount to End Stake', buttons=[('End Stake', True), ('Cancel', False)])
        if a:
          raw_units=float(tb.text)
        anvil.js.await_promise(self.main.dh_contract_write.endCompletedStake(self.d_stake_record['stakeID'],int(raw_units*100000000)))
        while existing_TEAM==int(self.main.pool_contract.balanceOf(self.address).toString()):
          time.sleep(1)
        self.stake_page.refresh_page()
      if t==self.button_extend_stake:
        
        tb = TextBox(type='number')
        a = alert(title='Are you sure you want to extend your stake into the next staking period?', buttons=[('Yes', True), ('Cancel', False)])
        if a:
          current_expiry = self.d_stake_record['stake_expiry_period']
          anvil.js.await_promise(self.main.dh_contract_write.extendStake(self.d_stake_record['stakeID']))
          while current_expiry==int(self.main.dh_contract.stakes(self.address, self.d_stake_record['stakeID'])[3].toString()):
            time.sleep(1)
          self.stake_page.refresh_page()
      if t==self.button_restake_completed_stake:
        current_amount_staked = self.d_stake_record['balance']
        c =confirm('This will end your current stake and start a new one in the next period.',title='Are you sure you want to restake?')
        if c:
          anvil.js.await_promise(self.main.dh_contract_write.restakeExpiredStake(self.d_stake_record['stakeID']))
          while current_amount_staked>0:
            time.sleep(1)
          self.stake_page.refresh_page()
      if t==self.button_claim_rewards:
        print(t)
        self.data_grid_2.visible=True
        self.repeating_panel_2.visible=True
      
      #self.refresh_card()
        
      # Any code you write here will run when the form opens.

  
  def claim_function(self, period, ticker, stake_id, **event_args):
    print('claim function')
    anvil.js.await_promise(self.main.srd_contract_write.claimRewards(period, ticker, stake_id))
    while not self.main.srd_contract.didUserStakeClaimFromPeriod(self.address,stake_id, period,ticker ):
      time.sleep(1)
    self.refresh_card()
    # check if the did claim value is set to true, then we need to refresh the view

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    pass

    
