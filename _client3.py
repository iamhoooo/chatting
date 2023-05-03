import socket
import PySimpleGUI as sg
import threading

# 서버 IP 및 열어줄 포트
#HOST = '127.0.0.1'
HOST = '192.168.10.159'
PORT = 9999

# 소켓 생성 및 서버와 연결 시도
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 레이아웃 설정
layout = [
    [sg.Multiline(size=(70, 20), key='output')],
    [sg.Input(key='input', size=(50, 3)), sg.Button('Send', bind_return_key=True), sg.Button('Quit')]
]
window = sg.Window('Chat Room', layout)

def receive_data():
    # 서버로부터 메시지를 수신하는 함수
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            output_message = data.decode()
            window['output'].print(output_message)  # 화면에 출력
        except:
            break

threading.Thread(target=receive_data).start()

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Quit'):
        break
    if event == 'Send':
        message = values['input']
        client_socket.send(message.encode())  # 서버로 메시지 전송
        window['output'].print(f'You: {message}')
        window['input'].update('')

client_socket.close()
window.close()
