import pygame, random, os
pygame.init()

pygame.display.set_caption('Crossy Road: KruASe edition')
WIDTH, HEIGHT=1500, 800
screen=pygame.display.set_mode((WIDTH, HEIGHT))

clock=pygame.time.Clock()
done=False

main_type, main, LINE_WIDTH, death, win=[random.choice([-1, 1])], [], 40, 0, 0
car_list1, car_list2=[pygame.image.load(os.path.join('car1.png')), pygame.image.load(os.path.join('car2.png')), pygame.image.load(os.path.join('car3.png')), pygame.image.load(os.path.join('car4.png')), pygame.image.load(os.path.join('car5.png')), pygame.image.load(os.path.join('car6.png'))], [pygame.image.load(os.path.join('1car.png')), pygame.image.load(os.path.join('2car.png')), pygame.image.load(os.path.join('3car.png')), pygame.image.load(os.path.join('4car.png')), pygame.image.load(os.path.join('5car.png')), pygame.image.load(os.path.join('6car.png'))]
BIG_FONT, SMALL_FONT=pygame.font.Font('jbm-r.ttf', 30), pygame.font.Font('jbm-r.ttf', 10)

def generate_level():
    while len(main_type)<16:
        if len(main_type)>3 and main_type[-1]!=0 and main_type[-2]!=0 and main_type[-3]!=0:
            main_type.append(0)
            continue
        if len(main_type)>1 and main_type[-1]==0 and main_type[-2]==0:
            main_type.append(random.choice([-1, 1]))
            continue
        a=random.choice([True, False])
        if a:
            main_type.append(0)
        else:
            main_type.append(random.choice([-1, 1]))
    for i in range(len(main_type)):
        a=main_type[i]
        main.append(Line(i))

class Car():
    def __init__(self, speed, duration, y, start, image):
        self.speed=speed
        self.duration=duration
        self.image=image
        self.start_y=y
        self.x=start
    
    def upd(self):
        self.y=self.start_y
        self.x+=self.speed*self.duration
        self.collider=pygame.Rect(self.x, self.y, 70, 35)
    
    def death(self):
        global death
        if (PLAYER.collider).colliderect(self.collider):
            death=1
    
    def remove(self):
        if (self.duration==-1 and self.x<-100) or (self.duration==1 and self.x>WIDTH+20):
            for i in main:
                try:
                    (i.cars).remove(self)
                except:
                    continue
    
    def draw(self):
        self.upd()
        self.death()
        self.remove()
        screen.blit(self.image, (self.x, self.y+2))

class Line():
    def __init__(self, index):
        global car_list1, car_list2
        self.index=index
        self.type=main_type[index]
        self.cars=[]
        if self.type==0:
            self.color=(116, 196, 63)
        else:
            self.color=(80, 80, 80)
            self.speed=random.choice([1, 3])
            if self.type==1:
                self.car_list=car_list1
                self.start_x=-80
            elif self.type==-1:
                self.car_list=car_list2
                self.start_x=WIDTH
        self.spawn_flag=True
    
    def upd(self):
        self.y=(self.index+3)*LINE_WIDTH

    def spawn(self):
        if self.spawn_flag:
            self.cars.append(Car(self.speed, self.type, self.y, self.start_x, random.choice(self.car_list)))
            self.pixel=random.randint(200*self.speed, 350*self.speed)
            self.spawn_flag=False
        if self.type==1 and self.cars!=[] and (not self.spawn_flag):
            if (self.cars[-1]).x>self.pixel:
                self.spawn_flag=True
        elif self.type==-1 and self.cars!=[] and (not self.spawn_flag):
            if ((self.cars[-1]).x-70)<(WIDTH-self.pixel):
                self.spawn_flag=True
    
    def draw(self):
        self.upd()
        pygame.draw.rect(screen, self.color, pygame.Rect(0, self.y, WIDTH, LINE_WIDTH))
        if self.type!=0:
            self.spawn()
            for i in self.cars:
                i.draw()
        

class Player():
    def __init__(self):
        self.x=(WIDTH-LINE_WIDTH)/2
        self.y=0
        self.collider=pygame.Rect(self.x, self.y, LINE_WIDTH, LINE_WIDTH)
        self.image=pygame.image.load(os.path.join('trollface.png'))
        self.flags=[True]*4
    
    def upd(self):
        self.collider=pygame.Rect(self.x, self.y, LINE_WIDTH, LINE_WIDTH)
    
    def win(self):
        global win
        if PLAYER.y==760:
            win=1

    def draw(self):
        self.upd()
        self.win()
        screen.blit(self.image, (self.x-4, self.y))
    
generate_level()

PLAYER=Player()

while not done:
    clock.tick(70)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    
    if event.type==pygame.KEYDOWN and death==0 and win==0:
        if PLAYER.flags[0] and (event.key==pygame.K_UP or event.key==pygame.K_w) and PLAYER.y>0:
            PLAYER.y-=LINE_WIDTH
            PLAYER.flags[0]=False
        if PLAYER.flags[1] and (event.key==pygame.K_DOWN or event.key==pygame.K_s) and PLAYER.y<HEIGHT-LINE_WIDTH:
            PLAYER.y+=LINE_WIDTH
            PLAYER.flags[1]=False
        if PLAYER.flags[2] and (event.key==pygame.K_RIGHT or event.key==pygame.K_d) and PLAYER.x<WIDTH-LINE_WIDTH*2:
            PLAYER.x+=LINE_WIDTH
            PLAYER.flags[2]=False
        if PLAYER.flags[3] and (event.key==pygame.K_LEFT or event.key==pygame.K_a) and PLAYER.x>LINE_WIDTH:
            PLAYER.x-=LINE_WIDTH
            PLAYER.flags[3]=False
    if event.type==pygame.KEYUP:
        if event.key==pygame.K_UP or event.key==pygame.K_w:
            PLAYER.flags[0]=True
        if event.key==pygame.K_DOWN or event.key==pygame.K_s:
            PLAYER.flags[1]=True
        if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
            PLAYER.flags[2]=True
        if event.key==pygame.K_LEFT or event.key==pygame.K_a:
            PLAYER.flags[3]=True

    for i in range(38):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(i*LINE_WIDTH, 760, LINE_WIDTH/2, LINE_WIDTH/2))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(i*LINE_WIDTH+LINE_WIDTH/2, 780, LINE_WIDTH/2, LINE_WIDTH/2))
    
    pygame.draw.rect(screen, (116, 196, 63), pygame.Rect(0, 0, WIDTH, LINE_WIDTH*3))
    
    for i in main:
        i.draw()
    
    PLAYER.draw()
    
    for i in main:
         for j in i.cars:
            j.draw()
    
    if win==1:
        screen.blit(pygame.image.load(os.path.join('win.png')), (490, 350))
        screen.blit(pygame.image.load(os.path.join('win.png')), (490, 320))
        screen.blit(pygame.image.load(os.path.join('for_restart.png')), (538, 421))
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                win=0
                PLAYER.x=(WIDTH-LINE_WIDTH)/2
                PLAYER.y=0
                main, main_type=[], [random.choice([-1, 1])]
                generate_level()

    if death==1:
        screen.blit(pygame.image.load(os.path.join('lose.png')), (490, 350))
        screen.blit(pygame.image.load(os.path.join('lose.png')), (490, 330))
        screen.blit(pygame.image.load(os.path.join('for_restart.png')), (555, 430))
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                death=0
                PLAYER.x=(WIDTH-LINE_WIDTH)/2
                PLAYER.y=0
    
    pygame.display.flip()
pygame.quit()
