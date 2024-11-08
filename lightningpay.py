import requests
import json
import uuid
from datetime import datetime
import os

strikeapikey = os.environ.get('strikeapikey')

def generate_invoice_id():
    """
    Generates a unique invoice ID using the current date/time and a unique identifier
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")  # format current date/time
    uid = str(uuid.uuid4().hex.upper()[0:6])  # generate unique identifier
    invoice_id = f"{now}-{uid}"  # combine date/time and identifier
    return invoice_id

def lightning_invoice(amount, description):
  # Create a new invoice
  url = "https://api.strike.me/v1/invoices"

  payload = json.dumps({
    "correlationId": generate_invoice_id(),#</= 40 characters
    "description": description, #</= 200 characters
    "amount": {
      "currency": "USD", # [BTC, USD, EUR, USDT, GBP]
      "amount": amount #for testing purposes
    }
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {strikeapikey}' #TODO: make this an environment variable
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  # print(response.json())
  invid = response.json()['invoiceId']
  return invid

# Function to generate lightning address
def lightning_quote(amount, description):
  invid = lightning_invoice(amount, description)
  # insert invoice id here
  url = "https://api.strike.me/v1/invoices/"+invid+"/quote" 

  payload={}
  headers = {
    'Accept': 'application/json',
    'Content-Length': '0',
    'Authorization': f'Bearer {strikeapikey}' #TODO: make this an environment variable
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  lninv = response.json()['lnInvoice']
  conv_rate = response.json()['conversionRate']['amount']
  return lninv, conv_rate, invid


def invoice_status(invoiceId):

  url = f"https://api.strike.me/v1/invoices/{invoiceId}"
  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {strikeapikey}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  status = response.json()['state']
  return status

if __name__ == '__main__':
   import qrcode
   amount = '0.01'
   description = 'Example Payment Completion'
   lninv, conv_rate, invid = lightning_quote(amount, description)
   qrcode.make(lninv).show()