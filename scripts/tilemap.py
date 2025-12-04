import pygame

SCHWARZ = (50, 50, 50) 

class TileMap:

   def __init__(self, tile_size, map_data, display):
      # Calculate tile size to fit the window
      self.tile_size = min(
         display.get_width() // len(map_data[0]),
         display.get_height() // len(map_data)
      )
      self.map_data = map_data
      self.display = display
      self.tiles = self.create_tilemap()

   def create_tilemap(self):
      tiles = []
      rows = len(self.map_data)
      cols = len(self.map_data[0])
      # Start from bottom left
      for row_index, row in enumerate(self.map_data):
         for col_index, tile in enumerate(row):
            if tile == 1:  # Assuming 1 represents a solid tile
               x = col_index * self.tile_size
               # Flip the row index so bottom row is at bottom of screen
               y = self.display.get_height() - (rows - row_index) * self.tile_size
               rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
               tiles.append(rect)
      return tiles

   def draw(self, surface, camera_offset=None):
      for tile in self.tiles:
         draw_rect = tile.copy()
         if camera_offset:
            draw_rect.x -= camera_offset.x
            draw_rect.y -= camera_offset.y
         pygame.draw.rect(surface, SCHWARZ, draw_rect)  # Draw tiles in schwarz 

   def get_collision_rects(self):
      # Returns all tile rects for collision detection
      return self.tiles
