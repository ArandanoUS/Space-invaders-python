import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = './graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if color == 'red': 
            self.value = 100
            self.health = 1
        elif color == 'yellow': 
            self.value = 200
            self.health = 2
        else: 
            self.value = 300
            self.health = 3


    def update(self,direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('./graphics/extra.png').convert_alpha()

        if side == 'right':
            x = screen_width + 50
            self.speed = -5
        else:
            x = -50
            self.speed = 5

        self.rect = self.image.get_rect(topleft = (x,80))

    def update(self):
        self.rect.x += self.speed