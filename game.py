import pygame, sys
from physik import Physics

WIDTH, HEIGHT = 800, 600 #fenster größe

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

      #boden 
      self.groundBreite, self.groundHöhe = 300, 25
      self.groundX, self.groundY = centerofscreen_x(self.groundBreite), self.display.get_height() - 50
      self.ground = pygame.Rect(self.groundX, self.groundY, self.groundBreite, self.groundHöhe)

      #physik variablen
      self.GRAVITY = 0.25

      #farben variablen
      self.BG = (200, 180, 150) #hintergrund farbe
      self.WEISS = (255, 255, 255) #spieler farbe
      self.SCHWARZ = (0, 0, 0) #ground farbe
   
   def update(self):
      #apply gravity
      self.velocity_y += self.GRAVITY
      self.player.y += self.velocity_y

      #ground collision
      if self.player.colliderect(self.ground):
         self.player.bottom = self.ground.top
         self.velocity_y = 0
      

   def draw(self):
      #hintergrund farbe
      self.display.fill(self.BG)

      #draw it
      pygame.draw.rect(self.display, self.WEISS, self.player) #player
      pygame.draw.rect(self.display, self.SCHWARZ, self.ground) #ground
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
         self.clock.tick(60) #FPS

if __name__ == '__main__':
   game = Game()
   game.run()