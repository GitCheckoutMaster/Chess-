import pygame

class Piece:
  white = 8
  black = 16
  pawn = 1
  white_pawn_img = pygame.image.load("assets/white_pawn.png")
  white_knight_img = pygame.image.load("assets/white_knight.png")
  white_bishop_img = pygame.image.load("assets/white_bishop.png")
  white_rook_img = pygame.image.load("assets/white_rook.png")
  white_queen_img = pygame.image.load("assets/white_queen.png")
  white_king_img = pygame.image.load("assets/white_king.png")
  black_pawn_img = pygame.image.load("assets/black_pawn.png")
  black_knight_img = pygame.image.load("assets/black_knight.png")
  black_bishop_img = pygame.image.load("assets/black_bishop.png")
  black_rook_img = pygame.image.load("assets/black_rook.png")
  black_queen_img = pygame.image.load("assets/black_queen.png")
  black_king_img = pygame.image.load("assets/black_king.png")
  knight = 3
  bishop = 3
  rook = 5
  queen = 9
  king = 10
  pieces = {
    "P": white | pawn,
    "N": white | knight,
    "B": white | bishop,
    "R": white | rook,
    "Q": white | queen,
    "K": white | king,
    "p": black | pawn,
    "n": black | knight,
    "b": black | bishop,
    "r": black | rook,
    "q": black | queen,
    "k": black | king
  }
  pieces_img = {
    "P": white_pawn_img,
    "N": white_knight_img,
    "B": white_bishop_img,
    "R": white_rook_img,
    "Q": white_queen_img,
    "K": white_king_img,
    "p": black_pawn_img,
    "n": black_knight_img,
    "b": black_bishop_img,
    "r": black_rook_img,
    "q": black_queen_img,
    "k": black_king_img
  }
  
  @staticmethod
  def get_piece_value(symbol):
    return Piece.pieces.get(symbol, None)