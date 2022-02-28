import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import dao

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '!', case_insensitive = True, intents = intents)

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  game_today.start()
  
@bot.command(name='criador')
async def creator(ctx):
    embed = discord.Embed(
        title= 'Meus links de contato:',
        color= 0x0000ff
    )
    embed.set_footer(text='Feito por Mateus')
    embed.set_author(name='Mateus Toni Vieira', icon_url=bot.user.avatar_url)
    embed.add_field(name='Linkedin', value="https://www.linkedin.com/in/mateus-toni-941853217/")
    embed.add_field(name='Portifólio', value='https://mateustonivieira.netlify.app/')
    embed.add_field(name='Instagram', value='https://www.instagram.com/mateustoni323')
    embed.add_field(name='GitHub', value='https://github.com/Mateus-Toni')
    await ctx.author.send(embed=embed)
    
    
    
@bot.command(name='mix')
async def mix(ctx, *name):
  from random import choice
  list_player = [names.replace(",", "") for names in name]
  if len(list_player)  > 10:
    await ctx.send("Você me mandou mais que 10 nomes")
  elif len(list_player) < 10:
      await ctx.send("Você me mandou menos que 10 nomes")
  else:
    time_1 = []
    time_2 = []
    for _ in range(5):
      name = choice(list_player)
      if name not in time_1:
          time_1.append(name)
          list_player.remove(name)

    time_2 = (list_player[:])
    await ctx.send(f"O primeiro time é: {' - '.join(time_1)}")
    await ctx.send(f"O segundo time é: {' - '.join(time_2)}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Seja Bem-Vindo {0.mention} ao meu server! Fica a vontade só não quebra nada'.format(member)
        await guild.system_channel.send(to_send)
        

@bot.command(name='add_agenda')
async def create_scheduling(ctx, date, hour):
    dao.create_scheduling(date, hour)
    await ctx.send(f'agendamento criado dia {date} às {hour}')
    
@bot.command(name='deletar_agenda')
async def delete_schedule(ctx):
    dao.delete_scheduling()
    await ctx.send("Todos os agendamentos das ligas foram apagados")

@bot.command(name='agenda')
async def schedule(ctx):
  c = 0
  hour_game = []
  import datetime
  today = datetime.datetime.now()
  hour = today.strftime('%H:%M')
  date = today.strftime('%d/%m/%Y')
  schedule = dao.return_schedule()
  if schedule:
      for dictionary in schedule:
          if dictionary["data_inicio"] == date:
              c += 1
              hour_game.append(dictionary['hora_inicio'])
  if c >= 1:
    await ctx.send(f'Temos {c} jogo Hoje: \n' + '-'.join(hour_game))
  else:
    next_games = []
    if schedule:
      for dictionary in schedule:

        data = datetime.datetime.strptime(dictionary["data_inicio"], "%d/%m/%Y")

        if data.day > today.day:
          next_games.extend((dictionary['data_inicio'], dictionary['hora_inicio']))
    if len(next_games) == 2:
      if next_games:
          await ctx.send(f"""Não temos jogo hoje, 
                mas nosso próximo jogo é dia {next_games[0]} às {next_games[1]}""")
    else:
      await ctx.send("""Não temos jogo hoje, mas nosso próximos jogos são:""")
      if schedule:
          for dictionary in schedule:

              data = datetime.datetime.strptime(dictionary["data_inicio"], "%d/%m/%Y")

              if data.day > today.day:
                  await ctx.send(f"dia {dictionary['data_inicio']} às {dictionary['hora_inicio']}")
        
@tasks.loop(hours=6)
async def game_today():
  import datetime
  c= 0
  games = []
  today = datetime.datetime.now()
  if schedule := dao.return_schedule():
    for dictionary in schedule:
        data = datetime.datetime.strptime(dictionary["data_inicio"], "%d/%m/%Y")
        if data.day == today.day:
            c+=1
            games.append(dictionary)
  channel = bot.get_channel(947305621047377931)
  if c == 1:
      await channel.send(f"Temos um jogo hoje às {[value['hora_inicio'] for value in games]}")
  elif c == 0:
      await channel.send("não temos jogo hoje")
  else:
      await channel.send(f"Hoje temos {c} jogos, às:")
      for game in games:
          await channel.send(f"{game['hora_inicio']}")
    

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get('TOKEN'))
