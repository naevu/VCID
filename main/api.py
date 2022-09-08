from main import app
from main.model import User, Event

@app.route('/api/get_user_info/id/<int:user_id>')
def get_user_by_id(user_id):
    message = dict()

    user = User.query.filter_by(id=user_id).first()

    if user:
        message = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    else:
        message = {
            'error': 'No User Found!'
        }
    
    return message


@app.route('/api/get_user_info/username/<string:username>')
def get_user_by_username(username):
    message = dict()

    user = User.query.filter_by(username=username).first()

    if user:
        message = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    else:
        message = {
            'error': 'No User Found!'
        }
    
    return message


@app.route('/api/get_user_info/email/<string:email>')
def get_user_by_email(email):
    message = dict()

    user = User.query.filter_by(email=email).first()

    if user:
        message = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    else:
        message = {
            'error': 'No User Found!'
        }
    
    return message


@app.route('/api/get_all_users')
def get_all_users():
    users = User.query.all()
    message = list()

    if users:
        for user in users:
            message.append(
                {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            )
    else:
        message = {
            'error': 'No User Found!'
        }
    
    return message


@app.route('/api/get_all_events')
def get_all_events():
    events = Event.query.all()
    message = list()

    if events:
        for event in events:

            participants = list()
            for part in event.participant:
                participants.append(
                    {
                        'user_id': part.id,
                        'username': part.username,
                        'email': part.email
                    }
                )

            message.append(
                {
                    'event_id': event.id,
                    'event_name': event.event_name,
                    'event_type': event.event_type,
                    'event_location': event.event_location,
                    'event_date': event.event_date,
                    'event_post_date': event.event_post_date,
                    'participant': participants
                }
            )
    else:
        message = {
            'error': 'No Event Found!'
        }
    
    return message

@app.route('/api/get_event_info/type/<string:event_type>')
def get_event_by_type(event_type):
    events = Event.query.filter_by(event_type=event_type).all()
    message = list()

    if events:
        for event in events:

            participants = list()
            for part in event.participant:
                participants.append(
                    {
                        'user_id': part.id,
                        'username': part.username,
                        'email': part.email
                    }
                )

            message.append(
                {
                    'event_id': event.id,
                    'event_name': event.event_name,
                    'event_type': event.event_type,
                    'event_location': event.event_location,
                    'event_date': event.event_date,
                    'event_post_date': event.event_post_date,
                    'participant': participants
                }
            )
    else:
        message = {
            'error': 'No Event Found!'
        }
    
    return message