from ._anvil_designer import disclaimerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js.window
import anvil.js
try:
  from anvil.js.window import ethereum
  is_ethereum=True
except:
  is_ethereum=False


class disclaimer(disclaimerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.target=properties['target']

    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('x-close-alert', value=True)
    a = alert("Choose Network", buttons=[("Ethereum", True), ("PulseChain", False), ("ETHPOW", "ETHPOW"), ("ETHFAIR", "ETHFAIR")]) #, ("Testnet", None)]
    if a==True:
      chain_id = '0x1'
    elif a == False:
      chain_id = "0x171"
    elif a ==None:
      chain_id =  "0x7A69"
    elif a == "ETHPOW":
      chain_id = "0x2711"
    elif a == "ETHFAIR":
      chain_id = "0x7D44C"
    if is_ethereum:     
      try:
        a = ethereum.request({
                  'method': 'wallet_switchEthereumChain',
                  'params': [{ "chainId": chain_id }] #'0x1
              })
        anvil.js.await_promise(a)
      except:
        pass
      self.clear()
      open_form('Main', target=self.target, chain_id = chain_id)
    else:
      Notification('To use the dapp you must be on an etherem enabled browser, such as MetaMask.').show()
      try:
        
        open_form('Main_copy')
      except:
        pass
        
