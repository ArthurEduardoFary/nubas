
import json

def getallmoney():
  with open('accounts.json', 'r') as f:
    accounts = json.load(f)

  bank_cash = 0
  for key in accounts:
        bank_cash += accounts[key]['cash']
            
  return bank_cash