import os
import math
import time
import random
import pygame
import csv
from pygame.locals import *
from pygame import mixer
pygame.init()
 #This is the game loop. The game will run when this variable is True, and close when it is False.

red_space_ship = pygame.image.load(os.path.join(r"C:\Users\167378\OneDrive - UAT\Alevels\Comp\Comp 3\c3_project\Proj_app\assets\pixel_ship_red_small.png"))
#Loads Image for red spaceship
pygame.display.set_caption("Space Shooter Game")
player_ship = pygame.image.load(os.path.join(r"C:\Users\167378\OneDrive - UAT\Alevels\Comp\Comp 3\c3_project\Proj_app\assets\player_ship.png"))

mixer.init()
mixer.music.load("COMP3_BGM2.WAV")
mixer.music.play(-1)
pygame.font.init()
#This code initialises the music player in Pygame. 
#It loads the background music file and loops it while the game is running

WIDTH, HEIGHT = 1200, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
# The code above creates the game window, at the height specified by the variables "WIDTH" and "HEIGHT". 
# It also loads a background image, scaled to the size of the game window.

class Laser:
    def __init__(self, x, y, img):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.laser = pygame.Surface((7, 2)).convert_alpha()
        self.laser.fill((50, 205, 50))
        self.laser = pygame.transform.rotate(self.laser, angle)
        self.speed = 2

    def draw(self, surf):
        laser_rect = self.laser.get_rect(center = self.pos)
        surf.blit(self.laser, laser_rect)

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed)
    
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    cooldown = 10
    
    def __init__(self, x, y, health = 3):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = player_ship
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
      
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        for laser in self.lasers:
            self.lasers.append(Laser(*pos))
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collison(obj):
                obj.health = obj.health - 1
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cooldown_counter >= self.cooldown:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter = self.cooldown_counter + 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.pos, self.dir)
            self.lasers.append(lasers)
            self.cooldown_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 3):
        super().__init__(x, y, health)
        self.ship_img = player_ship
      
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

        def move_lasers(self,vel, objs):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(height):
                    self.lasers.remove(laser)
                else:
                    for obj in objs:
                        if laser.collison(obj):
                            objs.remove(obj)
                            score = score + 1
                            if laser in self.lasers:
                                self.lasers.remove(lasers)
                                
        def draw(self, window):
            super().draw(window)
            self.healthbar(window)

        def healthbar(self, window):
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    def __init__(self, x, y, colour, health = 1):
        super().__init__(x, y, health)
        self.mask = pygame.mask.from_surface(red_space_ship)
        
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1
            
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    
class Asteroid:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        if t == "Large":
            self.size = 30
        elif t == "Normal":
            self.size = 20
        else:
            self.size = 10
        self.t = t

        # Make random speed and direction
        self.speed = random.uniform(1, (40 - self.size) * 4 / 15)
        self.dir = random.randrange(0, 360) * math.pi / 180

        # Make random asteroid sprites
        full_circle = random.uniform(18, 36)
        dist = random.uniform(self.size / 2, self.size)
        self.vertices = []
        while full_circle < 360:
            self.vertices.append([dist, full_circle])
            dist = random.uniform(self.size / 2, self.size)
            full_circle += random.uniform(18, 36)

    def updateAsteroid(self):
        # Move asteroid
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)

        # Check for wrapping
        if self.x > display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width
        elif self.y > display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height

        # Draw asteroid
        for v in range(len(self.vertices)):
            if v == len(self.vertices) - 1:
                next_v = self.vertices[0]
            else:
                next_v = self.vertices[v + 1]
            this_v = self.vertices[v]
            pygame.draw.line(gameDisplay, white, (self.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                                                  self.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                             (self.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                              self.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))


def main():
    run = True
    FPS = 60
    lives = 1
    level = 0
    main_font = pygame.font.SysFont("ostrich-sans.ttf", 50)
    lost_font = pygame.font.SysFont("ANGELIC.ttf", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 2
    player_vel = 5
    laser_vel = 5

    player = Player(150, 315)

    clock = pygame.time.Clock()
    lost = False
    lost_count = 0


    def redraw_window():
        win.blit(bg, (0,0))
        lives_label = main_font.render(f"LIVES: {lives}", 1,  (255,255,255))
        win.blit(lives_label, (10, 10))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

        if lost:
            lost_label = lost_font.render("<<<YOU HAVE FAILED THE MISSION>>>", 1, (255,255,255))
            win.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
        #Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel # Moves the player's ship left
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() <  WIDTH: 
            player.x += player_vel # Moves the player's ship right
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel # Moves the player's ship up
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel # Moves the player's ship down
        if keys[pygame.K_SPACE]:
            player.shoot()

        if keys[pygame.K_ESCAPE]:
            run = False
            pygame.quit()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

        if random.randrange(0, 2*60) == 1:
                enemy.shoot()

        if collide(enemy, player):
                player.health -= 0
                enemies.remove(enemy)
        elif enemy.y + enemy.get_height() > HEIGHT:
            lives -= 1
            enemies.remove(enemy)

        








def main_menu():
    title_font = pygame.font.SysFont("ostrich-regular.ttf", 70)
    run = True
    while run:
        win.blit(bg, (0,0))
        title_label = title_font.render("PRESS ENTER TO BEGIN:", 1, (255,255,255))
        win.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()

        

main_menu()
