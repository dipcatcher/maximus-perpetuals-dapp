from ._anvil_designer import faucetTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class faucet(faucetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main = properties['main']
    self.button_1.text = 'get {} from faucet'.format(self.main.ticker)
    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.main.pool_contract_write.faucet(1000000000000)

