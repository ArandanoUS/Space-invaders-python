import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))


shape = [
'     xxxxxxxxxxx    ',
'   xxxxxxxxxxxxxxx  ',
'  xxx       xxxxxxxx',
' xxx   xxxxxxxxxxxxx',
' xxx              xx',
'xxx                 ']

""" #shape = [
'           xxxxxxxxxxx         ',
'         xxxxxxxxxxxxxxx       ',
'        xxx       xxxxxxxx     ',
'       xxx   xxxxxxxxxxxxxx    ',
'       xxx   xxxx       xxxxx  ',
'  xxxxxxx   xxxxx          xxx ',
' xxxxxxx    xxxxxxxxxxxxxxxxx  ',
' xxx  xxx    xxxxxxxxxxxxxxxx  ',
' xxx  xxx     xxxxxxxxxxxxxx   ',
' xxx  xxx                xxx   ',
' xxx  xxx                xxx   ',
' xxxx xxx                xxx   ',
'  xxxxxxx     xxxxxxxxxxxx     ',
'       xx     xxx xxxx  xxx    ',
'       xx     xxx xxx   xxx    ',
'       xxxxxxxxx  xxxxxxxx     ',
'       xxxxxxxxx               ']"""

