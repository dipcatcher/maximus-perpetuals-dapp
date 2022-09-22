from ._anvil_designer import early_end_stakeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class early_end_stake(early_end_stakeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main = properties['main']
    self.raw_amount = 0
    self.team_balance= properties['team_balance']
    self.label_amount_staked.text = "{} {}".format(self.team_balance, self.main.ticker)
    # Any code you write here will run when the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if event_args['sender'].text not in ['', None, 0]:
      self.raw_amount=float(event_args['sender'].text)
      penalty=self.raw_amount/5
      self.label_1.text = "Early Ending {amount} {ticker} results in a {penalty} penalty. You will receive {result} {ticker} and the penalized amount will be sent to the Diamond Hands Reward Bucket.".format(
        amount= self.raw_amount, penalty = penalty, result = self.raw_amount-penalty, ticker = self.main.ticker
      )

  def link_max_team_click(self, **event_args):
    """This method is called when the link is clicked"""
    
    self.text_box_1.text=self.team_balance
    self.text_box_1_change(sender=self.text_box_1)

  

    
    
    

