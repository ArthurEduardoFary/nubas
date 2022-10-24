import json
import datetime
import threading

RATE = 0.01

def main():
  print('Checking timer...')
  with open('last_interest.txt', 'r') as f:
    last = f.read()

  now = datetime.datetime.now()
  #2022-10-17 16:19:39.146111
  format = "%Y-%m-%d %H:%M:%S.%f"
    
  if now > datetime.datetime.strptime(last, format) + datetime.timedelta(days=1):
    print('updating money')
    sweep()
    with open('last_interest.txt', 'w') as f:
      f.write(str(now))

def sweep():
    with open('accounts.json', 'r', encoding='utf-8') as f:
        accounts = json.load(f)

    for key in accounts:
        accounts[key]['cash'] = accounts[key]['cash'] + float(f"{(accounts[key]['cash'] * RATE):.2f}")
            
    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=4)