#!/usr/bin/python

from symbol import pass_stmt
import sys
import json
import socket

def checkAround(board, r, c, player):
  comp = 0
  if player == 1:
    comp = 2
  elif player == 2:
    comp = 1
  player = []
  if r<len(board)-1 and board[r+1][c] == comp:
    player.append({r+1, c})
  if r>0 and board[r-1][c] == comp:
    player.append({r-1, c})
  if c<len(board[r])-1 and board[r][c+1] == comp:
    player.append({r, c+1})
  if c>0 and board[r][c-1] == comp:
    player.append({r, c-1})
  return player


def checkValid(choices, player):
  while(choices is not None):
    move = choices[0]
    print(choices)
    choices.pop(0)
    print(choices)


def get_move(player, board):
  if player == 1:
    pass
  if player == 2:
    pass
  for r in board:
    print(r)
  # start at board[4][4] and check around for same player and different player
  r = 4
  c = 4
  valid = True
  while(valid):
    if board[r][c] == player:
      choices = checkAround(board, r, c, player)
      if choices is None:
        valid = False
        break
      checkValid(choices, player)

  return 

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
