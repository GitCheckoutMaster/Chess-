import pygame
import board
import moves
from piece import Piece

# pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 480))
clock = pygame.time.Clock()
pygame.display.set_caption("Dumb and Dumber Gambit, Blunder Variation: Chess")
running = True

board = board.Board()
moves = moves.Moves()
board.load_fen()
board.update_fen()
board.print_board(screen)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      board.mouse_down()
      board.highlight_legal_moves(moves.legal_moves)
      board.load_fen()
        
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      board.mouse_up()
      # board.update_fen()
      board.load_fen()

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  # RENDER YOUR GAME HERE
  board.print_board(screen)
  moves.generate_legal_moves_for_sliding_pieces(board.board, board.FEN.split(" ")[1])

  # flip() the display to put your work on screen
  pygame.display.flip()

  clock.tick(60)  # limits FPS to 60

pygame.quit()