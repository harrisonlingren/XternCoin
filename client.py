import socket, sys, json
from time import sleep

def main(args):
    print('Host: ' + args[1])
    host = args[1]
    print('Port: '+ str(args[2]))
    port = int(args[2])


    print('Welcome to the XternCoin client v0.1!\n')
    username = input('Please enter your username: ')
    guessing_range = int(input('Please enter the guessing range to use: '))

    print('\nStarting mining session. Press Ctrl + C to Quit.')

    while (True):
        print('Mining new coin...')
        for i in range(guessing_range):
            # message to be sent
            msg = json.dumps({
                'user': username,
                'guess': i
            })

            # Create socket and send message to host
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(msg.encode())

            # Print response
            resp = s.recv(1024).decode()
            resp_obj = json.loads(resp)

            if (resp_obj['result']):
                print('  Success! New balance: {}'.format(resp_obj['balance']))
                break

        # once coin has been successfully mined, sleep to let the socket breathe
        sleep(0.5)

    # Close socket
    s.shutdown(socket.SHUT_RDWR)
    s.close()

if __name__ == '__main__':
    # pass host, port
    if len(sys.argv) >= 3:
        main(sys.argv)
    elif len(sys.argv) == 2:
        main([sys.argv[0], sys.argv[1], 8080])
    else:
        main(['', 'localhost', 8081])
