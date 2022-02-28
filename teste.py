import dao

import datetime
today = datetime.datetime.now()
hour = today.strftime('%H:%M')
date = today.strftime('%d/%m/%Y')

schedule = dao.return_schedule()
if schedule:
    for dictionary in schedule:
        if dictionary["data_inicio"] == date:
         

    