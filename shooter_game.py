#Создай собственный Шутер!
from pygame import *
from random import randint
import time as timer
mixer.init()
font.init()
window = display.set_mode((700,500))
display.set_caption('Spacewar')
class GameSprite(sprite.Sprite):
    def __init__(self,images,speed,x,y,width,height):
        super().__init__()
        self.image = transform.scale(image.load(images),(width,height))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 695:
            self.rect.x += self.speed
        self.reset()
    def fire(self):
            self.bullet = Bullet('bullet.png',8,self.rect.centerx,self.rect.top,10,15)
            bullets.add(self.bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 495:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(30,650)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            bullets.remove(self)
class Asteroid(GameSprite):
    def update(self):
        if self.rect.y < 495:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(30,650)
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
background = transform.scale(image.load('kosmos.jpg'), (700,500))
clock = time.Clock()
spaceship = Player('rocket.png',8,300,400,50,50)
enemys = sprite.Group()
new_font = font.SysFont('Verdana', 20)
font3 = font.SysFont('Verdana', 30)
font2 = font.SysFont('Verdana', 10)
nfont = font.SysFont('Verdana', 70)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(2):
    asteroid1 = Asteroid('asteroid.png',randint(2,3),randint(30,650),0,60,60)
    asteroids.add(asteroid1)
num_bul = 5
lost = 0
crush = 0
lives = 3
for i in range(5):
    enemy = Enemy('ufo.png',randint(1,2),randint(30,650),0,75,60)
    enemys.add(enemy)
game = True
finished = False
reloading = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_bul > 0:
                    spaceship.fire()
                    fire.play()
                    num_bul -= 1
                elif num_bul <= 0 and reloading == False:
                    reloading = True
                    r_time = timer.time()
    if not finished:
        window.blit(background,(0,0))
        crushed = new_font.render('Сбитых: '+ str(crush), True, (255, 255, 255))
        losted = new_font.render('Пропущенных: ' + str(lost), True, (255, 255, 255))
        live = font3.render('Здоровье: '+ str(lives),True,(255,255,255))
        spaceship.update()
        bullets.draw(window)
        bullets.update()
        enemys.draw(window)
        asteroids.draw(window)
        asteroids.update()
        sprite_group = sprite.spritecollide(spaceship,enemys,True)
        sprite_group2 = sprite.groupcollide(bullets,enemys,True,True)
        sprite_group3 = sprite.spritecollide(spaceship,asteroids,True)
        for sprit in sprite_group:
            lives -= 1
            enemy = Enemy('ufo.png',randint(2,3),randint(30,650),0,75,60)
            enemys.add(enemy)
        for asteroid in sprite_group3:
            lives -= 1
            asteroid1 = Asteroid('asteroid.png',randint(2,3),randint(30,650),0,60,60)
            asteroids.add(asteroid1)
        if lives < 1 or lost >= 30:
            live = font3.render('Здоровье: '+ str(lives),True,(255,255,255))
            lose = nfont.render('You lose', True, (255,255,255))
            window.blit(lose,(200,200))
            finished = True
        elif crush >= 5000:
            win = nfont.render('You win', True, (255,255,255))
            window.blit(win, (200,200))
            finished = True
        for sprited in sprite_group2:
            crush += randint(1,4)*100
            crushed = new_font.render('Сбитых: '+ str(crush), True, (255, 255, 255))
            enemy = Enemy('ufo.png',randint(2,3),randint(30,650),0,75,60)
            enemys.add(enemy)
        if reloading is True:
            cur_time = timer.time()
            if cur_time-r_time < 2:
                reloadL = font2.render('Перезарядка:'+str(int(cur_time-r_time)),True, (255,255,255))
                window.blit(reloadL, (spaceship.rect.centerx-20,spaceship.rect.y+5))
            else:
                reloading = False
                num_bul = 5
        window.blit(live, (450,10))
        window.blit(crushed, (10,10))
        window.blit(losted, (10,30))
        enemys.update()
        clock.tick(60)
        display.update()