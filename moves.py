from piece import Piece
import pygame

class Moves:
  def __init__(self):
    self.legal_moves = {}
    self.king_offsets = [1, 7, 8, 9]
    self.pawn_offsets = [8, 16, 7, 9]
    self.offsets = [1, -1, -8, 8, -7, -9, 9, 7]
    self.rook_offsets = [1, 8]
    self.bishop_offsets = [7, 9]
    self.knight_offsets = [6, 10, 15, 17]
    self.num_square_to_edge = {}
    self.precomputed_move_data()
    
  def precomputed_move_data(self):
    for file in range(8):
      for rank in range(8):
        num_south = 7 - rank
        num_north = rank
        num_east = 7 - file
        num_west = file

        idx = rank * 8 + file

        self.num_square_to_edge[idx] = [
          num_east, num_west, num_north, num_south, min(num_north, num_east), min(num_north, num_west), min(num_south, num_east), min(num_south, num_west)
        ]


  def generate_moves_for_sliding_pieces(self, board, source_idx):
    legal_moves = []
    start_idx, end_idx = 0, 7
    if board[source_idx].lower() == 'r':
      start_idx, end_idx = 0, 3
    elif board[source_idx].lower() == 'b':
      start_idx, end_idx = 4, 7
    
    for direction, offset in enumerate(self.offsets[start_idx:end_idx + 1], start=start_idx):

      for move in range(self.num_square_to_edge[source_idx][direction]):
        target_idx = source_idx + offset * (move + 1)

        if move > 0 and board[source_idx].lower() == 'k':
          break

        if self.is_king_in_check(Piece.color(board[source_idx]), board, source_idx, target_idx):
          continue

        if Piece.are_friendly_pieces(board[source_idx], board[target_idx]):
          break

        legal_moves.append(target_idx)

        if Piece.are_enemy_pieces(board[source_idx], board[target_idx]):
          break

    return legal_moves


  def generate_moves(self, board, turn):
    
    for square in range(64):
      if board[square] != "" and Piece.color(board[square]) == turn:
        if Piece.is_sliding_piece(board[square]):
          moves = self.generate_moves_for_sliding_pieces(board, square)  
          self.legal_moves[square] = moves

    
    
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
  