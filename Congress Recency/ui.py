from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import secrets
from db import init_db, create_session, get_session_by_code, get_session_by_id, add_player, get_players, move_player

app = Flask(__name__, template_folder='.', static_folder='.')
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins='*')

# Initialize DB
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/po')
def po_dashboard():
    session_id = request.args.get('session_id')
    session_info = None
    if session_id:
        session_info = get_session_by_id(session_id)
    return render_template('po_dashboard.html', session_info=session_info)

@app.route('/speaker')
def speaker_join():
    return render_template('speaker_join.html')

@app.route('/speaker/view')
def speaker_view():
    code = request.args.get('code')
    name = request.args.get('name')
    if not code or not name:
        return redirect(url_for('speaker_join'))
    session_info = get_session_by_code(code)
    if not session_info:
        return redirect(url_for('speaker_join'))
    return render_template('speaker_view.html', code=code, name=name, session=session_info)

# API endpoints
@app.route('/api/create-session', methods=['POST'])
def api_create_session():
    data = request.json or {}
    po_name = data.get('po_name')
    round_name = data.get('round_name')
    room_number = data.get('room_number')
    session_id, code = create_session(po_name, round_name, room_number)
    if session_id:
        return jsonify({'success': True, 'session_id': session_id, 'code': code})
    return jsonify({'success': False}), 400

@app.route('/api/validate-code', methods=['POST'])
def api_validate_code():
    data = request.json or {}
    code = data.get('code')
    session_info = get_session_by_code(code)
    if session_info:
        return jsonify({'success': True, 'session': session_info})
    return jsonify({'success': False}), 400

@app.route('/api/join-session', methods=['POST'])
def api_join_session():
    data = request.json or {}
    code = data.get('code')
    name = data.get('name')
    session_info = get_session_by_code(code)
    if not session_info:
        return jsonify({'success': False}), 400
    add_player(session_info['id'], name)
    players = get_players(session_info['id'])
    socketio.emit('players_updated', {'players': players}, room=session_info['id'])
    return jsonify({'success': True, 'session_id': session_info['id']})

@app.route('/api/session/<session_id>/players')
def api_get_players(session_id):
    players = get_players(session_id)
    return jsonify({'players': players})

@app.route('/api/move-player', methods=['POST'])
def api_move_player():
    data = request.json or {}
    player_id = data.get('player_id')
    session_id = data.get('session_id')
    move_player(session_id, player_id)
    players = get_players(session_id)
    socketio.emit('players_updated', {'players': players}, room=session_id)
    return jsonify({'success': True})

# SocketIO
@socketio.on('join')
def on_join(data):
    session_id = data.get('session_id')
    join_room(session_id)
    emit('joined', {'ok': True})

@socketio.on('leave')
def on_leave(data):
    session_id = data.get('session_id')
    leave_room(session_id)
    emit('left', {'ok': True})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
