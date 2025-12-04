import pygame, sys

from scripts.tilemap import TileMap
from scripts.camera import Camera

WIDTH, HEIGHT = 1600, 900 #fenster größe
FPS = 60 #bilder pro sekunde


class Game:
   def __init__(self):
      pygame.init()

      #fenster titel
      pygame.display.set_caption("jump game")

      #fenster größe
      self.zoom = 2
      self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
      self.display = pygame.Surface((WIDTH/self.zoom, HEIGHT/self.zoom))

      #fps steuerung
      self.clock = pygame.time.Clock()

      #orte vom bildschirm
      self.centerofscreen_x = (self.display.get_width()) // 2
      def centerofscreen_x(input):
         return self.centerofscreen_x - input // 2
      self.centerofscreen_y = (self.display.get_height()) // 2
      def centerofscreen_y(input):
         return self.centerofscreen_y - input // 2

      #gui
      self.font = pygame.font.SysFont(None, 32)

      #spieler
      self.playerSize = [35, 65]
      self.playerPos = [centerofscreen_x(self.playerSize[0]), 50]
      self.player = pygame.Rect(self.playerPos[0], self.playerPos[1], self.playerSize[0], self.playerSize[1])
      self.JUMP_STRENGTH = -9
      self.velocity_y = 0
      self.flip = False
      self.show_hitboxes = False

      #demo level
      demo_level = [
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
         [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0],
         [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
      ]
      demo_level1 = [
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
      ]

      #Tilemap
      self.level = TileMap(32, demo_level1, self.display)

      # Camera
      self.camera = Camera(self.display.get_width(), self.display.get_height())

      #physik variablen
      self.GRAVITY = 0.25

      #farben variablen
      self.BG = (200, 180, 150) #hintergrund farbe
      self.WEISS = (255, 255, 255) #spieler farbe
      self.SCHWARZ = (0, 0, 0) #ground farbe
      self.ROT = (255, 0, 0) #ROT
   
   def update(self):
      #reset bewegung
      self.velocity_x = 0

      #apply gravity
      self.velocity_y += self.GRAVITY

      #move player vertically
      self.player.y += self.velocity_y

      #key inputs
      key = pygame.key.get_pressed()
      if key[pygame.K_d] or key[pygame.K_RIGHT]:
         self.velocity_x = 4
         self.flip = False
      elif key[pygame.K_a] or key[pygame.K_LEFT]:
         self.velocity_x = -4   
         self.flip = True
         
      #move player horizontal
      self.player.x += self.velocity_x

      #feet collider
      self.player_feet = pygame.Rect( #x, y, breite, höhe
         self.player.x,
         self.player.bottom,
         self.player.width,
         5
      )

      #head collider
      self.player_head = pygame.Rect( #x, y, breite, höhe
         self.player.x,
         self.player.top - 5,
         self.player.width,
         5
      )

      #left collider
      self.player_left = pygame.Rect( #x, y, breite, höhe
         self.player.left - 5,
         self.player.y,
         5,
         self.player.height 
      )

      #right collider
      self.player_right = pygame.Rect( #x, y, breite, höhe
         self.player.right ,
         self.player.y,
         5,
         self.player.height 
      )

      #tile collision
      self.on_ground = False
      self.on_head = False
      self.PUSH_OUT = 5
      for tile_rect in self.level.get_collision_rects():
         #füße
         if self.player_feet.colliderect(tile_rect) and self.velocity_y >= 0:
            self.player.bottom = tile_rect.top
            self.velocity_y = 0
            self.on_ground = True
            break
         #kopf
         if self.player_head.colliderect(tile_rect) and self.velocity_y < 0:
            self.player.top = tile_rect.bottom + self.PUSH_OUT
            self.velocity_y = 0
            self.on_head = True
            break
         #links
         if self.player_left.colliderect(tile_rect) and self.velocity_x < 0:
            self.player.left = tile_rect.right + self.PUSH_OUT
            self.velocity_x = 0
         #rechts
         if self.player_right.colliderect(tile_rect) and self.velocity_x > 0:
            self.player.right = tile_rect.left - self.PUSH_OUT
            self.velocity_x = 0



      # Update camera to follow player
      self.camera.follow(self.player)

      #jump
      if key[pygame.K_SPACE] and self.on_ground:
         self.velocity_y += self.JUMP_STRENGTH

      #hitboxen anzeigen
      if key[pygame.K_h]:
         self.show_hitboxes = not self.show_hitboxes
         pygame.time.delay(250) #verzögerung damit es nicht zu schnell umschaltet

      #respawn funktion
      if self.player.y > 500:
         self.player.x = self.playerPos[0]
         self.player.y = self.playerPos[1]
         self.velocity_y = 0
      elif pygame.key.get_pressed()[pygame.K_r]:
         self.player.x = self.playerPos[0]
         self.player.y = self.playerPos[1]
         self.velocity_y = 0

   def draw(self):
      #hintergrund farbe
      self.display.fill(self.BG)

      #tilemap with camera offset
      self.level.draw(self.display, self.camera.offset) #tilemap

      #draw player with camera offset
      player_draw_rect = self.player.copy()
      player_draw_rect.x -= self.camera.offset.x
      player_draw_rect.y -= self.camera.offset.y
      pygame.draw.rect(self.display, self.WEISS, player_draw_rect) #spieler

      def show_hitbox(rect, color):
         draw_rect = rect.copy()
         draw_rect.x -= self.camera.offset.x
         draw_rect.y -= self.camera.offset.y
         pygame.draw.rect(self.display, color, draw_rect, 5)

      if self.show_hitboxes:
         show_hitbox(self.player_feet, (0, 255, 0)) #player füße
         show_hitbox(self.player_head, (0, 0, 255)) #player kopf
         show_hitbox(self.player_left, (255, 255, 0)) #player links
         show_hitbox(self.player_right, (255, 0, 255)) #player rechts

      #gui
      fps_text = self.font.render(f'FPS: {int(self.clock.get_fps())}', True, (0, 0, 0))
      self.display.blit(fps_text, (10, 10))

      pos_text = self.font.render(f'Pos: {self.player.x}, {self.player.y}', True, (0, 0, 0))
      self.display.blit(pos_text, (10, 40))

      pygame.display.flip() #bildschirm aktualisieren

   #game schleife
   def run(self):
      while True:
         for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               pygame.quit()
               sys.exit()
               

         self.update()
         self.draw()
      
         self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #skalierung
         self.clock.tick(FPS) #FPS

if __name__ == '__main__':
   game = Game()
   game.run()