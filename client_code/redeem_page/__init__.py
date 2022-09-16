from ._anvil_designer import redeem_pageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import time
class redeem_page(redeem_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    self.address = self.main.address
    self.pool_address = properties['pool_address']
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract=self.main.web3_wallet.connect_contracts(self.main.provider, self.pool_address)
        self.write_maxi_contract, self.write_hex_contract = self.main.web3_wallet.connect_contracts(self.main.signer, self.pool_address)
        self.refresh_redeem()
    except Exception as e:
      raise e
      Notification('You must connect to MetaMask to redeem HEX.').show()
    
  
  def refresh_redeem(self):
    cd = self.maxi_contract.getHexDay().toNumber()
    me = self.maxi_contract.RELOAD_PHASE_END().toNumber()
    ms = self.maxi_contract.RELOAD_PHASE_START().toNumber()
    se = self.maxi_contract.STAKE_END_DAY().toNumber()
    ss = self.maxi_contract.STAKE_START_DAY().toNumber()
    
    
    self.can_redeem = all([cd>=ms, cd<=me])
    self.column_panel_3_copy.visible=self.can_redeem
    self.label_redemption_message.visible= not self.can_redeem
    
    self.symbol = self.maxi_contract.symbol()
    self.name = self.maxi_contract.name()
    self.label_burn_header.text= "Burn {}".format(self.symbol)
    self.label_token_balance.text ="{} balance:".format(self.symbol)
    self.redemption_rate = float(self.maxi_contract.HEX_REDEMPTION_RATE().toNumber()/(10**8))
    self.label_redeem_header.text = "Redeem {:,.8f} HEX per {} burnt".format(self.redemption_rate,self.symbol)
    self.maxi_balance = self.maxi_contract.balanceOf(self.address).toNumber()
    self.hex_balance = self.hex_contract.balanceOf(self.address).toNumber()
    self.label_redeem_hex_balance.text = '{:.8f} ⬣'.format(int(self.hex_balance)/100000000) 
    self.link_maxi_balance.text = '{:.8f} {}'.format(int(self.maxi_balance)/100000000, self.main.mm['symbol'])
    self.link_max_maxi.text = "{} max".format(self.main.mm['symbol'])
    
    # Any code you write here will run when the form opens.

  def button_redeem_hex_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.address is not None:
      if self.redeem_units <= float(self.maxi_balance):
        event_args['sender'].text=event_args['sender'].text.replace('REDEEM', "REDEEMING")
        current_maxi = self.maxi_balance
        anvil.js.await_promise(self.write_maxi_contract.redeemHEX(self.redeem_units))
        while current_maxi==self.maxi_contract.balanceOf(self.address).toNumber():
          time.sleep(.5)
          print('waiting')
          print(current_maxi, self.maxi_contract.balanceOf(self.address).toNumber())
        #self.call_js('redeemHEX', self.redeem_units, self.address)
        self.refresh_redeem()
        self.button_redeem_hex.text="REDEEM HEX"
        self.text_box_redeem_maxi.text = 0
        self.text_box_redeem_maxi_change()
      else:
        Notification('Insufficient {}.'.format(self.symbol)).show()
        self.refresh_redeem()
    else:
      Notification('Please connect MetaMask to Ethereum Mainnet.').show()

  def text_box_redeem_maxi_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.text_box_redeem_maxi.text in ['', None, 0]:
      self.button_redeem_hex.text='REDEEM HEX'
      self.button_redeem_hex.enabled = False
      self.units=0
    else:
      self.button_redeem_hex.text = 'REDEEM {:.8f} HEX'.format(self.text_box_redeem_maxi.text*self.redemption_rate)
      raw_units = float(self.text_box_redeem_maxi.text)
      self.redeem_units = int(raw_units*100000000)
      self.button_redeem_hex.enabled=True

  def link_max_maxi_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.text_box_redeem_maxi.text=float(float(self.maxi_balance)/100000000)
    self.text_box_redeem_maxi_change(sender=self.text_box_redeem_maxi)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.write_maxi_contract.endStakeHEX(0,605346)

  def button_end_stake_click(self, **event_args):
    """This method is called when the button is clicked"""
    from ..manage_test import manage_test
    alert(manage_test(write_contract = self.write_maxi_contract, pool_address=self.pool_address, read_contract=self.maxi_contract))







