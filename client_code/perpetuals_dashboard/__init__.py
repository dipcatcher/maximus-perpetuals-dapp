from ._anvil_designer import perpetuals_dashboardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class perpetuals_dashboard(perpetuals_dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    self.pool_address = properties['pool_address']
    self.ticker = properties['ticker']
    self.address = self.main.address
    self.scalar= 10**8
    
    try:
      if self.main.provider is not None:
        self.pool_contract, self.hex_contract=self.main.web3_wallet.connect_contracts(self.main.provider, self.pool_address)
        self.write_pool_contract, self.write_hex_contract = self.main.web3_wallet.connect_contracts(self.main.signer, self.pool_address)
        self.refresh_page()
    except Exception as e:
      raise e
  def refresh_page(self):
    self.hex_treasury = int(self.hex_contract.balanceOf(self.pool_address).toString())/(10**8)
    self.label_treasury_value_hex.text = '{:,.3f} HEX'.format(self.hex_treasury)
    self.label_total_supply_header.text = "Total {} Supply".format(self.ticker)
    supply_raw = int(self.pool_contract.totalSupply().toString())
    supply_scaled = supply_raw/self.scalar
    self.base_price = 0.05
    self.label_total_token_supply.text = "{:,.1f} {}".format(supply_scaled, self.ticker)
    self.market_cap.text = "${:,.2f}".format(self.base_price*supply_scaled)
    self.hex_day = self.pool_contract.getHexDay().toNumber()
    sd = self.pool_contract.RELOAD_PHASE_START().toNumber()
    ed = self.pool_contract.RELOAD_PHASE_END().toNumber()
    self.label_reload_start.text = "HEX Day {}".format(sd)
    self.label_reload_end.text= "HEX Day {}".format(ed)
    self.label_current_day.text = "HEX Day {}".format(self.hex_day)
    self.label_total_treasury_hex.text='{:,.3f} HEX'.format(self.hex_treasury)
    self.label_pool_supply.text="{:,.1f} {}".format(supply_scaled, self.ticker)
    self.label_pool_contract_address.text=self.pool_address
    ss = self.pool_contract.STAKE_START_DAY().toNumber()
    today = datetime.datetime.utcnow().date()
    
    se = self.pool_contract.STAKE_END_DAY().toNumber()
    if ss == 0:
      ss = ed
      se = ss +self.pool_contract.STAKE_LENGTH().toNumber()
      
    days_til_end = se - self.hex_day
    days_from_start = self.hex_day-ss
    ssd =today -datetime.timedelta(days=days_from_start)
    sed = today + datetime.timedelta(days=days_til_end)
    self.label_stake_start.text = "HEX Day {}".format(ss)
    self.label_stake_end.text = "HEX Day {}".format(se)
    
    self.label_stake_start_date.text= ssd.strftime('%m/%d/%Y')
    self.label_stake_end_date.text= sed.strftime('%m/%d/%Y')
    # Any code you write here will run when the form opens.
