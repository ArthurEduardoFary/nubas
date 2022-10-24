import json
def add(diamonds, account):
    
    with open('accounts.json', 'r', encoding='utf-8') as f:
        accounts = json.load(f)

    accounts[account]['cash'] = accounts[account]['cash'] + float(diamonds)*10
  
    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=4)

def rmv(diamonds, account):
    
    with open('accounts.json', 'r', encoding='utf-8') as f:
        accounts = json.load(f)
    
    accounts[account]['cash'] = accounts[account]['cash'] - float(diamonds)*10
  
    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=4)
