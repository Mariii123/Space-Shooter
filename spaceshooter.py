import pygame,random,time,sys
from os import path
pygame.init()
black=(0,0,0)
red=(255,0,0)
white=(255,255,255)
yellow=(255,255,0)
green=(0,255,0)
yellow=(255,255,0)
blue=(0,0,255)
purple=(255,0,255)
light_blue=(0,255,255)
dh=500
dw=500
powerup=5000
hi_score_file=open("highscore.txt",'r')
hi_score=int(hi_score_file.read())
hi_score_file.close()
screen=pygame.display.set_mode([dw,dh])
pygame.display.set_caption("Space war")
clock=pygame.time.Clock()
def msg(txt,color,size,x,y):
    font=pygame.font.SysFont("comicsansms",size,bold=1)
    mtxt=font.render(txt,True,color)
    mrect=mtxt.get_rect()
    mrect.center=x,y
    screen.blit(mtxt,mrect)
def start():
    wait=1
    while wait:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    wait=0
        screen.fill(light_blue)
        msg("Space Shooter",purple ,50,250,150)
        msg("Press Enter to Continue",blue,20,250,350)
        msg("hi_score:"+str(hi_score),blue,20,250,30)
        pygame.display.flip()
def gover():
    wait=1
    while wait:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    wait=0
        screen.fill(light_blue)
        msg("Game Over",red ,50,250,250)
        msg("Press Enter to Continue",blue,20,250,350)
        msg("hi_score"+str(hi_score),blue ,20,250,30)
        pygame.display.update()
def pause():
    wait=1
    while wait:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    wait=0
        msg("Paused",blue ,50,250,250)
        msg("Press Enter to Play",blue,20,250,350)
        pygame.display.update()
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("rocket.png")
        self.image=pygame.transform.scale(self.image,[40,70])
        self.rect=self.image.get_rect()
        self.rect.x=200
        self.rect.y=dh-80        
        self.vx=0
        self.last=pygame.time.get_ticks()
        self.ptime=pygame.time.get_ticks()
        self.shot_delay=250
        self.power=1
    def powerup(self):
        self.power+=1
        self.ptime=pygame.time.get_ticks()
    def shoot(self):
        now=pygame.time.get_ticks()
        
        if now-self.last>self.shot_delay:
            if self.power==1:
                self.last=now
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power>=2:  
                self.last=now
                bullet1=Bullet(self.rect.left,self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2=Bullet(self.rect.right,self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
    def update(self):
        if self.power>=2 and pygame.time.get_ticks()-self.ptime>powerup:
            self.power-=1
            self.ptime=pygame.time.get_ticks()
        self.vx=0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx=-5
        if keys[pygame.K_RIGHT]:
            self.vx=5
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.rect.x+=self.vx
        if self.rect.left<=0:
            self.rect.left=0
        if self.rect.right>=dw:
            self.rect.right=dw
class Pow(pygame.sprite.Sprite):
    def __init__(self,img):
        super().__init__()
        self.img=img
        self.image=pygame.image.load(self.img)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(dw-self.rect.width)
        self.rect.y=random.randrange(-50,-20)
        self.vy=5
    def  update(self):
        self.rect.y+=self.vy
        if self.rect.y>500:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.i1=pygame.image.load("meteor.png")
        self.image=self.i1
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(dw-self.rect.width)
        self.rect.y=random.randrange(-50,-20)
        self.vx=random.randint(-1,1)
        self.vy=random.randint(1,6)
        self.rot=0
        self.rot_speed=random.randrange(-8,8)
        self.last=pygame.time.get_ticks()
    def rotate(self):
        now=pygame.time.get_ticks()
        if now-self.last>50:
            self.last=now
            self.rot=(self.rot+self.rot_speed)%360
            new_image=pygame.transform.rotate(self.i1,self.rot)
            old_center=self.rect.center
            self.image=new_image
            self.rect=self.image.get_rect()
            self.rect.center=old_center
    def update(self):
        self.rotate()
        self.rect.x+=self.vx
        self.rect.y+=self.vy
        if self.rect.top>dh+10 or self.rect.right<0 or self.rect.left>dw+10:
            self.rect.x=random.randrange(dw-self.rect.width)
            self.rect.y=random.randrange(-50,-20)
            self.vx=random.randint(-1,1)
            self.vy=random.randint(1,6)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("bullet.png")

        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vy=-5
    def  update(self):
        self.rect.y+=self.vy
        if self.rect.y<=0:
            self.kill()
def newmeteor():
    meteor=Meteor()
    all_sprites.add(meteor)
    meteors.add(meteor)
def drawlives(surf,lives,x,y):
    for i in range(lives):
        img=pygame.image.load("lives.png")
        img=pygame.transform.scale(img,[15,30])
        imgrect=img.get_rect()
        imgrect.x=x+30*i
        imgrect.y=y
        screen.blit(img,imgrect)
      
over=False
intro=True
score=0
hit=0
while 1:
    clock.tick(60)
    if intro:
        start()
        intro=False
        score=0
        all_sprites=pygame.sprite.Group()
        meteors=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        powers=pygame.sprite.Group()
        rocket=Rocket()
        all_sprites.add(rocket)
        hit=0
        lives=3
        for i in  range(5):
           newmeteor()

    hi_score_file=open("highscore.txt",'r')
    hi_score=int(hi_score_file.read())
    hi_score_file.close()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                pause()
    if over:
        gover()
        over=False
        score=0
        hit=0
        all_sprites=pygame.sprite.Group()
        meteors=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        powers=pygame.sprite.Group()
        rocket=Rocket()
        all_sprites.add(rocket)
        lives=3
        for i in  range(5):
           newmeteor()

    all_sprites.update()
    hits=pygame.sprite.groupcollide(bullets,meteors,1,1)
    if hits:

        if random.random()>0.9:
            pow1=Pow(random.choice(["pow1.png","pow2.png"]))
            all_sprites.add(pow1)
            powers.add(pow1)
            ssound.play()
        newmeteor()
        score+=5
    hits1=pygame.sprite.spritecollide(rocket,meteors,1)
    if hits1:
        hit+=1
        lives-=1
        newmeteor()
    hits2=pygame.sprite.spritecollide(rocket,powers,1)
    if hits2 and pow1.img=="pow1.png":
        score+=10
        rocket.powerup()
    if hits2 and pow1.img=="pow2.png":
        score+=30
        rocket.powerup()
    
    screen.fill(light_blue)

    all_sprites.draw(screen)
    msg("Score:"+str(score),blue,20,250,20)
    if (hi_score)<score:
        hi_score_file=open("highscore.txt",'w+')
        hi_score_file.write(str(score))
        
    if hit>3:
        over=True
    drawlives(screen,lives,400,10)
    pygame.display.flip()
