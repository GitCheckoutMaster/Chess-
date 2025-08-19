import random

class Engine:
  def __init__(self, depth=0):
    self.depth = depth
  

  @staticmethod
  def random_move_picker(all_moves):

    filtered = {k: v for k, v in all_moves.items() if v}

    source = random.choice(list(filtered.keys()))
    target = random.choice(filtered[source])

    return [source, target]