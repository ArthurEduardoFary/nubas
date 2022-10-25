
import message_handler
import discord
from discord.ext import commands, tasks
import interest
import os

def DiscordBot():
    
    #TOKEN = os.environ.get('DISCORD_TOKEN')
    with open('discord_token.txt', 'r') as f:
      TOKEN = f.read()
      
    client = commands.Bot(command_prefix='.',intents=discord.Intents.all())
  
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        reminder.start()
 
    @tasks.loop(hours=1)
    async def reminder():
      print('Opening interest...')
      interest.main()
      
      
    #COMMANDS

    @client.command(help='Cria uma nova conta no NUBAS (max. 1 por pessoa). O número da conta deve ser positivo e de dois caracteres (00 a 99)', brief='Cria uma conta no NUBAS')
    async def join(ctx, arg1):
      await ctx.channel.send(embed=message_handler.join(ctx, arg1))
      
    @client.command(help='Envia uma mensagem no seu privado para você poder usar o NUBAS com privacidade', brief='Envia uma mensagem para você')
    async def priv(ctx):
      await ctx.message.author.send(embed = message_handler.priv())
      
    @client.command(help='Verifica a partir de um codigo Hash se há alguma transação bancaria com o mesmo Hash', brief='Checa a vericidade da transação')
    async def veri(ctx, arg1):
      await ctx.channel.send(embed = message_handler.veri(ctx, arg1))
      
    @client.command(help='Transfere uma quantia determinada a outra pessoa no formato de .picas VALOR CONTA_DA_OUTRA_PESSOA', brief='Transfere dinheiro entre as pessoas')
    async def picas(ctx, arg1, arg2):
      await ctx.channel.send(embed = message_handler.picas(ctx, arg1, arg2))
      
    @client.command(help='Checa o seu saldo atual', brief='Checa seu saldo')
    async def saldo(ctx):
      await ctx.channel.send(embed = message_handler.saldo(ctx))

    @client.command(help='Cria e registra o CNPJ de uma loja', brief='Cria uma loja')
    async def loja(ctx, *args):
      await ctx.channel.send(embed = message_handler.loja(ctx, *args))
    
    @client.command(hidden = True, help='Vai remover seu dinheiro e ninguem vai ler isso pq so o yut pode usar esse comando')
    async def rmv(ctx, arg1, arg2):
      if str(ctx.message.author) == 'yut#7995':
        await ctx.channel.send(embed = message_handler.rmv(ctx, arg1, arg2))
        
    @client.command(hidden = True, help='um miojo e IMPOSIVEL ficar pronto em 3 minutos, e literalmente imposivel')
    async def add(ctx, arg1, arg2):
      if str(ctx.message.author) == 'yut#7995':
        await ctx.channel.send(embed = message_handler.add(ctx, arg1, arg2))

    @client.command(hidden = True, help='Tira uma loja')
    async def rmvstore(ctx, arg1):
      if str(ctx.message.author) == 'yut#7995':
        await ctx.channel.send(embed = message_handler.rmvstore(ctx, arg1))
    
    
    #ERROR HANDLERES

    @join.error
    async def join_error(ctx, error):
      if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=":x: Algo deu errado", description="Argumentos incorretos", color=discord.Color.purple())
        await ctx.channel.send(embed = embed)
      
    @veri.error
    async def veri_error(ctx, error):
      if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=":x: Algo deu errado", description="Argumentos incorretos", color=discord.Color.purple())
        await ctx.channel.send(embed = embed)

    @picas.error
    async def picas_error(ctx, error):
      if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=":x: Algo deu errado", description="Argumentos incorretos", color=discord.Color.purple())
        await ctx.channel.send(embed = embed)

    @loja.error
    async def loja_error(ctx, error):
      if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=":x: Algo deu errado", description="Argumentos incorretos", color=discord.Color.purple())
        await ctx.channel.send(embed = embed)

    @add.error
    async def add_error(ctx, error):
      if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=":x: Algo deu errado", description="Argumentos incorretos", color=discord.Color.purple())
        await ctx.channel.send(embed = embed)

    @rmv.error
    async def rmv_error(ctx, error):
      if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=":x: Algo deu errado", description="Argumentos incorretos", color=discord.Color.purple())
        await ctx.channel.send(embed = embed)
          
    client.run(TOKEN)
