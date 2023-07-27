#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

# client.py
import eventlet
import socketio

def get_username():
    username = input("Enter your username: ")
    return username.strip()

def main():
    username = get_username()

    # Connect to the server
    server_ip = '127.0.0.1'  # Change this to the server IP address if running on a different machine
    server_port = 5000
    sio.connect(f"http://{server_ip}:{server_port}")

    # Send the username to the server during the "join" event
    sio.emit('join', {'username': username})

    # Main loop to send messages
    while True:
        try:
            message = input()
            if message.lower() == 'exit':
                break
            sio.emit('user_message', {'message': message})
        except KeyboardInterrupt:
            break

    sio.disconnect()

if __name__ == '__main__':
    sio = socketio.Client()

    @sio.on('connect')
    def on_connect():
        print(f'Connected to server.')

    @sio.on('server_message')
    def on_server_message(data):
        print(data)

    main()


