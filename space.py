import pygame,random,time
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
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode([dw,dh])
pygame.display.set_caption("Space war")
clock=pygame.time.Clock()
def msg(txt,color,size,x,y):
    font=pygame.font.SysFont("comicsansms",size,bold=1)
    mtxt=font.render(txt,True,color)
    mrect=mtxt.get_rect()
    mrect.center=x,y
    screen.blit(mtxt,mrect)
    
    
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
        screen.fill(white)            
        msg("Game Over",red ,50,250,250)
        msg("Press Enter to Continue",blue,20,250,350)
        pygame.display.flip()            
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
        screen.fill(white)            
        msg("Paused",blue ,50,250,250)
        msg("Press Enter to Continue",blue,20,250,350)
        pygame.display.update()
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface([50,50])
        self.image.fill(green)
        self.rect=self.image.get_rect()
        self.rect.x=200
        self.rect.y=dh-60
        self.vx=0
        self.last=pygame.time.get_ticks()
        self.ptime=pygame.time.get_ticks()
        self.shot_delay=250
    def shoot(self):
        now=pygame.time.get_ticks()
        if now-self.last>self.shot_delay:
            self.last=now
            bullet=Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
        elif now-self.ptime>powerup:
            self.ptime=now
            bullet1=Bullet(self.rect.left,self.rect.top)
            all_sprites.add(bullet1)
            bullet2=Bullet(self.rect.right,self.rect.top)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2) 
    def update(self):
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
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface([30,30])
        self.image.fill(red)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(dw-self.rect.width)
        self.rect.y=random.randrange(-50,-20)
        self.vx=random.randint(-3,3)
        self.vy=random.randint(1,3)
    def update(self):
        self.rect.y+=self.vy
        self.rect.y+=self.vy
        if self.rect.top>dh+10 or self.rect.right<0 or self.rect.left>dw+10:
            self.rect.x=random.randrange(dw-self.rect.width)
            self.rect.y=random.randrange(-50,-20)
            self.vx=random.randint(-3,3)
            self.vy=random.randint(1,3)
               
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface([10,30])
        self.image.fill(blue)
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
all_sprites=pygame.sprite.Group()
meteors=pygame.sprite.Group()
bullets=pygame.sprite.Group()
rocket=Rocket()
all_sprites.add(rocket)
for i in  range(5):
    newmeteor()
over=False
score=0
while 1:
    clock.tick(60)
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
        all_sprites=pygame.sprite.Group()
        meteors=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        rocket=Rocket()
        all_sprites.add(rocket)
        for i in  range(5):
           newmeteor()        
    all_sprites.update()
    hits=pygame.sprite.groupcollide(bullets,meteors,1,1)
    if hits:
        newmeteor()
        score+=5
    hits1=pygame.sprite.spritecollide(rocket,meteors,1)
    if hits1:
          over=True
    screen.fill(white)
    all_sprites.draw(screen)
    msg("Score"+str(score),blue,20,250,20)
    pygame.display.flip()
