import pygame
import board as b
import moves as m


pygame.display.set_caption("Dumb and Dumber Gambit, Blunder Variation: Chess")

def two_player_game(screen, clock):
    
  running = True
  board = b.Board()
  moves = m.Moves()
  board.load_fen()
  board.update_fen()
  board.print_board(screen)
  moves.generate_moves(board.board, board.FEN.split(" ")[1], board.FEN.split(" ")[2])

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        board.mouse_down()
        board.highlight_legal_moves(moves.legal_moves)
        board.load_fen()
          
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        board.mouse_up(moves)
        # board.update_fen()
        board.load_fen()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    board.print_board(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

  pygame.quit()