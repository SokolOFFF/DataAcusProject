import youtube_parser
import socket

def connectToSocket(sock, server_address):
    try:
        sock.connect(server_address)
    except:
        connectToSocket()

def parse_data(data):
    data = data.split(' ')
    if data[0] == 'subs':
        return youtube_parser.getNumberOfSubscribers(int(data[1]))
    else:
        return 'FUCK YOU'

host = '192.168.43.20'
port = 9900
server_address = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Connecting to server...')
connectToSocket(sock, server_address)
print("Connected to ESP socket. Let's rock!!")

bytes_to_receive = 8

try:
    while True:
        data = sock.recv(bytes_to_receive)
        print("Received: " + str(data))
        if data:
            message = parse_data(data.decode('utf-8'))
            print(f'Sending {message}')
            sock.sendall(message.encode('utf-8'))

except Exception as e:
    print(e)
    print("Closing connection to the server")
    sock.close()


finally:
    print("Closing connection to the server")
    sock.close()
