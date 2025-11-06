from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import base64
import json
import time
import socket
import os
from datetime import datetime
from encryption_utils import encrypt_message, decrypt_message, generate_shared_key
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[*] Environment variables loaded from .env file")
except ImportError:
    print("[!] python-dotenv not installed. Install with: pip install python-dotenv")
    print("[!] Falling back to system environment variables")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[!] Google Generative AI not installed. Using fallback suggestions.")
    print("[!] Install with: pip install google-generativeai")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'securetalk_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        print("[*] Google Gemini AI initialized successfully!")
    except Exception as e:
        print(f"[!] Failed to initialize Gemini: {e}")
        GEMINI_AVAILABLE = False
elif GEMINI_AVAILABLE and not GEMINI_API_KEY:
    print("[!] GEMINI_API_KEY not set in .env file. Using fallback suggestions.")
    print("[!] Add 'GEMINI_API_KEY=your-key-here' to your .env file")
    print("[!] Get your free API key from: https://makersuite.google.com/app/apikey")
    GEMINI_AVAILABLE = False

shared_key = generate_shared_key()
print("[*] Web SecureTalk Server - Shared encryption key generated")

active_users = {}
user_count = 0
active_rooms = {}
stored_rooms = {}
network_stats = {
    'total_connections': 0,
    'total_messages': 0,
    'bytes_transferred': 0,
    'server_start_time': time.time(),
    'active_connections': 0,
    'message_history': [],
    'rooms_created': 0,
    'active_rooms': 0
}

stored_rooms.update({
    'MAIN01': {
        'name': 'General Chat',
        'description': 'Main public chat room',
        'maxUsers': 50,
        'features': ['encryption', 'typing', 'timestamps'],
        'isPublic': True,
        'created_at': time.time()
    },
    'TECH02': {
        'name': 'Tech Discussion', 
        'description': 'For technology discussions',
        'maxUsers': 25,
        'features': ['encryption', 'typing'],
        'isPublic': True,
        'created_at': time.time()
    },
    'RANDOM': {
        'name': 'Random Chat',
        'description': 'Casual conversations', 
        'maxUsers': 10,
        'features': ['encryption'],
        'isPublic': True,
        'created_at': time.time()
    }
})

@app.route('/')
def index():
    """Serve the main menu"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Serve the chat interface"""
    room = request.args.get('room', 'default')
    room_name = request.args.get('name', f'Room {room}')
    return render_template('chat.html', room=room, room_name=room_name)

@app.route('/create-room')
def create_room():
    """Serve the room creation page"""
    return render_template('create_room.html')

@app.route('/join-room')
def join_room_page():
    """Serve the join room page"""
    return render_template('join_room.html')

@app.route('/api/create-room', methods=['POST'])
def create_room_api():
    """API endpoint to create a new room"""
    try:
        data = request.get_json()
        
        import random
        import string
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        while room_code in stored_rooms:
            room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        stored_rooms[room_code] = {
            'name': data.get('name', f'Room {room_code}'),
            'description': data.get('description', ''),
            'maxUsers': int(data.get('maxUsers', 10)),
            'features': data.get('features', []),
            'isPublic': data.get('isPublic', True),
            'created_at': time.time(),
            'creator': data.get('creator', 'Anonymous')
        }
        
        network_stats['rooms_created'] += 1
        
        return json.dumps({
            'success': True,
            'roomCode': room_code,
            'roomData': stored_rooms[room_code]
        })
        
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)}), 500

@app.route('/api/rooms')
def get_rooms():
    """API endpoint to get available rooms"""
    public_rooms = {
        code: {
            'code': code,
            'name': room['name'],
            'description': room['description'],
            'maxUsers': room['maxUsers'],
            'currentUsers': len(active_rooms.get(code, {}).get('users', set())),
            'isPublic': room.get('isPublic', True)
        }
        for code, room in stored_rooms.items()
        if room.get('isPublic', True)
    }
    
    for code, room_info in public_rooms.items():
        print(f"[DEBUG API] Room {code}: {room_info['currentUsers']}/{room_info['maxUsers']} users")
    
    return json.dumps(public_rooms)

@app.route('/api/room/<room_code>')
def get_room_info(room_code):
    """API endpoint to get specific room information"""
    if room_code in stored_rooms:
        room_data = stored_rooms[room_code].copy()
        room_data['code'] = room_code
        room_data['currentUsers'] = len(active_rooms.get(room_code, {}).get('users', set()))
        return json.dumps(room_data)
    else:
        return json.dumps({'error': 'Room not found'}), 404

@app.route('/network-stats')
def network_stats_page():
    """Serve the network statistics dashboard"""
    return_room = request.args.get('return_room')
    return_name = request.args.get('return_name')
    return render_template('network_stats.html', return_room=return_room, return_name=return_name)

@app.route('/api/stats')
def get_stats():
    """API endpoint for network statistics"""
    current_time = time.time()
    uptime = current_time - network_stats['server_start_time']
    
    stats = {
        'server_uptime': f"{uptime:.2f} seconds",
        'total_connections': network_stats['total_connections'],
        'active_connections': network_stats['active_connections'],
        'total_messages': network_stats['total_messages'],
        'bytes_transferred': network_stats['bytes_transferred'],
        'rooms_created': network_stats['rooms_created'],
        'active_rooms': network_stats['active_rooms'],
        'server_ip': socket.gethostbyname(socket.gethostname()),
        'server_port': 5000,
        'protocol': 'WebSocket over HTTP',
        'encryption': 'AES-256-GCM',
        'active_users': [user_data['username'] for user_data in active_users.values()],
        'room_details': {
            room_code: {
                'name': room_data['name'],
                'user_count': len(room_data['users']),
                'message_count': room_data['message_count'],
                'created_at': room_data['created_at']
            } for room_code, room_data in active_rooms.items()
        }
    }
    return json.dumps(stats)


def generate_smart_replies_with_llm(message, max_suggestions=3):
    """Generate smart replies using Google Gemini LLM"""
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        return None
    
    try:
        prompt = f"""You are a helpful chat assistant. Given the following message, generate {max_suggestions} short, natural, and contextually appropriate reply suggestions. Each reply should be casual, friendly, and conversational.

Message: "{message}"

Requirements:
- Keep replies SHORT (max 8-10 words each)
- Make them sound natural and human-like
- Match the tone and context of the message
- Be relevant and helpful
- Use emojis sparingly when appropriate
- Provide diverse response options (e.g., one agreeing, one questioning, one supportive)

Return ONLY the {max_suggestions} reply suggestions, one per line, without numbering or bullet points."""

        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            suggestions = [
                line.strip() 
                for line in response.text.strip().split('\n') 
                if line.strip() and not line.strip().startswith(('*', '-', '1.', '2.', '3.'))
            ]
            
            cleaned_suggestions = []
            for s in suggestions:
                s = re.sub(r'^\d+[\.)]\s*', '', s)
                s = re.sub(r'^[-*•]\s*', '', s)
                if s:
                    cleaned_suggestions.append(s)
            
            return cleaned_suggestions[:max_suggestions]
    
    except Exception as e:
        print(f"[!] Gemini API error: {e}")
        return None
    
    return None


@app.route('/api/smart-replies', methods=['POST'])
def smart_replies_api():
    """API endpoint returning AI-powered smart-reply suggestions using Google Gemini LLM.
    Requires GEMINI_API_KEY to be set in .env file."""
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        
        if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
            return json.dumps({
                'suggestions': [],
                'ai_powered': False,
                'error': 'AI not configured. Please set GEMINI_API_KEY in .env file.'
            })
        
        suggestions = generate_smart_replies_with_llm(message)
        
        if not suggestions:
            suggestions = []
        
        return json.dumps({
            'suggestions': suggestions,
            'ai_powered': True
        })
    except Exception as e:
        return json.dumps({
            'suggestions': [],
            'ai_powered': False,
            'error': str(e)
        }), 500

@socketio.on('connect')
def on_connect():
    """Handle new user connections"""
    global user_count
    user_count += 1
    username = f"User{user_count}"
    active_users[request.sid] = {
        'username': username,
        'room': None,
        'join_time': time.time()
    }
    
    network_stats['total_connections'] += 1
    network_stats['active_connections'] = len(active_users)
    
    print(f"[+] {username} connected ({request.sid}) from {request.remote_addr}")
    print(f"[DEBUG] Total active users: {len(active_users)}")
    
    emit('user_connected', {
        'username': username,
        'message': f'Welcome to SecureTalk! You are {username}',
        'server_info': {
            'protocol': 'WebSocket',
            'encryption': 'AES-256-GCM',
            'server_ip': socket.gethostbyname(socket.gethostname())
        }
    })

@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining a specific room"""
    room_code = data.get('room', 'default')
    username = active_users.get(request.sid, {}).get('username', 'Unknown')
    
    if room_code not in stored_rooms and room_code != 'default':
        emit('room_error', {
            'error': 'Room not found',
            'message': f'Room {room_code} does not exist or has been deleted.'
        })
        return
    
    if room_code in stored_rooms:
        room_info = stored_rooms[room_code]
        room_name = room_info['name']
        max_users = room_info.get('maxUsers', 50)
    else:
        room_name = 'General Chat'
        max_users = 50
    
    current_users = len(active_rooms.get(room_code, {}).get('users', set()))
    if current_users >= max_users:
        emit('room_error', {
            'error': 'Room is full',
            'message': f'Room {room_name} is at capacity ({max_users} users).'
        })
        return
    
    old_room = active_users[request.sid].get('room')
    if old_room:
        leave_room(old_room)
        if old_room in active_rooms:
            active_rooms[old_room]['users'].discard(request.sid)
            if not active_rooms[old_room]['users']:
                del active_rooms[old_room]
                network_stats['active_rooms'] = len(active_rooms)
    
    join_room(room_code)
    
    if room_code not in active_rooms:
        active_rooms[room_code] = {
            'name': room_name,
            'users': set(),
            'created_at': time.time(),
            'message_count': 0,
            'message_history': []
        }
        if room_code not in stored_rooms:
            network_stats['rooms_created'] += 1
    
    was_already_in_room = request.sid in active_rooms[room_code]['users']
    
    active_rooms[room_code]['users'].add(request.sid)
    active_users[request.sid]['room'] = room_code
    network_stats['active_rooms'] = len(active_rooms)
    
    print(f"[+] {username} joined room {room_code} ({room_name})")
    print(f"[DEBUG] Room {room_code} now has {len(active_rooms[room_code]['users'])} users")
    print(f"[DEBUG] Session IDs in room: {list(active_rooms[room_code]['users'])}")
    print(f"[DEBUG] Usernames in room: {[active_users[sid]['username'] for sid in active_rooms[room_code]['users']]}")
    print(f"[DEBUG] Current user session ID: {request.sid}")
    print(f"[DEBUG] Was already in room: {was_already_in_room}")
    
    if not was_already_in_room:
        emit('user_joined', {
            'username': username,
            'message': f'{username} joined {room_name}',
            'room': room_code
        }, room=room_code, include_self=False)
    
    emit('room_joined', {
        'room': room_code,
        'room_name': room_name,
        'user_count': len(active_rooms[room_code]['users']),
        'max_users': max_users
    })
    
    if active_rooms[room_code]['message_history']:
        emit('message_history', {
            'messages': active_rooms[room_code]['message_history']
        })
    
    emit('room_stats', {
        'user_count': len(active_rooms[room_code]['users']),
        'message_count': active_rooms[room_code]['message_count']
    }, room=room_code)

@socketio.on('disconnect')
def on_disconnect():
    """Handle user disconnections"""
    if request.sid in active_users:
        user_data = active_users[request.sid]
        username = user_data['username']
        room_code = user_data.get('room')
        
        if room_code and room_code in active_rooms:
            active_rooms[room_code]['users'].discard(request.sid)
            emit('user_left', {
                'username': username,
                'message': f'{username} left the room'
            }, room=room_code)
            
            if active_rooms[room_code]['users']:
                emit('room_stats', {
                    'user_count': len(active_rooms[room_code]['users']),
                    'message_count': active_rooms[room_code]['message_count']
                }, room=room_code)
            else:
                del active_rooms[room_code]
                network_stats['active_rooms'] = len(active_rooms)
        
        del active_users[request.sid]
        
        network_stats['active_connections'] = len(active_users)
        
        print(f"[-] {username} disconnected")

@socketio.on('send_message')
def handle_message(data):
    """Handle encrypted message sending"""
    try:
        user_data = active_users.get(request.sid, {})
        username = user_data.get('username', 'Unknown')
        room_code = user_data.get('room', 'default')
        message = data.get('message', '').strip()
        
        if not message:
            return
        
        print(f"[MSG] {username} in {room_code}: {message}")
        
        network_stats['total_messages'] += 1
        message_size = len(message.encode('utf-8'))
        network_stats['bytes_transferred'] += message_size
        
        if room_code in active_rooms:
            active_rooms[room_code]['message_count'] += 1
            
            message_data = {
                'username': username,
                'message': message,
                'timestamp': data.get('timestamp', datetime.now().strftime('%H:%M:%S')),
                'encrypted_message': None
            }
            
            active_rooms[room_code]['message_history'].append(message_data)
            if len(active_rooms[room_code]['message_history']) > 50:
                active_rooms[room_code]['message_history'].pop(0)
        
        network_stats['message_history'].append({
            'timestamp': datetime.now().isoformat(),
            'username': username,
            'room': room_code,
            'size_bytes': message_size,
            'encrypted': True
        })
        if len(network_stats['message_history']) > 100:
            network_stats['message_history'].pop(0)
        
        encrypted_msg = encrypt_message(shared_key, message)
        
        if room_code in active_rooms and active_rooms[room_code]['message_history']:
            active_rooms[room_code]['message_history'][-1]['encrypted_message'] = encrypted_msg.decode('utf-8')
        
        emit('receive_message', {
            'username': username,
            'message': message,
            'encrypted_message': encrypted_msg.decode('utf-8'),
            'timestamp': data.get('timestamp'),
            'room': room_code,
            'packet_info': {
                'size_bytes': message_size,
                'protocol': 'WebSocket',
                'encrypted': True
            }
        }, room=room_code, include_self=False)
        
        emit('message_sent', {
            'message': message,
            'timestamp': data.get('timestamp'),
            'bytes_sent': message_size,
            'room': room_code
        })
        
        if room_code in active_rooms:
            emit('room_stats', {
                'user_count': len(active_rooms[room_code]['users']),
                'message_count': active_rooms[room_code]['message_count']
            }, room=room_code)
        
    except Exception as e:
        print(f"[ERROR] Failed to handle message: {e}")
        emit('error', {'message': 'Failed to send message'})

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicators"""
    user_data = active_users.get(request.sid, {})
    username = user_data.get('username', 'Unknown')
    room_code = user_data.get('room', 'default')
    
    emit('user_typing', {
        'username': username,
        'is_typing': data.get('is_typing', False),
        'room': room_code
    }, room=room_code, include_self=False)

if __name__ == '__main__':
    print("[*] Starting Web SecureTalk Server...")
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Listening on 0.0.0.0:{port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)