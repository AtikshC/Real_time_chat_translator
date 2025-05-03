"""
Author: Atiksh Chawla
Date: May 2, 2025
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from googletrans import Translator

# Create the Flask application
app = Flask(__name__)
# Wrap it with Socket.IO support
socketio = SocketIO(app)
# Initialize the translator client
translator = Translator()

# Dictionaries to track connected clients:
# client_lang maps session IDs (sid) to each client's chosen language
client_lang = {}      # sid -> preferred language
# user_sid maps usernames to their session IDs
user_sid = {}         # username -> sid
# sid_user maps session IDs back to usernames
sid_user = {}         # sid -> username

@app.route('/')
def index_route():
    """Serve the chat UI."""
    return render_template('index.html')

@socketio.on('register')
def handle_register(data):
    """
    Register a new user:
    - Store their username → sid mapping
    - Store their sid → username mapping
    - Set a default language ('en') for this session
    """
    username = data.get('username', 'User')
    user_sid[username]        = request.sid
    sid_user[request.sid]     = username
    client_lang[request.sid]  = 'en'  # default language
    print(f"🔑 {username} registered with sid {request.sid}")

@socketio.on('set_language')
def handle_set_language(data):
    """
    Update a client's preferred language.
    Expects data = { 'lang': '<language_code>' }.
    """
    lang = data.get('lang', 'en')
    client_lang[request.sid] = lang
    print(f"📝 {request.sid} set language to {lang}")

@socketio.on('disconnect')
def handle_disconnect():
    """
    Clean up mappings when a client disconnects:
    - Remove their sid from all tracking dicts
    """
    sid = request.sid
    username = sid_user.get(sid)
    if username:
        user_sid.pop(username, None)
        sid_user.pop(sid, None)
    client_lang.pop(sid, None)
    print(f"❌ {sid} disconnected")

@socketio.on('send_message')
def handle_send_message(data):
    """
    Handle a message send attempt:
    - Validate sender, recipient
    - Translate the message into the recipient's language
    - Emit only to the target client's sid
    """
    original = data.get('msg', '')
    sender   = data.get('username', 'User')
    target   = data.get('target')
    print(f"🔔 from {sender} to {target}: {original}")

    # Ensure the target user exists
    if not target or target not in user_sid:
        emit('error', {'msg': f"User '{target}' not found."}, to=request.sid)
        return

    # Lookup the recipient's session ID and language
    dest_sid = user_sid[target]
    lang = client_lang.get(dest_sid, 'en')
    try:
        # Perform translation
        translated = translator.translate(original, dest=lang).text
    except Exception:
        # Fallback to original text on failure
        translated = original

    # Send the translated message to the recipient only
    payload = {
        'username': sender,
        'translated': translated
    }
    emit('receive_message', payload, to=dest_sid)

if __name__ == '__main__':
    # Run the app with Eventlet for async support
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
