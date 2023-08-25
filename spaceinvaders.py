import pygame, sys
from player import Player
from alien import Alien, Extra
import obstacle
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        #player setup
        player_sprite = Player((screen_width/2, screen_height), screen_width, screen_height,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #health and score
        self.lives = 3
        self.live_surf = pygame.image.load('./graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]*2 +20)
        self.score = 0
        self.font = pygame.font.Font('./graphics/font.ttf',20)


        #obstacle setup
        self.shape = obstacle.shape
        self.block_size = 5
        self.blocks = pygame.sprite.Group()
        self.block_color = 'red'
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width/ self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start= screen_width/40, y_start=480)

        #alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=5, cols=3)
            
        self.alien_direction = 2
        self.stage_num =1
        

        #extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(50, 100)

        #audio setup
        music = pygame.mixer.Sound('./graphics/music.wav')
        music.set_volume(0.1)
        music.play(loops=-1)


    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index *self.block_size
                    block = obstacle.Block(self.block_size,self.block_color,x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_offset=70, y_offset=30, x_distance = 60,y_distance=48):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: 
                    alien_sprite = Alien('green', x,y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('yellow', x,y)
                else:
                    alien_sprite = Alien('red', x,y)
                self.aliens.add(alien_sprite)

    def alien_setup2(self, rows, cols, x_offset=70, y_offset=50, x_distance = 60,y_distance=48):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index % 3 == 0: 
                    alien_sprite = Alien('red', x,y)
                elif row_index % 3 == 1:
                    alien_sprite = Alien('green', x,y)
                elif row_index % 3 == 2:
                    alien_sprite = Alien('yellow', x,y)
                self.aliens.add(alien_sprite)

    def alien_setup3(self, rows, cols, x_offset=70, y_offset=50, x_distance = 60,y_distance=48):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index % 3 == 0: 
                    alien_sprite = Alien('red', x,y)
                elif row_index % 3 == 1:
                    alien_sprite = Alien('green', x,y)
                elif row_index % 3 == 2:
                    alien_sprite = Alien('yellow', x,y)
                self.aliens.add(alien_sprite)

    def alien_position_check(self):
        
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                if self.stage_num ==1:
                    self.alien_direction = -2
                    self.alien_down(3)
                elif self.stage_num ==2:
                    self.alien_direction = -3
                    self.alien_down(2)
                else:
                    self.alien_direction = -6
                    self.alien_down(2)
            elif alien.rect.left <= 0:
                if self.stage_num ==1:
                    self.alien_direction = 2
                    self.alien_down(3)
                elif self.stage_num ==2:
                    self.alien_direction = 3
                    self.alien_down(2)
                else:
                    self.alien_direction = 6
                    self.alien_down(2)

 
    def alien_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),screen_width))
            self.extra_spawn_time = randint(400,800)

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)

    def collision_check(self):
        #player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                    
                    
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,False)    
                if aliens_hit:
                    for alien in aliens_hit:
                        alien.health -= 1
                        if alien.health <= 0:
                            alien.kill()
                            self.score += alien.value
                            music = pygame.mixer.Sound('./graphics/explosion.wav')
                            music.set_volume(0.3)
                            music.play(loops=0)
                    laser.kill()
                    

                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.score +=500

        #alien laser            
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                    

                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()


        #aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live* (self.live_surf.get_size()[0]+10))
            screen.blit(self.live_surf,(x,8))

    def next_stage(self):
        if not self.aliens.sprites():
                victory_surf = self.font.render("Credits", False, 'white')
                victory_rect = victory_surf.get_rect(center = (screen_width/2, screen_height/2 -120))
                screen.blit(victory_surf, victory_rect)
                victory_surf2 = self.font.render("Daniel Caballero", False, 'white')
                victory_rect2 = victory_surf.get_rect(center = (screen_width/2-30, screen_height/2 -60))
                screen.blit(victory_surf2, victory_rect2)
                victory_surf3 = self.font.render("Diego Hernandez", False, 'white')
                victory_rect3 = victory_surf.get_rect(center = (screen_width/2-30, screen_height/2-20))
                screen.blit(victory_surf3, victory_rect3)
                victory_surf4 = self.font.render("Emanuel Santos", False, 'white')
                victory_rect4 = victory_surf.get_rect(center = (screen_width/2-30, screen_height/2+20))
                screen.blit(victory_surf4, victory_rect4)
                victory_surf5 = self.font.render("Cristian Diaz", False, 'white')
                victory_rect5 = victory_surf.get_rect(center = (screen_width/2-30, screen_height/2+60))
                screen.blit(victory_surf5, victory_rect5)

    def main_menu(self):
        menu_surf = self.font.render('Press space to start', False, 'white')
        menu_rect = menu_surf.get_rect(center = (screen_width/2, screen_height/2))
        screen.blit(menu_surf, menu_rect)

    def run_stage1(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.extra.update()
        self.alien_position_check()
        self.alien_lasers.update()
        self.extra_alien_timer()
        
        self.collision_check()

        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_score()
        self.display_lives()
        self.next_stage()

        



if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600 
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    game_started = False



    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)


    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    
            if event.type  == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        if game_started == False:
            game.main_menu()
        else:
            game.run_stage1()

        pygame.display.flip()
        clock.tick(60)

