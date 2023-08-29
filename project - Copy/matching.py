from website import create_app, db
from website.models import *
import datetime
from datetime import date
from datetime import time as timos
import time as sleeptime
import random
from flask_mail import Mail, Message


app = create_app()
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'testemail12982@gmail.com'
app.config['MAIL_PASSWORD'] = 'vhgzpwxmpnvugrrq'
#app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

with app.app_context():
    start_hour = 11
    start_minute = 00
    end_hour = 11
    end_minute = 30

    def send_matching_mail(match, matched_with):
        user_match = db.session.get(User,match.user_id)

        user_match_with =db.session.get(User,matched_with.user_id)

        msg = Message('Matching system', sender = ('Matching', 'testemail12982@gmail.com'), recipients = [user_match.email])
        msg.body = "Sie essen heute mit: {}".format(str(user_match_with.email))
        mail.send(msg)

    def send_notfound_mail(match):
        user_match = db.session.get(User, match.user_id)
        msg = Message('Matching system', sender = 'testemail12982@gmail.com', recipients = [user_match.email])
        msg.body = "Kein Paar gefunden :("
        mail.send(msg)

    def get_appointments_by_time(target_time):
        today = date.today()
        appointments = Appointment.query.filter_by(date=today, time=target_time).all()
        return appointments
    def shufle_and_insert(subarray_data):
        appointments_data = [appointment for appointment in subarray_data]
        random.shuffle(appointments_data)
        subarrays = [appointments_data[i:i+2] for i in range(0, len(appointments_data), 2)]

        for elem in subarrays:
            if len(elem) == 2:
                if Matches.query.filter_by(match_id=elem[0].id, match_with_id=elem[1].id, date=elem[0].date, time=elem[0].time).first() is None: #place=elem[0].place
                    match = Matches(match_id=elem[0].id, match_with_id=elem[1].id, date=elem[0].date, time=elem[0].time) #place=elem[0].place
                    db.session.add(match)
                    db.session.commit()
                    
                    send_matching_mail(elem[0], elem[1])
                    send_matching_mail(elem[1], elem[0])
            elif len(elem) == 1:
                send_notfound_mail(elem[0])
            else:
                print("Not found")
            
    
    while True:
        now = datetime.datetime.now().time()
        start_time = datetime.time(start_hour, start_minute)
        end_time = datetime.time(end_hour, end_minute)
        
        if start_time <= now <= end_time:
            appointments_data = []
            today = date.today()
            # appointments_today = Appointment.query.filter_by(date=today).all() 
            appointments_1130am = get_appointments_by_time(timos(11, 30))
            appointments_12am = get_appointments_by_time(timos(12, 0))
            appointments_1213am = get_appointments_by_time(timos(12, 30))
            shufle_and_insert(appointments_1130am)
            shufle_and_insert(appointments_12am)
            shufle_and_insert(appointments_1213am)
            time_until_next_day = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), start_time) - datetime.datetime.now()
            sleeptime.sleep(time_until_next_day.seconds)
        else:
            time_left = datetime.datetime.combine(datetime.date.today(), start_time) - datetime.datetime.now()
            print(f"Waiting until {start_time.strftime('%I:%M %p')}... Time left: {time_left}")
            sleeptime.sleep(time_left.seconds + 5)




   
