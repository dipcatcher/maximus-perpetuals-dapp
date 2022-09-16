import anvil.secrets
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server



@anvil.server.http_endpoint('/token/logo/:ticker')
def get_logo(ticker):
  return app_tables.media.get(ticker=ticker)['logo']