from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime, date
from . import db
from .models import User, Appointment, Matches
from sqlalchemy import or_

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home1():
    return render_template("home.html", user=current_user)


@views.route('/appointments', methods=['POST', 'GET'])
@login_required
def manage_appointments():
    if request.method == 'POST':
        date_str = request.form.get('date')
        time_str = request.form.get('time')

        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        new_appointment = Appointment(date=date_obj, time=time_obj, user_id=current_user.id) #place=place_str

        db.session.add(new_appointment)
        db.session.commit()

        success_message = "Appointment created successfully!"
        return render_template("success.html", user=current_user, success_message=success_message)


    elif request.method == 'GET':
        return render_template("appointment.html", user=current_user)
    
    else:
        error_message = "Error in Appointment creation!"
        return render_template("appointment.html", user=current_user, error_message=error_message)
    

@views.route('/match-appointments', methods=['GET'])
@login_required
def match_appointments_endpoint():
    current_user_id = current_user.id
    # place_str = place_str

    matched_appointments_data = []

    
    today = date.today()
    user_appointments = Appointment.query.filter_by(user_id=current_user_id, date=today).all() #place=place_str
    print(user_appointments)
    match_data = []

    for appointment in user_appointments:
        matches = Matches.query.filter(
            or_(Matches.match_id == appointment.id, Matches.match_with_id == appointment.id)
        ).all()
        print(matches)
        for match in matches:
            match_appointment = Appointment.query.get(match.match_id)
            match_appointment_with = Appointment.query.get(match.match_with_id)
        
            match_user = User.query.get(match_appointment.user_id)
            match_with_user = User.query.get(match_appointment_with.user_id)
            match_data.append({
                "match" : match_user.first_name,
                "match_with" : match_with_user.first_name,
                "match_with_id" : match_with_user.id,
                "match_with_lastName" : match_with_user.last_name,
                "match_place" : match_user.place,
                "details":match
            })
    print(match_data)
    return render_template("matched.html", matches=match_data, matched_appointments=matched_appointments_data , user=current_user)
