# XternCoin

I made this stupidly simple psuedo-cryptocurrency system for a technical screening for an internship.

## server.py
Generates a queue of random integers using a given range, then accepts client connections over TCP, handles their guesses, and responds accordingly.

## client.py
Connects to a XternCoin server at a given host and port, logins in with a username, and mines for XternCoin over a given range.
