class Moves:
  def __init__(self):
    self.legal_moves = {}
    self.king_offsets = [1, 7, 8, 9]
    self.pawn_offsets = [8, 16, 7, 9]
    self.queen_offsets = [1, 7, 8, 9]
    self.rook_offsets = [1, 8]
    self.bishop_offsets = [7, 9]
    self.knight_offsets = [6, 10, 15, 17]

  
  def generate_moves(self, board, source_idx, offsets, turn):
    row = source_idx // 8
    col = source_idx % 8
    legal_moves = []

    for offset in offsets:
      
      target_idx = source_idx
      i, j = target_idx // 8, target_idx % 8
      displacement = 0

      while 0 <= target_idx < 64 and (i == row or j == col or (offset == 7 or offset == 9)):

        if displacement == 2 and board[source_idx].lower() == 'k':
          break
        
        if (target_idx != source_idx) and board[target_idx] == "" or (board[target_idx].isupper() and turn == "b") or (board[target_idx].islower() and turn == "w"):
          
          # if the king is in check after this move then skip it
          if self.is_king_in_check(turn, board, source_idx, target_idx):
            target_idx += offset
            i = (target_idx // 8)
            j = (target_idx % 8)
            displacement += 1
            continue

          # if the piece is a bishop or queen, check for diagonal moves and break if it hits the edge of the board
          if (offset == 7 and (row != i - displacement or col != j + displacement)) or (offset == 9 and (row != i - displacement or col != j - displacement)):
            break

          legal_moves.append(target_idx)
        
        # if a piece is in the way, break the loop
        if (target_idx != source_idx) and (board[target_idx] != "" or board[source_idx].lower() == "k"):
          break

        
        # if the piece is a bishop or queen, check for diagonal moves and break if it hits the edge of the board
        if (target_idx != source_idx) and (offset == 7 or offset == 9) and ((target_idx // 8) == 0 or (target_idx // 8) == 7 or (target_idx % 8) == 0 or (target_idx % 8) == 7):
          break
        
        target_idx += offset
        i = (target_idx // 8)
        j = (target_idx % 8)
        displacement += 1

      target_idx = source_idx
      i, j = target_idx // 8, target_idx % 8
      displacement = 0
      
      while 0 <= target_idx < 64 and ((i == row or j == col) or (offset == 7 or offset == 9)):

        if displacement == 2 and board[source_idx].lower() == 'k':
          break
      
        if (source_idx != target_idx) and board[target_idx] == "" or (board[target_idx].isupper() and turn == "b") or (board[target_idx].islower() and turn == "w"):
          
          # if the king is in check after this move then skip it
          if self.is_king_in_check(turn, board, source_idx, target_idx):
            if source_idx == 28 and target_idx == 19:
              print("King in check")
            target_idx -= offset
            i = target_idx // 8
            j = target_idx % 8
            displacement += 1
            continue

          # if the piece is a bishop or queen, check for diagonal moves and break if it hits the edge of the board
          if (offset == 7 and (row != i + displacement or col != j - displacement)) or (offset == 9 and (row != i + displacement or col != j + displacement)):
            break

          legal_moves.append(target_idx)

        # if a piece is in the way, break the loop
        if (target_idx != source_idx) and (board[target_idx] != "" or board[source_idx].lower() == "k"):
          break


        if (target_idx != source_idx) and (offset == 7 or offset == 9) and ((target_idx // 8) == 0 or (target_idx // 8) == 7 or (target_idx % 8) == 0 or (target_idx % 8) == 7):
          break

        target_idx -= offset
        i = target_idx // 8
        j = target_idx % 8
        displacement += 1
    
    return legal_moves


  def generate_legal_moves_for_sliding_pieces(self, board, turn):
    offsets_rook = self.rook_offsets
    offsets_bishop = self.bishop_offsets
    offsets_queen = self.queen_offsets
    offsets_king = self.king_offsets
    
    #Get every piece on the board and loop over their possible moves
    for i in range(64):
      if board[i] == "" or (board[i].isupper() and turn == "b") or (board[i].islower() and turn == "w"):
        continue
      piece = board[i]
      self.legal_moves[i] = []
      if piece.lower() == "r":
        self.legal_moves[i] = self.generate_moves(board, i, offsets_rook, turn)
      elif piece.lower() == "b":
        self.legal_moves[i] = self.generate_moves(board, i, offsets_bishop, turn)
      elif piece.lower() == "q":
        self.legal_moves[i] = self.generate_moves(board, i, offsets_queen, turn)
      elif piece.lower() == "k":
        self.legal_moves[i] = self.generate_moves(board, i, offsets_king, turn)    
    
    
  def is_king_in_check(self, turn, board, source_idx, target_idx):
    
    new_board = board.copy()

    def get_king_position(b, t):
      for i in range(64):
        if (t == "w" and b[i] == "K") or (t == "b" and b[i] == "k"):
          return i
      return -1

    new_board[target_idx] = board[source_idx]
    new_board[source_idx] = ""
    king_position = get_king_position(new_board, turn)

    for offset in self.rook_offsets:
      for direction in [1, -1]:  # both directions
        check = king_position
        while True:
          check += offset * direction
          if not (0 <= check < 64):
            break

          # Special care for horizontal moves (+1, -1)
          if offset == 1:
            if (check // 8) != (king_position // 8):
              break

          if (turn == 'b' and (new_board[check] == 'R' or new_board[check] == 'Q')) or (turn == 'w' and (new_board[check] == 'r' or new_board[check] == 'q')):
            return True

          if new_board[check] != "":
            break

      row = king_position // 8
      col = king_position % 8

      for offset in self.bishop_offsets:
        for direction in [1, -1]:
          check = king_position
          current_row = row
          current_col = col
          
          while True:
            if offset == 7:
              if direction == 1:
                current_row += 1
                current_col -= 1
              else:
                current_row -= 1
                current_col += 1
            elif offset == 9:
              if direction == 1:
                current_row += 1
                current_col += 1
              else:
                current_row -= 1
                current_col -= 1

            if not (0 <= current_row < 8 and 0 <= current_col < 8):
              break  # off the board

            check = current_row * 8 + current_col

            if (turn == 'b' and (new_board[check] == 'B' or new_board[check] == 'Q')) or (turn == 'w' and (new_board[check] == 'b' or new_board[check] == 'q')):
              return True

            if new_board[check] != "":
              break


    return False
  