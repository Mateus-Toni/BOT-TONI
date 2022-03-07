import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import youtube_dl
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
    convert_date = dao.date_conversor(date)
    dao.create_scheduling(convert_date, hour)
    await ctx.send(f'agendamento criado dia {date} às {hour}')
    
@bot.command(name='deletar_agenda')
async def delete_schedule(ctx):
    dao.delete_schedule()
    await ctx.send("Todos os agendamentos das ligas foram apagados")

@bot.command(name='agenda')
async def schedule(ctx):
  from datetime import datetime
  next_match = not_have = have = 0
  today = datetime.now().date()
  schedule = dao.return_schedule()
  if schedule:
      next_game = []
      today_game = []
      for dictionary in schedule:
          if today < dictionary['data_inicio']:
              next_game.append(dictionary)
              next_match += 1
          if today > dictionary['data_inicio']:
              dao.delete_scheduling(dictionary['data_inicio'])
          if today == dictionary['data_inicio']:
              today_game.append(dictionary)
              have += 1
      
                  
      if have == 1:
          for game in today_game:
              print(f'temos um jogo hoje às {game["hora_inicio"]}') 
              
          if next_match == 1:
              for games in next_game:
                  print(f'e também temos um jogo dia {games["data_inicio"]} às {games["hora_inicio"]}')
          elif next_match > 1:
              print(f'e também temos jogos:')
              for games in next_game:
                  print(f'dia {games["data_inicio"]} às {games["hora_inicio"]}')
      elif have > 1:
          print(f'temos {have} jogos Hoje, são eles:')
          for games in today_game:
              print(f'{games["hora_inicio"]}')
          
          if next_match == 1:
              for games in next_game:
                  print(f'e também temos um jogo dia {games["data_inicio"]} às {games["hora_inicio"]}')
          elif next_match > 1:
              print(f'e também temos jogos:')
              for games in next_game:
                  print(f'dia {games["data_inicio"]} às {games["hora_inicio"]}')
      else:
          if next_game:
              if next_match == 1:
                  for games in next_game:
                      print(f'Nosso próximo jogo é dia {games["data_inicio"]} às {games["hora_inicio"]}')
              elif next_match > 1:
                  print(f'Nossos próximos jogos estão marcados para:')
                  for games in next_game:
                      print(f'dia {games["data_inicio"]} às {games["hora_inicio"]}')
          else:
              print('Não temos jogos marcados para esta aberta')
  else:
      print('sem agendamentos')

@tasks.loop(hours=6)
async def game_today():
  import datetime
  c= 0
  games = []
  today = datetime.datetime.now()
  if schedule := dao.return_schedule():
    for dictionary in schedule:
        data = datetime.datetime.strftime(dictionary["data_inicio"], "%Y/%m/%d")
        if data == today:
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
    
@bot.command("mira")
async def mira(ctx):
  miras = {
        'Furia':{ 'Kscerato':'', 'Art':'', 'Saffee':'', 'Drop':'', 'Yuurih':''},
        'Imperial':{ 'Fallen':'', 'Fer':'', 'Fnx':'', 'Vini':'', 'Boltz':''},
        '00Nation':{ 'Coldzera':'', 'MalbsMD':'', 'T7Y':'', 'Leo_Drk':'', 'V$M':''},
        'GODSENT': { 'Taco':'', 'Latto':'', 'Felps':'', 'Dumau':'', 'B4artin':''},
        'paiN Gaming': { 'PKL':'', 'Hardzao':'', 'Biguzera':'', 'Nython':'', 'Nekiz':''},
        'Team One': { 'Maluk3':'', 'TRK':'', 'Pesadelo':'', 'XNS':'', 'Keiz':''},
        'MIBR':{ 'chello':'', 'exit':'', 'WOOD7':'', 'Tuurtle':'', 'Jota':'' }
        }
  await ctx.send('Copie alugamas das Miras Brasileiras:')
  for value in miras.values():
    for player, crosshair in value.items():
      await ctx.send(f"{player} -> {crosshair}")


#musica
@bot.command("play")
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Geral')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command("sair")
async def leave(ctx):
    voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command("pause")
async def pause(ctx):
    voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command("resume")
async def resume(ctx):
    voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command("stop")
async def stop(ctx):
    voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
    voice.stop()


if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get('TOKEN'))
