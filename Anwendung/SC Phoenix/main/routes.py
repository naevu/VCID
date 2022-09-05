from tkinter.messagebox import NO
from main import app, db, EVENT_TYPES, USER_ROLES
from main.model import *
from flask import render_template, request, session, flash, redirect, url_for
from datetime import datetime
from sqlalchemy import and_

@app.route("/signin", methods=["GET", "POST"])
def signin():

    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if '@' in email:
            query = User.query.filter(and_(User.email==email, User.password==password)).first()
        else:
            query = User.query.filter(and_(User.username==email, User.password == password)).first()
        

        if query:
            session['username'] = query.username
            session['user_id'] = query.id
            session['email'] = query.email
            session['role'] = query.role

            flash("Logged In Successfully!", "success") 
            return redirect(url_for('index')) 
        else:
            flash("Failed to Login!", "danger")
    return render_template("signin.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = 'normal'

        if password != confirm_password:
            flash('Passwords Didn\'t Match','danger')
            return redirect(url_for('signup'))

        exist = db.session.query(User).filter((User.email==email) | (User.username==username)).first()

        if exist:
            flash("User Already Exist", 'danger')
            return redirect(url_for('signup'))

        user = User(email=email, password=password, username=username, role=role)
        db.session.add(user)
        db.session.commit()

        session['username'] = username
        session['email'] = email
        session['role'] = role

        return redirect(url_for('index'))

    users = User.query.all()

    return render_template("signup.html", userInfo=session, userRoles=USER_ROLES, users=users)

@app.route('/')
@app.route("/index")
def index():
    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'admin':
        return redirect(url_for('manage_event'))

    if not 'user_id' in session:
        user = User.query.filter_by(email=session['email']).first()
        session['user_id'] = user.id
    
    events = Event.query.all()

    print(session)

    joined_events_by_user = []
    for event in events:
        for participant in event.participant:
            if participant.id == session['user_id']:
                joined_events_by_user.append(event.id)

    return render_template("dashboard.html", userInfo=session, events=events, events_joined=joined_events_by_user)


@app.route('/view_participants/<int:event_id>')
def view_participants(event_id):
    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'normal':
        return redirect(url_for('index'))

    eventInfo = Event.query.filter_by(id=event_id).first()

    return render_template('view_participants.html', userInfo=session, eventInfo=eventInfo)


@app.route('/manage_event', methods=["GET", "POST"])
def manage_event():
    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'normal':
        return redirect(url_for('index'))
    
    if request.method == "POST":
        name = request.form['event_name']
        location = request.form['event_location']
        date = datetime.strptime(request.form['event_date'], "%Y-%m-%d")
        e_type = request.form['event_type']

        event = Event(event_name=name, event_location=location, event_date=date, event_type=e_type)
        db.session.add(event)
        db.session.commit()

        return redirect(url_for('manage_event'))
    
    events = Event.query.all()

    return render_template('manage_event.html', userInfo=session, event_types=EVENT_TYPES, events=events)


@app.route('/join_event/<int:event_id>')
def join_event(event_id):
    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'admin':
        return redirect(url_for('manage_event'))
    
    join = joined_events.insert().values(
        user_id=session['user_id'],
        event_id=event_id
    )

    db.session.execute(join)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/leave_event/<int:event_id>')
def leave_event(event_id):
    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'admin':
        return redirect(url_for('manage_event'))
    
    event = Event.query.filter_by(id=event_id).first()
    event.participant.remove(User.query.filter_by(id=session['user_id']).first())
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):

    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'normal':
        return redirect(url_for('index'))

    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()

    return redirect(url_for('manage_event'))

@app.route('/remove/<int:event_id>/<int:user_id>')
def remove_participant(event_id, user_id):
    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'normal':
        return redirect(url_for('index'))
    
    event = Event.query.filter_by(id=event_id).first()
    event.participant.remove(User.query.filter_by(id=user_id).first())
    db.session.commit()

    return redirect(url_for('view_participants', event_id=event_id))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    if 'username' not in session:
        return redirect(url_for('signin'))

    if session['role'] == 'normal':
        return redirect(url_for('index'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('manageUser'))


@app.route("/manage_user", methods=["GET", "POST"])
def manageUser():
    if not 'username' in session:
        return redirect(url_for('signin'))

    if session['role'] != 'admin':
        return redirect(url_for('index'))
    
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['user_role'].lower()

        exist = db.session.query(User).filter((User.email==email) | (User.username==username)).first()

        if exist:
            flash("User Already Exist", 'danger')
            return redirect(url_for('manageUser'))

        user = User(email=email, password=password, username=username, role=role)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('manageUser'))

    users = User.query.all()

    return render_template("manageUser.html", userInfo=session, userRoles=USER_ROLES, users=users)


@app.route("/update_user/<int:id>", methods=["GET", "POST"])
def update_user(id):
    if not 'username' in session:
        return redirect(url_for('signin'))

    if session['role'] != 'admin':
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(id)

    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['user_role'].lower()

        user.email = email
        user.username = username
        user.role = role
        user.password = password if password else user.password
        db.session.commit()

        return redirect(url_for('manageUser'))

    return render_template("update_user.html", userInfo=session, userRoles=USER_ROLES, user=user)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('user_id')
        session.pop('email')
        session.pop('role')

        flash("Logged Out", 'info')

        return redirect(url_for('signin'))
    
    return redirect(url_for('index'))
