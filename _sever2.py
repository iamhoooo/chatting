import socket
import PySimpleGUI as sg
import threading

# 서버 IP 및 열어줄 포트
#HOST = '127.0.0.1'
HOST = '192.168.10.159'
PORT = 9999

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

# GUI 레이아웃 설정
layout = [
    [sg.Multiline(size=(70, 20), key='output')],
    [sg.Input(key='input', size=(50, 3)), sg.Button('Send', bind_return_key=True)]
]
window = sg.Window('Chat Room', layout)

client_sockets = []  # 클라이언트 소켓을 리스트로 관리
output_value = ''  # 채팅 내역을 저장할 변수

def receive_data(client_socket, client_number):
    # 클라이언트로부터 데이터를 수신하는 함수
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            output_message = f'{client_number}: {data.decode()}'
            window['output'].print(output_message)  # 화면에 출력
            global output_value  # 전역 변수 사용
            output_value += output_message  # 변수에 저장
            # 모든 클라이언트에게 메시지 전달
            for sock in client_sockets:
                if sock != client_socket:
                    sock.send(output_message.encode())
        except:
            break


def start_server():
    # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
    # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다.
    global client_sockets
    while True:
        try:
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            client_number = len(client_sockets)  # 클라이언트 번호
            threading.Thread(target=receive_data, args=(client_socket, client_number)).start()
            # 모든 클라이언트에게 연결되었다는 메시지 전달
            for sock in client_sockets:
                if sock != client_socket:
                    sock.send(f'Client {client_number} is connected.'.encode())
        except:
            break


threading.Thread(target=start_server).start()

# GUI 이벤트 루프
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Send':
        message = values['input']
        for client_socket in client_sockets:
            client_socket.send(message.encode())
        client_number = len(client_sockets)  # 클라이언트 번호
        output_message = f'{client_number}: You: {message}\n'
        window['output'].print(output_message)  # 화면에 출력
        output_value += output_message  # 변수에 저장
        window['input'].update('')

window.close()
server_socket.close()
