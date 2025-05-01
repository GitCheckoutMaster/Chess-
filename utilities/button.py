class Button:
  def __init__(self, pos, text, font, color, hovering_color, image=None):
    self.x_pos = pos[0]
    self.y_pos = pos[1]
    self.text_input = text
    self.font = font
    self.text = self.font.render(text, True, color)
    self.base_color = color
    self.hovering_color = hovering_color
    if image is not None:
      self.image = image
    else:
      self.image = self.text

    self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
  
  def update(self, screen):
    if self.image:
      screen.blit(self.image, self.rect)
    screen.blit(self.text, self.text_rect)

  
  def check_for_input(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
      return True
    return False
  
  def change_color(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
      self.text = self.font.render(self.text_input, True, self.hovering_color)
    else:
      self.text = self.font.render(self.text_input, True, self.base_color)
  
