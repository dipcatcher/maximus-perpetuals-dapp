from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    self.link_1.text = self.item['period']
    
    

    # Any code you write here will run when the form opens.
    self.repeating_panel_1.set_event_handler('x-click-claim', self.claim_click)
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.item['period']<self.item['current_period']:
      self.data_grid_1.visible=not self.data_grid_1.visible
      #self.data_grid_1.remove_from_parent()
      #self.data_grid_1.foreground='black'
      self.repeating_panel_1.items=self.item['claimable']
      #alert(self.data_grid_1, large=True)
    else:
      Notification('Check back for rewards once Year {} ends.'.format(self.item['period'])).show()
  
  def claim_click(self,period, ticker, stake_id, **event_args):
    print('srowtemplat5')
    print(self.parent.__name__)
    print(self.parent.parent.__name__)
    print(self.parent.parent.parent.__name__)
    print(self.parent.parent.parent.parent.__name__)
    self.parent.raise_event('x-claim-function', period=period, ticker=ticker, stake_id=stake_id)
    