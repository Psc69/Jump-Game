import pygame, sys

WIDTH, HEIGHT = 800, 600 #fenster größe
FPS = 60 #bilder pro sekunde


class Game:
   def __init__(self):
      pygame.init()

      #fenster titel
      pygame.display.set_caption("jump game")

      #fenster größe
      self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
      self.display = pygame.Surface((WIDTH/2, HEIGHT/2))

      #fps steuerung
      self.clock = pygame.time.Clock()

      #orte vom bildschirm
      self.centerofscreen_x = (self.display.get_width()) // 2
      def centerofscreen_x(input):
         return self.centerofscreen_x - input // 2
      self.centerofscreen_y = (self.display.get_height()) // 2
      def centerofscreen_y(input):
         return self.centerofscreen_y - input // 2

      #spieler
      self.playerBreite, self.playerHöhe = 25, 45 
      self.playerX, self.playerY = centerofscreen_x(self.playerBreite), 50 
      self.player = pygame.Rect(self.playerX, self.playerY, self.playerBreite, self.playerHöhe)
      self.velocity_y = 0
      self.flip = False


      #boden 
      self.groundBreite, self.groundHöhe = 300, 25
      self.groundX, self.groundY = centerofscreen_x(self.groundBreite), self.display.get_height() - 50
      self.ground = pygame.Rect(self.groundX, self.groundY, self.groundBreite, self.groundHöhe)

      #decke
      self.ceilingBreite, self.ceilingHöhe = 300, 25
      self.ceilingX, self.ceilingY = centerofscreen_x(self.ceilingBreite), +60
      self.ceiling = pygame.Rect(self.ceilingX, self.ceilingY, self.ceilingBreite, self.ceilingHöhe)

      #physik variablen
      self.GRAVITY = 0.25

      #farben variablen
      self.BG = (200, 180, 150) #hintergrund farbe
      self.WEISS = (255, 255, 255) #spieler farbe
      self.SCHWARZ = (0, 0, 0) #ground farbe
      self.ROT = (255, 0, 0) #ROT

   #platform
   def tile (self, x, y):
      return pygame.Rect(x, y, 50, 50)
   
   def update(self):
      #reset bewegung
      self.velocity_x = 0

      #apply gravity
      self.velocity_y += self.GRAVITY
      
      #move player vertically
      self.player.y += self.velocity_y

      #ceiling collider
      self.player.head = pygame.Rect( #x, y, breite, höhe
         self.player.x,
         self.player.bottom,
         self.player.width,
         5
      )

      #feet collider
      self.player_feet = pygame.Rect( #x, y, breite, höhe
         self.player.x,
         self.player.bottom,
         self.player.width,
         5
      )

      #ground collision
      if self.player_feet.colliderect(self.ground) and self.velocity_y >= 0:
         self.player.bottom = self.ground.top
         self.velocity_y = 0
         self.on_ground = True
      else:
         self.on_ground = False

      key = pygame.key.get_pressed()
      if key[pygame.K_d] or key[pygame.K_RIGHT]:
         self.velocity_x = 3
      elif key[pygame.K_a] or key[pygame.K_LEFT]:
         self.velocity_x = -3   

      #move player horizontal
      self.player.x += self.velocity_x

      #jump
      if key[pygame.K_SPACE] and self.on_ground:
         self.velocity_y += -8 

      
      

   def draw(self):
      #hintergrund farbe
      self.display.fill(self.BG)

      #draw it
      pygame.draw.rect(self.display, self.WEISS, self.player) #player
      pygame.draw.rect(self.display, self.SCHWARZ, self.ground) #ground
      pygame.draw.rect(self.display, self.SCHWARZ, self.ceiling) #ceiling
      pygame.draw.rect(self.display, self.ROT, self.player_feet) #player füße
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

         print(self.velocity_y)
         if pygame.key.get_pressed()[pygame.K_SPACE]:
            print("SPRINGE")
      
         self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #skalierung
         self.clock.tick(FPS) #FPS

if __name__ == '__main__':
   game = Game()
   game.run()