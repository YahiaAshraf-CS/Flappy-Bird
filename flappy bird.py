#flappy bird part 1 :-creating a background
#استدعاء الباي جيم للبدي في عمل اللعبة
from typing import Any
import pygame
from pygame.locals import*
import random #عشان اخلي الاقماع مختلفة في المسافة عن بعض



pygame.init()
#make the game run slower
clock=pygame.time.Clock()
fps=60#the frame of speed is 60 frame per second
#
#bulit the game window
screen_width=828#700
screen_height=815#800#900
screen= pygame.display.set_mode((screen_width,screen_height))

#name the game (flappy bird)
pygame.display.set_caption('flappy bird')
#define my font and the color of the score
font=pygame.font.SysFont('ADLaM Display',60)#شكل الخط يتاع الرقم
white=(255,255,255)



#define game variable
ground_scroll=0
scroll_speed=4#هخالي السرعة 4 
flying=False#هنا ده متغير هيتحول لصح عشان يخلي العصفور يطير اول لما ابدا اللعبة
game_over=False
pipe_gap=250#المسافة مابين العمود اللي فوق و اللي تحت
pipe_frequency=1500#time by millisecond
last_pipe=pygame.time.get_ticks()-pipe_frequency
score=0
pass_pipe=False

#download images for the game to be the background
background=pygame.image.load(r"bg.png") # download the background image
ground= pygame.image.load(r"ground.png") # download the ground image
restart_button=pygame.image.load(r"restart.png") # download the restart buttom #yehia
#here i will download the score like a text on the game





def draw_text(text,font,text_color,x,y):#render=تجسيد الرقم
    img=font.render(text,True,text_color)#i will make the score text like an image
    screen.blit(img,(x,y))
    
    
#this funtion when the game is over and restart the game the score return back to zero and the all game return to original (yehia)    
def reset_game():  
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(screen_height/2)
    score=0
    return score
    
    
    
    
class bird(pygame.sprite.Sprite):#this function is to make the image of the bird & make the animation of the bird & make the physics that make the bird down 
    def __init__(self, x, y):#الxوالyدول زوايا للمستطيل
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,4):
            img=pygame.image.load(fr"bird{num}.png")
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.velocity=0
        self.clicked=False
    def update(self):
        # making the gravity
        if flying==True:
            self.velocity+=0.5
            if self.velocity>8:
               self.velocity=8
        #print(self.velocity) هنا كنت عايز اشوف هل الكثافة هتقف عند 8 ولا لا
            if self.rect.bottom<705:
               self.rect.y +=int(self.velocity)
        
        
        
        
        if game_over==False:
         # making the bird jump
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False : #هنا انا عامل شرط يخلي يعرف اللعبة اني دوست علي الماوث  عشان ينط العصفور 
             self.clicked=True
             self.velocity=-10
            if pygame.mouse.get_pressed()[0]==0:
             self.clicked=False
        
            
        # handling the animation             handle=يظبط
            self.counter+=1
            flap_cooldown=5
            if self.counter>flap_cooldown:
              self.counter=0
              self.index+=1
            if self.index>=len(self.images):
              self.index=0
              self.image=self.images[self.index] 
        
         #rotate the bird بخلي يطلع بزاويا و ينزل بزاويا 
            self.image=pygame.transform.rotate(self.images[self.index],self.velocity*-2) 
        else:
           self.image=pygame.transform.rotate(self.images[self.index],-90)     
            
 #create thee pipe class:-           
class pipe(pygame.sprite.Sprite) :
    def __init__(self,x,y,position):#initialization __init__ =بتهيئة الوظيفة
      pygame.sprite.Sprite.__init__(self)  #take the sprite function from the sprite class
      self.image=pygame.image.load(r"pipe.png")#dowmload the image in the game
      self.rect=self.image.get_rect()#talk the image and create the rectangle around the image
      #position 1 is from the top, -1 from the bottom
      if position==1:
          self.image=pygame.transform.flip(self.image,False,True)#flip=يشقلب الصورة i filp the image to be up and down in this function x=false and y=true
          self.rect.bottomleft=[x,y-int(pipe_gap/2)]
      if position==-1:
          self.rect.topleft=[x,y+int(pipe_gap/2)]#define the position of the rectangle based on x and y coordinates and the gap between the two pipes
           
    
    #hanling the pipe to move to the left:-
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()#.kill (used to delete the past pipe that the bird had across it )
            
#yehia create the button
class Button():
    def __init__(self,x,y,image):
        self.image=image 
        self.rect=self.image.get_rect() #to create the rectangle of the image 
        self.rect.topleft= (x,y)#to make the image in the top left
        
        
        
        
    
    def draw(self):
        action= False
        #get mouse position
        position=pygame.mouse.get_pos()#عشان اقدر ادوس علي الزوارmake it a list
        
        #check if mouse is over the button =عشان اقدر اضغط علي الزر
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0]==1: #make it a small list
                action=True
                
               
        #draw the restart button
        screen.blit(self.image,(self.rect.x,self.rect.y))         
        return action    
            
    
    
    
    
        
bird_group=pygame.sprite.Group()#create the bird group for the function

pipe_group=pygame.sprite.Group()#create the pipe group     
   
flappy=bird (100 , int(screen_height/2))#x and y 
bird_group.add(flappy)
#yehia
#create my restart button insrance=مثيل للزر    
button=Button(screen_width/2-50,screen_height/2-100,restart_button)#make the place to the button


#create the game loop:-
#هنا انا عايز اخلي اللعبة شغاله لحد لما ادوس علي غلق ف اللعبة تقفل
run=True
while run:
    clock.tick(fps)
    #هنا انا هحط الصورة علي الشاشة بتاعه اللعبة 
    
#draw the background :-
    screen.blit(background,(0,0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    
    
    #draw the ground
    screen.blit(ground,(ground_scroll,705))
    
    #check the score
    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right\
            and pass_pipe==False:
                pass_pipe=True
        if pass_pipe==True:
             if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
                  score+=1
                  pass_pipe=False
              
    draw_text(str(score),font,white,int(screen_width/2),20)
    
    
    
    #look for the collision=عندما يحدث اصطدام
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False)or flappy.rect.top<0:
        game_over=True
    #check if the bird hit the ground 
    if flappy.rect.bottom>=705:
        game_over=True
        flying=False
        
        
#draw the ground and scroll the ground:-
    
    
#?هنا هخلي الرسمة تتحرك 
    if game_over==False and flying==True:
        #generate new pipe
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipe_frequency:
            pipe_height=random.randint(-100,100)#to make the pipes randomly not the same lenght
            bottom_pipe=pipe(screen_width,int(screen_height/2)+pipe_height,-1)#define the x and y coordinate=مثيل له
            top_pipe=pipe(screen_width,int(screen_height/2)+pipe_height,1)
            pipe_group.add(bottom_pipe)# i added the bottom pipe to the pipe group
            pipe_group.add(top_pipe)  
            last_pipe=time_now       
        
    #draw and scroll the ground
        ground_scroll-=scroll_speed
        if abs(ground_scroll)>35:#35 pixels
            ground_scroll=0
    
        pipe_group.update()#i make it here because when the game is over the pipes stops
     
     
     
     
#!check for the game over and restart

    if game_over==True:
        if button.draw()==True:   #yehia =لو اللعبة انتهت ارسم الزر الاعادة
            game_over=False
            score=reset_game()
        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True
            
    pygame.display.update()
pygame.quit()
