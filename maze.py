from pygame import *
mixer.init()
font.init()
window = display.set_mode((700,500))
display.set_caption('Лабиринт')
class GameSprite(sprite.Sprite):
    def __init__(self,images,speed,x,y):
        super().__init__()
        self.image = transform.scale(image.load(images),(70,70))
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
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 395:
            self.rect.y += self.speed
class Enemy(GameSprite):
    def __init__(self,images,speed,x,y):
        super().__init__(images,speed,x,y)
        self.direction = 'left'
    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
            if self.rect.x <= 450:
                self.direction = 'right'
        elif self.direction == 'right':
            self.rect.x += self.speed
            if self.rect.x >= 595:
                self.direction = 'left'
class Wall(sprite.Sprite):
    def __init__(self,colors,width,height,x,y):
        super().__init__()
        self.colors = colors
        self.width = width
        self.height = height
        self.image = Surface((width,height))
        self.image.fill(colors)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
font = font.SysFont('Arial', 70)
win = font.render('You win!', True, (255, 254, 5))
defeat = font.render('Lose', True, (5, 193, 255))
health = 3
healthbar = font.render(str(health), True, (255, 255, 255))
background = transform.scale(image.load('background.jpg'),(700,500))
treasure = GameSprite('treasure.png',0,500,400)
sprite1 = Player('hero.png', 4, 20,400)
sprite2 = Enemy('cyborg.png',3, 460,300)
wall1 = Wall((245, 60, 87),10,400,130,120)
wall2 = Wall((245, 60, 87),150,10,100,0)
wall3 = Wall((245, 60, 87),10,350,240,10)
wall4 = Wall((245, 60, 87),100,10,340,350)
wall5 = Wall((245, 60, 87),10,400,430,150)
wall6 = Wall((245, 60, 87),10,250,340,0)
wall7 = Wall((245, 60, 87),10,500,650,0)
game = True
finish = False
clock = time.Clock()
FPS = 60
x1 = 100
y1 = 400
while game:
    window.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        sprite1.update()
        sprite2.update()
        sprite2.reset()
        treasure.reset()
        sprite1.reset()
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        wall7.draw_wall()
        if sprite.collide_rect(sprite1, treasure):
            window.blit(win, (200, 200))
            money.play()
            finish = True
        if sprite.collide_rect(sprite1, sprite2) or sprite.collide_rect(sprite1, wall1) or sprite.collide_rect(sprite1, wall2) or sprite.collide_rect(sprite1, wall3) or sprite.collide_rect(sprite1, wall4) or sprite.collide_rect(sprite1, wall5) or sprite.collide_rect(sprite1, wall6) or sprite.collide_rect(sprite1, wall7):
            kick.play()
            health -= 1
            healthbar = font.render(str(health), True, (255, 255, 255))
            sprite1.rect.x = 20
            sprite1.rect.y = 400
            if health == 0:
                window.blit(defeat, (200, 200))
                finish = True      
        window.blit(healthbar, (20,20))
        clock.tick(FPS)
        display.update()