from ._anvil_designer import mint_pageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import time
import datetime
class mint_page(mint_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.main=properties['main']
    self.pool_address = properties['pool_address']
    self.address = self.main.address
    
    try:
      if self.main.provider is not None:
        self.maxi_contract, self.hex_contract=self.main.web3_wallet.connect_contracts(self.main.provider, self.pool_address)
        self.write_maxi_contract, self.write_hex_contract = self.main.web3_wallet.connect_contracts(self.main.signer, self.pool_address)
        self.refresh_mint()
    except Exception as e:
      raise e
    
  def refresh_mint(self):
    
    self.symbol = self.maxi_contract.symbol()
    self.label_maxi_balance_header.text = "{} balance:".format(self.symbol)
    self.button_2.text = "MINT {}".format(self.symbol)
    self.link_1_copy.text = "Add {} to Metamask".format(self.symbol)
    self.maxi_balance = self.maxi_contract.balanceOf(self.address).toNumber()
    self.hex_balance = self.hex_contract.balanceOf(self.address).toNumber()
    self.hex_day = self.maxi_contract.getHexDay().toNumber()
    self.minting_phase_end_day = self.maxi_contract.RELOAD_PHASE_END().toNumber()
    days_left = self.minting_phase_end_day-self.hex_day
    if days_left <0:
      self.column_panel_3.visible = False
      self.card_1.add_component(Label(text='Minting Phase is Over', foreground='white',align='center'))
    try:
      formatted_date = (datetime.datetime.utcnow().date() +datetime.timedelta(days=self.minting_phase_end_day-self.hex_day)).strftime('%Y-%m-%d 17:00')#2022-08-19 14:21
      html = """<script src="https://cdn.logwork.com/widget/countdown.js"></script>
      <a href="https://logwork.com/countdown-wsd9" class="countdown-timer" data-style="circles" data-timezone="America/Los_Angeles" data-textcolor="#ffffff" data-date="{}" data-digitscolor="#ffffff" data-unitscolor="#ffffff">Minting Deadline</a>""".format(formatted_date)
      h = HtmlTemplate(html=html)
      self.column_panel_countdown.clear()
      self.column_panel_countdown.add_component(h)
    except Exception as e:
      print(e)
    self.label_mint_duration.text= '{} Days Remaining'.format(days_left)
    self.link_hex_balance.text = '{:.8f} ⬣'.format(int(self.hex_balance)/100000000) 
    self.label_maxi_balance.text = '{:.8f} {}'.format(int(self.maxi_balance)/100000000, self.main.mm['symbol'])
    self.redemption_rate = float(self.maxi_contract.HEX_REDEMPTION_RATE().toNumber()/(10**8))
    self.label_headline.text = "Mint {:.8f} {} per HEX pledged".format(1/self.redemption_rate,self.symbol)
    rt = "<h1><b>Maximus </b>{}</h1>".format(self.symbol)
    self.rich_text_1.content=rt
    self.image_symbol.source=self.main.mm['logo']
    self.label_intro.text= self.label_intro.text.format(symbol=self.main.mm['ticker'], stake_years = int(self.main.mm['days_staked']/365))
    self.rich_text_description.content=self.rich_text_description.content.format(symbol=self.main.mm['ticker'], stake_length=self.main.mm['days_staked'])    
  def text_box_1_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    if self.text_box_1.text in ['', None, 0]:
      self.button_2.text='MINT {}'.format(self.symbol)
      self.button_2.enabled = True
      
      self.units=0
      
    else:
      self.button_2.text = 'MINT {:.8f} {}'.format(float(self.text_box_1.text/self.redemption_rate), self.symbol)
      raw_units = float(self.text_box_1.text)
      self.units = int(raw_units*100000000)
    try:
      self.check_approval()
    except Exception as e:
      raise e
      Notification('You must first connect to MetaMask.').show()
      return False
    if self.units>self.approved_hex:
      self.column_panel_2.visible=True
      self.label_1.visible=True
      self.link_3.visible=True
      self.column_panel_2.role='card'
      self.button_2.enabled = False
      self.label_1.text="First, {} needs your permission to interact with {} of your HEX.".format(self.maxi_contract.name(),raw_units)
      self.button_2_copy.text = 'APPROVE {} HEX'.format(raw_units)
      
    else:
      self.column_panel_2.visible=False
      self.button_2.enabled = True

  def check_approval(self):
    
    self.approved_hex = int(self.hex_contract.allowance(self.main.address, self.main.web3_wallet.MAXI_CONTRACT_ADDRESS).toNumber() or 0)
    
    
    return self.approved_hex

  def link_hex_balance_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.text_box_1.text=float(float(self.hex_balance)/100000000)
    self.text_box_1_change(sender=self.text_box_1)
  def approve_request(self, units):
    try:
      a = anvil.js.await_promise(self.write_hex_contract.approve(self.main.web3_wallet.MAXI_CONTRACT_ADDRESS, units))
      a.wait()
      self.label_1.visible=False
      self.link_3.visible=False
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVING", "APPROVED")
      self.button_2_copy.background='green'
      self.column_panel_2.role=''
      self.button_2_copy.enabled=False
      self.button_2_copy.icon='fa:check'
      self.button_2.enabled=True
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVING", "APPROVE")
      self.text_box_1_change()
  def button_2_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    if 'APPROVE' in self.button_2_copy.text:
      
      self.button_2_copy.text=self.button_2_copy.text.replace("APPROVE", "APPROVING")
      self.button_2_copy.enabled=False
      self.approve_request(self.units)
    else:
      self.text_box_1_change()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    """This method is called when the button is clicked"""
    try:
      raw_units = float(self.text_box_1.text)
    except:
      return False
    units = int(raw_units*100000000)
    try:
      self.check_approval()
    except:
      Notification('You must connect to MetaMask on Ethereum Mainnet.').show()
      return False
    if units>self.approved_hex:
      self.column_panel_3.visible=False
      self.column_panel_2.visible=True
      #a = alert(Label(font_size=24,text='Maximus needs your approval to interact with {} of your HEX'.format(raw_units)),buttons=[('Cancel', False)])
      #
    else:
      
      self.button_2_copy.enabled=False
      self.button_2.enabled=False
      self.button_2.text='MINTING {:.8f} {}'.format(raw_units/self.redemption_rate, self.symbol)
      
      existing_hex = self.hex_balance
      try:
        a = anvil.js.await_promise(self.write_maxi_contract.pledgeHEX(units))
        a.wait()
        self.button_2.enabled=True
        self.button_2.text='MINT {}'.format(self.symbol)
        self.text_box_1.text=None
        self.text_box_1_change(sender=self.text_box_1)
        self.button_2_copy.enabled=True
        self.button_2_copy.background='#246BFD'
        self.button_2.foreground='white'
        self.button_2_copy.icon=''
        self.refresh_mint()
      except Exception as e:
        try:
          alert(e.original_error.reason)
        except:
          alert(e.original_error.message)

  def link_need_hex_click(self, **event_args):
    """This method is called when the link is clicked"""
    c=ColumnPanel()
    l = Label(text='Get HEX on Uniswap')
    
    li = Link(text='https://app.uniswap.org/#/swap?inputCurrency=0x2b591e99afe9f32eaa6214f7b7629768c40eeb39&outputCurrency=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=mainnet',url='https://app.uniswap.org/#/swap?inputCurrency=0x2b591e99afe9f32eaa6214f7b7629768c40eeb39&outputCurrency=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&chain=mainnet')

    c.add_component(l)
    c.add_component(li)
    a = alert(c, large=True)

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    if event_args['sender'].icon == 'fa:check':
      pass
    else:
      try:
        tokenSymbol = self.symbol
        tokenDecimals = 8
        tokenImage = "{}/token/logo/{}".format(anvil.server.get_api_origin(), self.symbol)#'https://watery-decisive-guitar.anvil.app/_/api/name/maxi.jpg';
        
        from anvil.js.window import ethereum
        a = ethereum.request({
        'method': 'wallet_watchAsset',
        'params': {
          'type': 'ERC20', 
          'options': {
            'address': self.main.web3_wallet.MAXI_CONTRACT_ADDRESS, 
            'symbol': tokenSymbol, 
            'decimals': tokenDecimals, 
            'image': tokenImage, 
          },
        },
      })
        anvil.js.await_promise(a)
        
        event_args['sender'].icon = 'fa:check'
        event_args['sender'].text='{} Token Added'.format(self.symbol)
      except Exception as e:
        print(e)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('To protect your security, in order for the {name} contract to Mint {symbol} with your HEX you must approve an exact amount of HEX that the {name} contract is allowed to use on your behalf.'.format(name=self.maxi_contract.name(), symbol=self.symbol))

  def button_start_stake_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.write_maxi_contract.stakeHEX()





