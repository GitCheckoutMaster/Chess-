import pygame
from two_player_chess import two_player_game
from zero_elo_bot import zero_elo_opponent
from utilities.button import Button

# pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 480))
clock = pygame.time.Clock()
pygame.display.set_caption("Dumb and Dumber Gambit, Blunder Variation: Chess")


def main_menu():
  # Main menu setup
  screen.fill((0, 0, 0))
  font = pygame.font.Font(None, 74)
  title_text = font.render("Chess", True, (255, 255, 255))
  title_rect = title_text.get_rect(center=(240, 100))

  # Button setup
  button_font = pygame.font.Font(None, 36)
  two_player_button = Button((240, 200), "Two Player", button_font, (255, 255, 255), (200, 200, 200))
  one_player_button = Button((240, 300), "Dumb and Dumber", button_font, (255, 255, 255), (200, 200, 200))
  quit_button = Button((240, 400), "Quit", button_font, (255, 255, 255), (200, 200, 200))
  
  # Main menu loop
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if event.type == pygame.MOUSEBUTTONDOWN:
        if two_player_button.check_for_input(pygame.mouse.get_pos()):
          two_player_chess()
        elif one_player_button.check_for_input(pygame.mouse.get_pos()):
          one_player_chess()
        elif quit_button.check_for_input(pygame.mouse.get_pos()):
          running = False

    screen.fill((0, 0, 0))
    screen.blit(title_text, title_rect)

    for button in [two_player_button, one_player_button, quit_button]:
      button.change_color(pygame.mouse.get_pos())
      button.update(screen)

    pygame.display.flip()
    clock.tick(60)

def two_player_chess(): 
  two_player_game(screen, clock)

def one_player_chess():
  zero_elo_opponent(screen, clock)

def import_in_chess():
  pass

main_menu()
# two_player_chess()