import anvil.secrets
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
@anvil.server.callable
def tweet(text):
  data={}
  data['text']=text
  url = "https://hooks.zapier.com/hooks/catch/10571278/33o7rxr/"
  anvil.http.request(url, method="POST", data=data)