#conversor de datas



from datetime import datetime
import dao

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