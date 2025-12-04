import pygame

class Physik:
   def __init__(self, game, e_type, pos, size):
      self.game = game
      self.type = e_type
      self.pos = list(pos)
      self.size = size
      self.velocity = [0, 0] 

   def movement(self, movement=(0, 0)):
      frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) #bewegung + geschwindigkeit = gesamt bewegung

      self.pos[0] += frame_movement[0] #x bewegung
      self.pos[1] += frame_movement[1] #y bewegung
   
   def render(self, surface):
      #TODO: change to blit later am besten mit:
      """surf.blit(self.game.assets['player'], self.pos)"""
      pygame.draw.rect(surface, (255, 255, 255), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
      
