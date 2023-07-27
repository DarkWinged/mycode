#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

# server.py
import eventlet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

if __name__ == '__main__':
    app = Flask(__name__)
    socketio = SocketIO(app)

    # Dictionary to store connected clients and their usernames
    clients = {}

    @socketio.on('connect')
    def on_connect():
        print(f'Client connected: {request.sid}')

    @socketio.on('join')
    def on_join(data):
        username = data.get('username')
        clients[request.sid] = username
        print(f'{username} joined the chat.')
        emit('server_message', f'{username} joined the chat.', broadcast=True)

    @socketio.on('user_message')
    def on_user_message(data):
        username = clients.get(request.sid)
        message = data.get('message')
        print(f'{username}: {message}')
        emit('server_message', f'{username}: {message}', broadcast=True, include_self=False)

    @socketio.on('disconnect')
    def on_disconnect():
        if request.sid in clients:
            username = clients[request.sid]
            del clients[request.sid]
            print(f'{username} left the chat.')
            emit('server_message', f'{username} left the chat.', broadcast=True)


    print(f"Starting server on port 5000...")
    socketio.run(app, host='0.0.0.0', port=5000)

