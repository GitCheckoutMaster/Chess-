import pygame
import board
from piece import Piece

# pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 480))
clock = pygame.time.Clock()
running = True
board = board.Board()

board.load_fen()
board.print_board(screen)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      board.mouse_down()
      board.load_fen()
        
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      board.mouse_up()
      board.update_fen()
      board.load_fen()

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  # RENDER YOUR GAME HERE
  board.print_board(screen)

  # flip() the display to put your work on screen
  pygame.display.flip()

  clock.tick(60)  # limits FPS to 60

pygame.quit()