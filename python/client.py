#!/usr/bin/python

from symbol import pass_stmt
import sys
import json
import socket

# def checkAround(board, r, c, player):
#   comp = 0
#   if player == 1:
#     comp = 2
#   elif player == 2:
#     comp = 1
#   player = []
#   if r<len(board)-1 and board[r+1][c] == comp:
#     player.append({r+1, c})
#   if r>0 and board[r-1][c] == comp:
#     player.append({r-1, c})
#   if c<len(board[r])-1 and board[r][c+1] == comp:
#     player.append({r, c+1})
#   if c>0 and board[r][c-1] == comp:
#     player.append({r, c-1})
#   return player[0]


def isValid(spot, board, player):
  if player == 1:
    next = 2
  else:
    next = 1
  it = board[spot[0]][spot[1]] # spot is a spot on the board comprised of the row and column 
  i = spot # start at spot position
  while(i[0]<len(board) and i[1]<len(board) and i[0]>0 and i[1]>0):
    if(board[i[0]][i[1]]==next):
      pass
      # search for next spot with opponent until we find a white spot
  return True  # FIXME

def lookAround(player, board, i, j):

  # look around the board if space is valid until we find en empty spot
  if board[i][j] == 0:
    return {i, j}
  if(i+1<len(board)):
    lookAround(player, board, i+1, j)
  if(j+1<len(board)):
    lookAround(player, board, i, j+1)
  if(i>0):
    lookAround(player, board, i-1, j)
  if(j>0):
    lookAround(player, board, i, j-1)
  if(i>0 and j>0):
    lookAround(player, board, i-1, j-1)
  if(i<len(board) and j<len(board)):
    lookAround(player, board, i+1, j+1)


def findPlayer(player, board):
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == player:
        spot =  lookAround(player, board, i, j)
        if(isValid(spot, board, player)):
          return spot
        
  return lookAround(player, board, 5, 5)


def get_move(player, board):
  move = findPlayer(player, board)
  return move
  
  # start at board[4][4] and check around for same player and different player
  # r = 4
  # c = 4
  # valid = True
  # while(valid):
  #   if board[r][c] == player:
  #     choices = checkAround(board, r, c, player)
  #     if choices is None:
  #       valid = False
  #       break
  #     checkValid(choices, player)


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
