class Moves:
  def __init__(self):
    self.legal_moves = {}

  def generate_legal_moves_for_sliding_pieces(self, board, turn):
    offsets_rook = [1, 8]
    offsets_bishop = [7, 9]
    offsets_queen = [1, 7, 8, 9]
    offsets_king = [1, 7, 8, 9]
    
    def generate_moves(board, source_idx, offsets):
      row = source_idx // 8
      col = source_idx % 8

      for offset in offsets:
        target_idx = source_idx + offset
        i, j = row, col
        while 0 <= target_idx < 64 and (i == row or j == col):
          if board[target_idx] == "" or (board[target_idx].isupper() and turn == "b") or (board[target_idx].islower() and turn == "w"):
            self.legal_moves[source_idx].append(target_idx)
          if board[target_idx] != "":
            break
          target_idx += offset
          if offset != 7 and offset != 9:
            i = (target_idx // 8)
            j = (target_idx % 8)

        target_idx = source_idx - offset
        i, j = row, col
        while 0 <= target_idx < 64 and (i == row or j == col):
          if board[target_idx] == "" or (board[target_idx].isupper() and turn == "b") or (board[target_idx].islower() and turn == "w"):
            self.legal_moves[source_idx].append(target_idx)
          if board[target_idx] != "":
            break
          target_idx -= offset
          if offset != 7 and offset != 9:
            i = target_idx // 8
            j = target_idx % 8

    
    #Get every piece on the board and loop over their possible moves
    for i in range(64):
      if board[i] == "" or (board[i].isupper() and turn == "b") or (board[i].islower() and turn == "w"):
        continue
      piece = board[i]
      self.legal_moves[i] = []
      if piece.lower() == "r":
        generate_moves(board, i, offsets_rook)
      elif piece.lower() == "b":
        generate_moves(board, i, offsets_bishop)
      elif piece.lower() == "q":
        generate_moves(board, i, offsets_queen)
      elif piece.lower() == "k":
        generate_moves(board, i, offsets_king)    
    
    
  def is_king_in_check(self):
    pass
