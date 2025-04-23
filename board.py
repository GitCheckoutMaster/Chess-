import pygame
from piece import Piece

class Board:
  def __init__(self):
    self.active_piece = None
    self.active_square = None
    self.active_color = (238,238,210)
    self.highlighted_square = []
    self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    self.board = [""] * 64
    # self.board = [
    #   "r", "n", "b", "q", "k", "b", "n", "r",
    #   "p", "p", "p", "p", "p", "p", "p", "p",
    #   " ", " ", " ", " ", " ", " ", " ", " ",
    #   " ", " ", " ", " ", " ", " ", " ", " ",
    #   " ", " ", " ", " ", " ", " ", " ", " ",
    #   " ", " ", " ", " ", " ", " ", " ", " ",
    #   "P", "P", "P", "P", "P", "P", "P", "P",
    #   "R", "N", "B", "Q", "K", "B", "N", "R"
    # ]

  def print_board(self, screen):
    # pygame.draw.rect(screen, (255, 255, 255), (0, 0, 60, 60))
    for i in range(8):
      for j in range(8):
        color = (255, 255, 255)
        if (i + j) % 2 != 0:
          color = (118, 150, 86)
        idx = i * 8 + j
        pygame.draw.rect(screen, self.active_color if idx in self.highlighted_square else color, (j * 60, i * 60, 60, 60))

        # Draw the pieces
        piece = self.board[i * 8 + j]
        if piece != "":
          screen.blit(Piece.pieces_img.get(piece, None), (j * 60, i * 60))
        if self.active_square is not None:
          screen.blit(Piece.pieces_img.get(self.active_piece, None), (pygame.mouse.get_pos()[0] - 30, pygame.mouse.get_pos()[1] - 30))
                
  # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
  def load_fen(self):
    i = 0
    # ROW, COL = 0, 0
    board_pos = 0
    
    while i < len(self.FEN):
      if self.FEN[i].isdigit():
        board_pos += int(self.FEN[i])
      elif self.FEN[i] == "/":
        # board_pos += 1
        i += 1
        continue
      elif self.FEN[i] == " " or board_pos >= 64:
        break
      else:
        self.board[board_pos] = self.FEN[i]
        board_pos += 1
      i += 1

  #TODO: update the last part of the FEN string 
  def update_fen(self):
    new_FEN = ""
    for i in range(8):
      empty_count = 0
      for j in range(8):
        piece = self.board[i*8 + j]
        if piece == "":
          empty_count += 1
        else:
          if empty_count > 0:
            new_FEN += str(empty_count)
            empty_count = 0
          new_FEN += piece
      new_FEN += str(empty_count) if empty_count > 0 else "/"
    new_FEN = new_FEN[:-1]  # remove the last "/"
    new_FEN += " "
    new_FEN += self.FEN.split(" ")[1]
    self.FEN = new_FEN

  def mouse_down(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = mouse_y // 60
    col = mouse_x // 60
    index = row * 8 + col

    piece = self.board[index]
    if piece != "":
      self.highlight_square(index, None, False)
      self.active_piece = piece
      self.active_square = index
      self.board[index] = ""  # Remove the piece from the board
    
    self.update_fen()

  def mouse_up(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = mouse_y // 60
    col = mouse_x // 60
    index = row * 8 + col  

    if self.active_piece is not None and ((self.active_piece.isupper() and self.FEN.split(" ")[1] == "b") or (self.active_piece.islower() and self.FEN.split(" ")[1] == "w") or (index < 0 or index >= 64)):
      self.board[self.active_square] = self.active_piece
      self.active_piece = None
      self.active_square = None
      self.update_fen()
      self.highlight_square(self.highlighted_square[0], self.highlighted_square[1] if len(self.highlighted_square) > 1 else None)
      return

    piece = self.board[index]

    if self.active_piece is not None:
      if piece == "":
        self.board[index] = self.active_piece
        self.highlight_square(self.active_square, index)
        self.change_turn()
      else:
        active_piece_color = 8 if self.active_piece.isupper() else 16
        target_piece_color = 8 if piece.isupper() else 16
        if active_piece_color != target_piece_color:
          self.board[index] = self.active_piece
          self.highlight_square(self.active_square, index)
          self.change_turn()
        else:
          self.board[self.active_square] = self.active_piece
          self.highlight_square(self.highlighted_square[0], self.highlighted_square[1] if len(self.highlighted_square) > 1 else None)
      
      self.active_piece = None
      self.active_square = None
    self.update_fen()

  def highlight_square(self, active_square=None, target_square=None, clear=True):
    if clear:
      self.highlighted_square = []
    if active_square is not None:
      self.highlighted_square.append(active_square)
    if target_square is not None:
      self.highlighted_square.append(target_square)

  def change_turn(self):
    print("Changing turn")
    if self.FEN.split(" ")[1] == "w":
      self.FEN = self.FEN.replace("w", "b")
    else:
      self.FEN = self.FEN.replace("b", "w")