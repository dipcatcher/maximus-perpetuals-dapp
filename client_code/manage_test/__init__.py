from ._anvil_designer import manage_testTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class manage_test(manage_testTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.init_components(**properties)
    self.label_1.text=properties['pool_address']
    self.write_contract = properties['write_contract']
    self.read_contract = properties['read_contract']
    ms = self.read_contract.RELOAD_PHASE_START().toNumber()
    me = self.read_contract.RELOAD_PHASE_END().toNumber()
    ss = self.read_contract.STAKE_START_DAY().toNumber()
    se = self.read_contract.STAKE_END_DAY().toNumber()
    h=self.read_contract.getHexDay().toNumber()
    self.label_2.text="current day: {}\nmint start day: {} mint end day:{}\nstake start day: {} stake end day: {}".format(h,ms, me, ss, se)
    # Any code you write here will run when the form opens.

  def button_mint_hedron_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.write_contract.mintHedron(self.text_box_index.text, self.text_box_id.text)

  def button_end_stake_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.write_contract.endStakeHEX(self.text_box_index.text, self.text_box_id.text)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.write_contract.stakeHEX()



