
from datetime import date
import mysql.connector


NAME_DB = "agendas_discordbot"
PASSWORD = ''
HOST = 'localhost'
USER = "root"

def open_db(USER, PASSWORD, HOST, NAME_DB):
    try:
        db = mysql.connector.connect(user=USER, password=PASSWORD, 
                                     host=HOST, database=NAME_DB)
        cursor = db.cursor(dictionary=True)
    except:
        return None, None
    else:
        return db, cursor


def create_scheduling(date, hour):
    db, cursor = open_db(USER, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"insert into agenda_aberta values (default, '{date}', '{hour}');")
        db.commit()
        db.close()
        
        
def delete_schedule():
    db, cursor = open_db(USER, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute("truncate table agenda_aberta;")
        db.commit()
        db.close()
        

def return_schedule():
    db, cursor = open_db(USER, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute("select * from agenda_aberta;")
        schedule = cursor.fetchall()
        db.close()
        return schedule
    
def delete_scheduling(start_date):
    db, cursor = open_db(USER, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"delete from agenda_aberta where data_inicio = '{start_date}';")
        db.commit()
        db.close()
        
def date_conversor(start_date):
    from datetime import datetime
    start_date = datetime.strptime(start_date.replace('/','-'), '%d-%m-%Y').date()
    return start_date

def date_us_to_br(date):
    from datetime import datetime
    
    date = datetime.strftime(date, '%d-%m-%Y')
    print(date)

