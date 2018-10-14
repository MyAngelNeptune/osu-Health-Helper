import socket

SERVER = 'irc.ppy.sh'
PORT = 6667

IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IRC.connect((SERVER, PORT))
print('opened')
IRC.send('/msg MyAngelNeptune owo')
IRC.close()
print('closed')
