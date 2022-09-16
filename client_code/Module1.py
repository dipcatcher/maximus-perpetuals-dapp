import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#
from anvil.js.window import ethers, ethereum
from .Main import Main
try:
  from anvil.js.window import ethers, ethereum
  is_ethereum=True
  open_form('Main')
except:
  #Notification('This dapp may only be used with a browser with MetaMask Wallet enabled.').show()
  is_ethereum=False
