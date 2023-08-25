import pygame
from laser import Laser 

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,constraintx,constrainty,speed):
            super().__init__()
            self.image = pygame.image.load('./graphics/player.png').convert_alpha()
            self.rect = self.image.get_rect(midbottom = pos)
            self.speed = speed
            self.max_x_constraint = constraintx
            self.max_y_constraint = constrainty
            self.ready = True
            self.laser_time = 0
            self.laser_cooldown = 600

            self.lasers = pygame.sprite.Group()
            

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
        
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            music = pygame.mixer.Sound('./graphics/laser.wav')
            music.set_volume(0.2)
            music.play(loops=0)

            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time =pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                 self.ready = True


    def constraintx(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
             self.rect.right = self.max_x_constraint

    def constrainty(self):
        if self.rect.bottom >= self.max_y_constraint:
            self.rect.bottom = self.max_y_constraint
        if self.rect.top <= 400:
             self.rect.top = 400

    def shoot_laser(self):
         self.lasers.add(Laser(self.rect.center,-8, self.rect.bottom))

    def update(self):
         self.get_input()
         self.constraintx()
         self.constrainty()
         self.recharge()
         self.lasers.update()
         

