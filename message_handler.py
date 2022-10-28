import discord
import json
from datetime import datetime
import base64
import manage
import pytz
from collections import OrderedDict

def log(ctx):
    log_msg = str(ctx.message.author) + " said: " + str(ctx.message.content) + "(" + str(ctx.channel) + ")" + " " + str(datetime.now())
    with open('bot_log.txt', 'a') as f:
      f.write(log_msg + "\n")
  

def priv():
    embed = discord.Embed(title='Oie! Os comandos do NUBAS funcionam também no chat privado!', description='O NUBAS preza pela sua privacidade :lock:', color=discord.Color.purple())
    return embed
def join(ctx, arg1):
    
    user = str(ctx.message.author)
    n_conta = str(arg1)

    with open('accounts.json', 'r', encoding='utf-8') as f:
      accounts = json.load(f)

    
    for key in accounts:
      if accounts[key]['user'] == str(user):
        embed = discord.Embed(title=":x: Algo deu errado", description="Você já tem uma conta NUBAS, por enquanto a NUBAS oferece apenas uma conta linkada com seu discord", color=discord.Color.purple())             
        return embed

    if n_conta in accounts:
      embed = discord.Embed(title=":x: Conta NUBAS já registrada neste número", description="Tente usar outro número de conta.", color=discord.Color.purple())
      return embed

    if not n_conta.isdigit():
      embed = discord.Embed(title=":x: Número de conta inválido", description="Tente usar outro número de conta.", color=discord.Color.purple())
      return embed

    if len(n_conta) != 2 or int(n_conta) < 0:
      embed = discord.Embed(title=":x: Número da conta inválido. Digite 2 caracteres numéricos positivos.", description="", color=discord.Color.purple())
      return embed
        
    accounts[n_conta] = {"cash": 0.00, "user": user}
    with open('accounts.json', 'w', encoding='utf-8') as f:
      json.dump(accounts, f, indent=4)
    
    embed = discord.Embed(title="Nu Conta criada!", description="Sua conta NUBAS foi criada com sucesso! :white_check_mark:", color=discord.Color.purple())
    embed.add_field(name="Conta: {conta}, atibuída a {usu}".format(conta=n_conta, usu=user), value='Obrigado por criar sua conta NUBAS! :purple_heart:')

    log(ctx)
    
    return embed
def picas(ctx, arg1, arg2):
            
      user = str(ctx.message.author)

    
          #embed = discord.Embed(title=":x: Algo deu errado", description="Alguns dados estão faltando! Tente novamente no formato:", color=discord.Color.purple())
          #embed.add_field(name=".picas QUANTIDADE CONTA", value="A conta deve ser o número de dois dígitos atrelado a conta de quem está recebendo.")
          #return embed

      with open('accounts.json', 'r', encoding='utf-8') as f:
          accounts = json.load(f)

      with open('stores.json', 'r', encoding='utf-8') as f:
          stores = OrderedDict(json.load(f))

      for key in accounts:
          if accounts[key]['user'] == user:
              account_number = key
              
      if float(accounts[account_number]['cash']) < float(arg1):
          embed = discord.Embed(title=":x: Algo deu errado", description="Dinheiro insuficiente.", color=discord.Color.purple())
          return embed

      if float(arg1) <= 0:
          embed = discord.Embed(title=":x: Algo deu errado", description="Quantidade Inválida", color=discord.Color.purple())
          return embed
      
      if str(arg2) not in accounts and str(arg2) not in stores:
          embed = discord.Embed(title=":x: Algo deu errado", description="Conta {conta} não existe.".format(conta=arg2), color=discord.Color.purple())
          return embed
      ##
      
      if str(arg2) in accounts:
        accounts[account_number]['cash'] = float(f"{(float(accounts[account_number]['cash']) - float(arg1)):.2f}")
        accounts[str(arg2)]['cash'] = float(f"{(float(accounts[str(arg2)]['cash']) + float(arg1)):.2f}")

        
      elif str(arg2) in stores:
        
        accounts[account_number]['cash'] = float(f"{(float(accounts[account_number]['cash']) - float(arg1)):.2f}")
        
        for i, owner in enumerate(stores[str(arg2)]['owners']):

          perc = float(stores[str(arg2)]['percentages'][i])
          print(accounts[owner]['cash'])
          accounts[owner]['cash'] = float(f"{(float(accounts[owner]['cash']) + (float(arg1) * perc/100)):.2f}")
          print(accounts[owner]['cash'])


      ###

      with open('accounts.json', 'w', encoding='utf-8') as f:
          json.dump(accounts, f, indent=4)

      tz = pytz.timezone('Brazil/East')
      today = datetime.now(tz)
      today_f = f'{today.day}{"/"}{today.month}{"/"}{today.year}{" "}{today.hour}{":"}{today.minute}{":"}{today.second}'

      transfer_log = str(account_number) + " " + str(arg2) + " " + str(arg1) +" "+ today_f
      with open('transfer_log.txt', 'a') as f:
          f.write(transfer_log + "\n")

      embed = discord.Embed(title="Transferência realizada com sucesso! :money_with_wings:", description="Obrigado por usar o NUBAS! :purple_heart:", color=discord.Color.purple())
      confirmation_hash = bytes(transfer_log, 'utf-8') 
      confirmation_hash = base64.b64encode(confirmation_hash)
      confirmation_hash = confirmation_hash.decode()

      dados = "De: " + str(account_number) + "\nPara: " + str(arg2) + "\nValor: " + str(arg1) + " NUB$\nData: " + today_f + "\n"
      embed.add_field(name="Dados da transferência:", value=dados)
      embed.add_field(name="Hash de confirmação:", value=confirmation_hash, inline=False)

      log(ctx)
      return embed
  
def veri(ctx, arg1):

  
      #embed = discord.Embed(title=":x: Algo deu errado", description="Alguns dados estão faltando! Tente novamente no formato:", color=discord.Color.purple())
      #embed.add_field(name=".veri HASH_DE_CONFIRMAÇÃO", value="O Hash de Confirmação é gerado com toda transferência.")
      #return embed

  with open('transfer_log.txt') as f:
      transfer_log = f.read().splitlines()
  

  try:
      decoded_hash = base64.b64decode(str(arg1))
      decoded_hash = str(decoded_hash, "utf-8")

  except UnicodeDecodeError:
      embed = discord.Embed(title=":x: Algo deu errado", description="Hash inserido incorreto.", color=discord.Color.purple())

      log(ctx)
      
      return embed

  if decoded_hash not in transfer_log:
      embed = discord.Embed(title=":x: Algo deu errado", description="Transação não encontrada no log, verifique se o hash inserido é o correto.", color=discord.Color.purple())
      return embed
  
  else:
      embed = discord.Embed(title="Transferência encontrada", description="A transferência foi encontrada nos logs do NUBAS",color=discord.Color.purple())

      hash_splited = decoded_hash.split(' ')
      if len(hash_splited[1]) == 3:

        with open('stores.json', 'r', encoding='utf-8') as f:
          stores = OrderedDict(json.load(f))

        hash_splited[2] = hash_splited[2] + " (" +  ", ".join((stores[hash_splited[1]]['percentages'])) + ")" 
        hash_splited[1] = hash_splited[1] + " (" + ", ".join((stores[hash_splited[1]]['owners'])) + ")"
        


      dados = "De: " + hash_splited[0] + "\nPara: " + hash_splited[1] + "\nValor: " + hash_splited[2] + " NUB$\nData: "+ hash_splited[3]+ " "+ hash_splited[4]+  "\n\nTransferência confirmada :white_check_mark:"
      embed.add_field(name="Dados da transferência:", value=dados)
      return embed
      
def loja(ctx, *args):
    # embed = discord.Embed(title=":x: Algo deu errado", description=f"{len(args)}", color=discord.Color.purple())
    # return embed

    nome_da_loja = str(args[0])
    cnpj = int(args[1])
    owners = []
    percentages = []
    
    for i,arg in enumerate(args):
      if i >= 2:
        if i % 2 == 0:
          owners.append(arg)
        else:
          percentages.append(arg)

    print(len(owners), len(percentages))

    if len(owners) != len(percentages):
      embed = discord.Embed(title=":x: Algo deu errado", description=f"Número de porcentagens não é igual ao número de donos", color=discord.Color.purple())
      return embed
    
    all_percentage = 0
    for percent in percentages:
      all_percentage += float(percent)

    if not (all_percentage >= 99 and all_percentage <= 100):
      embed = discord.Embed(title=":x: Algo deu errado", description=f"Porcentagem inválida", color=discord.Color.purple())
      return embed

    if (cnpj < 100) or (cnpj > 999):
      embed = discord.Embed(title=":x: Algo deu errado", description="CNPJ inválido. Insira um número positivo de 3 dígitos entre 100 e 999", color=discord.Color.purple())
      return embed

    with open('accounts.json', 'r', encoding='utf-8') as f:
      accounts = json.load(f)

    overall_percentage = 0

    # verifica dados dos donos
    for owner in owners:
      if str(owner) not in accounts:
        embed = discord.Embed(title=":x: Algo deu errado", description=f"Conta {owner} inválida.", color=discord.Color.purple())
        return embed

    ### ADICIONA DADOS EM STORES.JSON

    with open('stores.json', 'r', encoding='utf-8') as f:
      stores = json.load(f)

    if str(cnpj) in stores:
      embed = discord.Embed(title=":x: Algo deu errado", description="CNPJ já em uso.", color=discord.Color.purple())
      return embed

    stores[cnpj] = {'nome': nome_da_loja,'owners': (owners), 'percentages': (percentages)}
    
    with open('stores.json', 'w', encoding='utf-8') as f:
      json.dump(stores, f, indent=4)

    embed = discord.Embed(title=f"Loja {nome_da_loja} criada", description=f"Loja '{nome_da_loja}' criada com êxito. Dados:", color=discord.Color.purple())
    embed.add_field(name='CNPJ:', value=f'{cnpj}')
    embed.add_field(name='Donos:', value=f'{", ".join(owners)}')
    embed.add_field(name='Porcentagens:', value=f'{", ".join(percentages)}')
    return embed
    
    
def add(ctx, arg1, arg2):
  
    diamonds = int(arg1)
    account = str(arg2)
  
    try:
      manage.add(diamonds, account)
      embed = discord.Embed(title=f"{diamonds*10} NUB$ ({diamonds} diamantes) adicionados da conta {account}", description="", color=discord.Color.purple())

      tz = pytz.timezone('Brazil/East')
      today = datetime.now(tz)
      today_f = f'{today.day}{"/"}{today.month}{"/"}{today.year}{" "}{today.hour}{":"}{today.minute}{":"}{today.second}'
      
      transfer_log = "+" + str(float(diamonds)*10) +" "+ account + " "+ today_f
      with open('transfer_log.txt', 'a') as f:
        f.write(transfer_log + "\n")

      log(ctx)
      
      return embed
      
    except Exception as e:
      embed = discord.Embed(title=f"Ocorreu um erro: {e}", description="", color=discord.Color.purple())
      return embed
      
def rmv(ctx, arg1, arg2):
    diamonds = int(arg1)
    account = str(arg2)
    
    try:
      manage.rmv(diamonds, account)
      embed = discord.Embed(title=f"{diamonds*10} NUB$ ({diamonds} diamantes) removidos da conta {account}", description="", color=discord.Color.purple())
  
      tz = pytz.timezone('Brazil/East')
      today = datetime.now(tz)
      today_f = f'{today.day}{"/"}{today.month}{"/"}{today.year}{" "}{today.hour}{":"}{today.minute}{":"}{today.second}'
      
      transfer_log = "-" + str(float(diamonds)*10) +" "+ account +" "+ today_f
      with open('transfer_log.txt', 'a') as f:
        f.write(transfer_log + "\n")

      log(ctx)
      
      return embed
      
    except Exception as e:
      embed = discord.Embed(title=f"Ocorreu um erro: {e}", description="", color=discord.Color.purple())
      return embed

def rmvstore(ctx, arg1):
  store = str(arg1)

  with open('stores.json', 'r') as f:
    stores = json.load(f)
  if store not in stores:
    embed = discord.Embed(title=f":x: Ocorreu um erro:", description=f"{store} not in stores.json", color=discord.Color.purple())
    return embed

  del stores[store]

  with open('stores.json', 'w') as f:
    json.dump(stores, f, indent=4)

  embed = discord.Embed(title=f"Loja {store} removida", description=f"", color=discord.Color.purple())
  return embed

def saldo(ctx):
  user = str(ctx.message.author)
  with open('accounts.json', 'r', encoding='utf-8') as f:
    accounts = json.load(f)
  
  for key in accounts:
      if accounts[key]['user'] == user:
          account_number = key
  
  embed = discord.Embed(title="O saldo na sua conta é de: ", description=str(accounts[account_number]['cash']) + " NUB$ :moneybag:", color=discord.Color.purple())
  embed.add_field(name="Dados da conta:", value="Usuário: " + str(accounts[account_number]['user']) + "\n Número da conta: " + str(account_number))

  log(ctx)
  return embed



  