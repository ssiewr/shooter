from pygame import *
from random import randint
from time import time as timer
import sys
import os
 
WIDTH = 700
HEIGHT = 500
FPS = 60
 
LOST = 0
SCORE = 0
 
MAX_LOST = 10
MAX_SCORE = 20
#iuytr
LIFE = 3
 
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)
 
image_folder = resource_path(".")
 
mixer.init()
 
back_music = os.path.join(image_folder, "space.ogg")
mixer.music.load(back_music)
 
mixer.music.set_volume(0.1)
 
f_sound = os.path.join(image_folder, "fire.ogg")
fire_sound = mixer.Sound(f_sound)
 
img_back = os.path.join(image_folder, "galaxy.jpg")
img_hero = os.path.join(image_folder, "rocket.png")
img_monster = os.path.join(image_folder, "ufo.png")
img_bullet = os.path.join(image_folder,"bullet.png")
img_ast = os.path.join(image_folder,"asteroid.png")
 
font.init()
 
font2 = font.Font(None, 36)
font3 = font.Font(None, 70)
 
win = font2.render("YOU WIN!!!", True, (255, 255, 255))
lose = font2.render("YOU LOSE!!!", True, (180, 0, 0))
 
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (WIDTH, HEIGHT))
 
clock = time.Clock()
 
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
class Enemy(GameSprite):
    def update(self):
        global LOST
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(80, WIDTH - 80)
            self.rect.y = 0
            LOST += 1
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
 
 
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
 
ship = Player(img_hero, 5, HEIGHT - 100, 80, 100, 10)
 
for i in range(1, 6):
    monster = Enemy(img_monster, randint(80, WIDTH - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
for i in range(1, 3):
    ansteroid = Enemy(img_ast, randint(30, WIDTH - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(ansteroid)
 
num_fire = 0
rel_time = False # Перезарядка
run = True
finish = False
 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time: # rel_time == False
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
 
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True
 
    if not finish:
        window.blit(background, (0, 0))
 
        ship.update()
        ship.reset()
 
        monsters.update()
        monsters.draw(window)
 
        bullets.update()
        bullets.draw(window)
 
        asteroids.update()
        asteroids.draw(window)
 
        if rel_time:
            now_time = timer()
 
            if now_time - last_time < 3:
                reload_txt = font2.render("Перезарядка...", True, (150, 0, 0))
                window.blit(reload_txt, (260, 460))
            else:
                num_fire = 0
                rel_time = False
 
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            SCORE += 1
            monster = Enemy(img_monster, randint(80, WIDTH - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)   
 
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False): # Проигрыш
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            LIFE -= 1
 
        if LIFE == 0 or LOST >= MAX_LOST:
            finish = True
            window.blit(lose, (200, 200))
 
        if SCORE >= MAX_SCORE: # Выигрыш
            finish = True 
            window.blit(win, (200, 200))
 
        text_score = font2.render(f"Счёт: {SCORE}", True, (255, 255, 255))
        window.blit(text_score, (10, 20))
 
        text_lost = font2.render(f"Пропущено: {LOST}", True, (255, 255, 255))
        window.blit(text_lost, (10, 50))
        if LIFE == 3:
            life_color = (0, 150, 0)
        if LIFE == 2:
            life_color = (150, 150, 0)
        if LIFE == 1:
            life_color = (150, 0, 0)
 
        text_life = font2.render(str(LIFE), 1, life_color)
        window.blit(text_life, (650, 10))
 
        display.update()
 
    else:
        finish = False
        SCORE = 0
        LOST = 0
        num_fire = 0
        LIFE = 3
 
        for b in bullets:
            b.kill()
 
        for m in monsters:
            m.kill()
 
        for a in asteroids:
            a.kill()
 
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_monster, randint(80, WIDTH - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
 
        for i in range(1, 3):
            ansteroid = Enemy(img_ast, randint(30, WIDTH - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(ansteroid) 
 
    time.delay(50)