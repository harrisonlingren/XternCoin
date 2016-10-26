import random, collections, sys, socket, json

# initialize number queue, ledger dictionary and max range
num_queue = collections.deque()
ledger = {}
MAX_RANGE = 0

# update queue function, after each socket is closed
def update_queue():
    global num_queue
    global MAX_RANGE

    while (len(num_queue) < 25):
        new_num = random.randrange(0,MAX_RANGE)
        print('Adding to queue: {}'.format(new_num))
        num_queue.append(new_num)

# update ledger method -- If success == true, update ledger and return new balance. Otherwise, return old balance
def update_ledger(user, success):
    global ledger
    global num_queue

    # if user does not exist in ledger, create record
    if user not in ledger:
        ledger[user] = 0

    if success:
        ledger[user] += 1
        num_queue.pop()
        print('>  Updated user: {} | Balance: {}'.format(user, ledger[user]))
        return ledger[user]
    else:
        return ledger[user]

# parse details from the message, return as dictionary
def parse_message(msg):
    # strip headers from client request, create detail object and return
    parsed_msg = json.loads(msg)

    user = parsed_msg['user']
    guess = int(parsed_msg['guess'])
    details = {
        'user': user,
        'guess': guess
    }
    return details

# check guess against the queue
def check_num(guess):
    global num_queue

    # compare guess with rightmost deque item
    if (num_queue[-1] == int(guess)):
        return True
    else:
        return False

# Boilerplate socket connection 'n whatnot
def main(argv):
    global MAX_RANGE
    port = int(argv[0])
    MAX_RANGE = int(argv[1])
    print('Port: {}, Range: {}'.format(port, MAX_RANGE))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)
    print('Listening on port {} for connections...\n'.format(port))

    #main
    while(1):
        # build/update the queue if less than 25
        update_queue()

        # init new connection
        connection, address = s.accept()
        message = connection.recv(1024).decode('UTF-8')

        # parse connection info from message
        details = parse_message(message)

        # check guess against queue
        result = check_num(details['guess'])

        if (result == True):
            # update ledger, remove number from queue
            bal = update_ledger(details['user'], result)

            resp = json.dumps({
                'helper_text': 'Congrats! You guessed correctly and have been awarded one (1) XternCoin. Your balance is now {}.'.format(bal),
                'balance': bal,
                'result': result
            })
            connection.send(resp.encode())
            connection.close()
        else:
            # get balance from ledger
            bal = update_ledger(details['user'], result)

            resp = json.dumps({
                'helper_text': 'Incorrect guess. Try again!',
                'balance': bal,
                'result': result
            })
            connection.send(resp.encode())

    # cleanup
    s.shutdown(socket.SHUT_RDWR)
    s.close()

# SOP
if __name__ == '__main__':
    # Check if the port is specified in arguments
    if len(sys.argv) > 2:
        # run on given port with given range
        main(sys.argv[1:])
    elif len(sys.argv) == 2:
        # run on given port with 100 as range if no port/range specified
        main([sys.argv[1], 100])
    else:
        # run on port 8080 with 100 as range if no port/range specified
        main([8080, 100])
