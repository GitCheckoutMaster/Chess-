import pygame
from piece import Piece

class Board:
  def __init__(self):
    self.active_piece = None
    self.active_square = None
    self.active_color = (238,238,210)
    self.highlighted_square = []
    self.highlighted_legal_moves = []
    self.en_passant = None
    self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    # self.FEN = "4k3/3n4/1r4q1/2N1b3/2B5/Q4R2/4N3/4K3 w - - 0 1"
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
        
        if idx in self.highlighted_legal_moves:
          pygame.draw.rect(screen, (0, 255, 0), (j * 60, i * 60, 60, 60))
        elif idx in self.highlighted_square:
          pygame.draw.rect(screen, (255, 0, 0), (j * 60, i * 60, 60, 60))
        else:
          pygame.draw.rect(screen, color, (j * 60, i * 60, 60, 60))

        # Draw the pieces
        piece = self.board[i * 8 + j]
        if piece != "" and piece != "_":
          screen.blit(Piece.pieces_img.get(piece, None), (j * 60, i * 60))
        if self.active_square is not None:
          screen.blit(Piece.pieces_img.get(self.active_piece, None), (pygame.mouse.get_pos()[0] - 30, pygame.mouse.get_pos()[1] - 30))
                

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
      if empty_count > 0:
        new_FEN += str(empty_count)
        empty_count = 0
      new_FEN += "/"
      
    new_FEN = new_FEN[:-1]  # remove the last "/"
    new_FEN += " "
    new_FEN += " ".join(self.FEN.split(" ")[1:])
    self.FEN = new_FEN


  # Handle mouse button down event
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


  # Handle mouse button up event
  def mouse_up(self, move):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = mouse_y // 60
    col = mouse_x // 60
    index = row * 8 + col
    same_move = False

    # if move is not legal or if the piece is not the correct color then clean up the mess and return without doing anything
    if self.active_piece is not None and (((self.active_piece.isupper() and self.FEN.split(" ")[1] == "b") or (self.active_piece.islower() and self.FEN.split(" ")[1] == "w") or (index < 0 or index >= 64)) or (self.active_square == index) or index not in self.highlighted_legal_moves):
      self.board[self.active_square] = self.active_piece
      self.active_piece = None
      self.active_square = None
      self.update_fen()
      if len(self.highlighted_square) > 1:
        self.highlight_square(self.highlighted_square[0], self.highlighted_square[1])
      else:
        self.highlighted_square = []
      return

    piece = self.board[index]

    if self.active_piece is not None:
      
      # selected piece will move to an empty square
      if piece == "":
        self.board[index] = self.active_piece
        self.highlight_square(self.active_square, index)

        # pawn dash (two squares forward) then mark the square behind it with "_"
        if self.active_piece.lower() == 'p':
          self.clean_up()
          if self.active_square // 8 == 1 and index // 8 == 3:
            self.board[index - 8] = "_"
          elif self.active_square // 8 == 6 and index // 8 == 4:
            self.board[index + 8] = "_"
          self.en_passant = 'b' if self.active_piece.isupper() else 'w'
          print(self.en_passant)
          same_move = True
        
        self.change_turn(move)
      
      # en passant capture
      elif piece == '_' and self.active_piece.lower() == 'p':
        self.board[index] = self.active_piece
        if Piece.color(self.active_piece) == 'w':
          self.board[index + 8] = ""
        else:
          self.board[index - 8] = ""
        
        self.change_turn(move)
        self.highlight_square(self.active_square, index)
        self.clean_up()

      # capture of enemy piece or stop at friendly piece
      else:
        active_piece_color = 8 if self.active_piece.isupper() else 16
        target_piece_color = 8 if piece.isupper() else 16

        # capture
        if active_piece_color != target_piece_color:
          self.board[index] = self.active_piece
          self.highlight_square(self.active_square, index)
          self.change_turn(move)
        # friendly piece
        else:
          self.board[self.active_square] = self.active_piece
          if len(self.highlighted_square) > 1:
            self.highlight_square(self.highlighted_square[0], self.highlighted_square[1])
          self.highlighted_square = []
      
      self.active_piece = None
      self.active_square = None
    
    if not same_move and self.en_passant is not None and self.FEN.split(" ")[1] == self.en_passant:
      self.clean_up()

    self.update_fen()


  # Highlight the active square and target square
  def highlight_square(self, active_square=None, target_square=None, clear=True):
    if clear:
      self.highlighted_square = []
    if active_square is not None:
      self.highlighted_square.append(active_square)
    if target_square is not None:
      self.highlighted_square.append(target_square)


  # Change the turn in FEN and update the move number
  def change_turn(self, move):
    print("Changing turn")
    self.highlighted_legal_moves = []
   
    if self.FEN.split(" ")[1] == "w":
      self.FEN = self.FEN.replace("w", "b")
    else:
      # increase the move after black's turn and also change the turn in FEN
      move_number = int(self.FEN.split(" ")[5]) + 1
      new_FEN = " ".join(self.FEN.split(" ")[:5]) + " " + str(move_number)
      self.FEN = new_FEN
      self.FEN = self.FEN.replace("b", "w")

    move.generate_moves(self.board, self.FEN.split(" ")[1])
  

  # Highlight legal moves of clicked piece 
  def highlight_legal_moves(self, legal_moves):
    self.highlighted_legal_moves = []
    row = pygame.mouse.get_pos()[1] // 60
    col = pygame.mouse.get_pos()[0] // 60
    idx = row * 8 + col
    piece = self.active_piece if self.active_piece is not None else self.board[idx]


    if piece == "" or (piece.isupper() and self.FEN.split(" ")[1] == "b") or (piece.islower() and self.FEN.split(" ")[1] == "w"):
      # self.highlighted_legal_moves = []
      return

    legal_moves = legal_moves.get(self.active_square, [])
    print(piece, legal_moves)
    for move in legal_moves:
      self.highlighted_legal_moves.append(move)
    

  # Clean up the board 
  def clean_up(self):
    self.highlighted_legal_moves = []
    self.en_passant = False

    for square in range(64):
      if self.board[square] == "_":
        self.board[square] = ""
