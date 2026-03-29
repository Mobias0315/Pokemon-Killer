import pygame as pg
import os 
import random as rd
import time

pg.init()
screen_w,screen_h=1024,640
screen = pg.display.set_mode((screen_w, screen_h))   
pg.display.set_caption("game")
pg.display.set_caption('寶可夢大屠殺')
pg.display.set_icon(pg.image.load(os.path.join('./img/title','icon.png')))
bg = pg.Surface(screen.get_size()).convert_alpha()
bg.fill((255,255,255))

screen.blit(bg, (0,0))
clock = pg.time.Clock()
pg.display.update()


class human(pg.sprite.Sprite):
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)
        self.img =  [pg.image.load(os.path.join('./img/human','human%d.png'%i)).convert_alpha() for i in range(16)]
        self.mo = 'stop'                                    #初始狀態
        self.befor = self.img[0]                            #動畫起始
        self.image = self.img[0]                            #讀取座標用的起始
        self.speed = 0.07                                   #動畫速度 
        self.weapon = 'fist'                                #裝備                                  
        self.rect = self.image.get_rect()
        self.mo_speed =  0.2                                #移動速度 0.2
        self.radius = self.rect.width / 2                   #碰撞判斷用的半徑
        self.blood = 500                                    #血量
        self.blood_slot = 500                               #血量槽
        self.defense = 50                                   #防禦力
        self.defense_slot = 50                              #防禦力槽
        self.level = 1                                      #等級
        self.experience_slot = 5                            #經驗槽
        self.experience = 0                                 #經驗值
        self.rect.x = screen_w/2-self.rect.width/2          #初始位置
        self.rect.y = screen_h/2-self.rect.height/2             
        self.invincible_time = 0.3                          #受到傷害後的無敵時長 (每隻怪分開計算)
        self.time = time.time()                             
        self.buff_damage = 6                               #自身傷害
        self.attack_counter = 1                             
        self.att_frequency = 1                              #攻擊頻率 
        self.att_frequency_up = 1                              #攻擊頻率上升率 
        self.att_distance = 40                              #子彈起始距離增加
        self.att_befor = self.rect.centerx, self.rect.centery+self.att_distance ,90
        self.a = 0                                          #計算攻擊次數用
        self.s_x,self.s_y = 0,0                             #起始移動設定

    def update(self):
        if self.blood>0:
            if self.blood > self.blood_slot :
                self.blood = self.blood_slot  
            self.anime()
            self.attack()
            self.ex()
            self.zero = 0
            self.dead_time=time.time()
        else:
            self.mo_speed = 0
            self.img = [pg.image.load(os.path.join('./img/human/dead','dead%s.png'%i)) for i in range(4)]
            self.image= self.img[int((time.time()-self.dead_time)*3)%4]
            if int((time.time()-self.dead_time)*3)%4 == 3 and self.zero == 0:

                self.zero+=1
                self.dead()
        screen.blit(pg.font.Font('prstart.ttf',16).render( str(self.level) , True, (255,255,255), ),(screen_w/2 - len(str(self.level))*10,10)) #畫等級
        pg.draw.rect(screen, (79, 31, 30), [self.rect.left, self.rect.bottom, self.img[0].get_size()[0], 5])           #畫血條
        pg.draw.rect(screen, (240, 31, 30), [self.rect.left, self.rect.bottom, self.img[0].get_size()[0] * (self.blood / self.blood_slot) , 5])
        pg.draw.rect(screen, (79, 31, 30), [self.rect.left, self.rect.bottom+6, self.img[0].get_size()[0], 5])           #畫防禦條
        pg.draw.rect(screen, (202, 211, 209), [self.rect.left, self.rect.bottom+6, self.img[0].get_size()[0] * (self.defense / self.defense_slot) , 5])
        pg.draw.rect(screen, (79, 31, 30), [0, 0, screen_w, 5])         #畫經驗條
        pg.draw.rect(screen, (240, 31, 30), [0, 0, screen_w * (self.experience / self.experience_slot) , 5])

    def anime(self):
        if self.mo == 'stop':
            self.image = self.befor
            self.s_x = 0 
            self.s_y = 0 
        elif self.mo == 'left' or self.mo == 'up_left' or self.mo=='down_left':
            self.befor = self.img[4]
            self.s_x -= mo_x * self.speed
            self.image = self.img[int(self.s_x%4+4)]
            
        elif self.mo == 'right' or self.mo == 'up_right' or self.mo=='down_right':
            self.befor = self.img[8]
            self.s_x += mo_x * self.speed
            self.image = self.img[int(self.s_x%4+8)]

        elif self.mo == 'down':
            self.befor = self.img[0]
            self.s_y += mo_y * self.speed
            self.image = self.img[int(self.s_y%4)]

        elif self.mo == 'up':
            self.befor = self.img[12]
            self.s_y -= mo_y * self.speed
            self.image = self.img[int(self.s_y%4+12)]
    def attack(self) :
        if self.mo == 'stop':
            x,y ,self.angle = self.att_befor
        elif self.mo == 'left':
            x = self.rect.centerx-self.att_distance
            y = self.rect.centery
            self.angle = 0
            self.att_befor = x,y,self.angle
        elif self.mo == 'up_left':
            x = self.rect.centerx - ((self.att_distance**2)/2)**0.5
            y = self.rect.centery - ((self.att_distance**2)/2)**0.5
            self.angle = -45
            self.att_befor = x,y,self.angle
        elif self.mo == 'down_left':
            x = self.rect.centerx - ((self.att_distance**2)/2)**0.5
            y = self.rect.centery + ((self.att_distance**2)/2)**0.5
            self.angle = 45
            self.att_befor = x,y,self.angle
        elif self.mo == 'right':
            x = self.rect.centerx + self.att_distance
            y = self.rect.centery 
            self.angle = 180
            self.att_befor = x,y,self.angle
        elif self.mo == 'up_right':
            x = self.rect.centerx + ((self.att_distance**2)/2)**0.5
            y = self.rect.centery - ((self.att_distance**2)/2)**0.5
            self.angle = -135
            self.att_befor = x,y,self.angle
        elif self.mo == 'down_right':
            x = self.rect.centerx + ((self.att_distance**2)/2)**0.5
            y = self.rect.centery + ((self.att_distance**2)/2)**0.5
            self.angle = 135
            self.att_befor = x,y,self.angle
        elif self.mo == 'up':
            self.angle = 180
            x = self.rect.centerx 
            y = self.rect.centery - self.att_distance
            self.angle = -90
            self.att_befor = x,y,self.angle
        elif self.mo == 'down':

            x = self.rect.centerx 
            y = self.rect.centery + self.att_distance
            self.angle = 90
            self.att_befor = x,y,self.angle

        if self.weapon == 'fist' and int(time_gap * self.att_frequency)== self.a:
            self.att_frequency = 1 * self.att_frequency_up
            self.att_distance = 40
            bullet = fist(x,y,self.angle)
            bullet_group.add(bullet)
            all_spr.add(bullet)

        elif self.weapon == 'magic_wand' and int(time_gap * self.att_frequency)== self.a:
            self.att_frequency = 1 * self.att_frequency_up
            self.att_distance = 40
            bullet = magic_wand(x,y,self.angle)
            bullet_group.add(bullet)
            all_spr.add(bullet)

        elif self.weapon == 'e_gun' and int(time_gap * self.att_frequency)== self.a:
            self.att_frequency = (0.5 * self.att_frequency_up)
            self.att_distance = 40
            bullet = e_gun(x,y,self.angle)
            bullet_group.add(bullet)
            all_spr.add(bullet)

        elif self.weapon == 'gun'  and int(time_gap * self.att_frequency)== self.a:
            self.att_frequency = 1.3 * self.att_frequency_up
            self.att_distance = 40
            bullet = gun(x,y,self.angle)
            bullet_group.add(bullet)
            all_spr.add(bullet)
        elif self.weapon == 'rapier'  and int(time_gap * self.att_frequency)== self.a:
            self.att_frequency = 1 * self.att_frequency_up
            self.att_distance = 100
            bullet = rapier(x,y,self.angle)
            bullet_group.add(bullet)
            all_spr.add(bullet)

        self.a = int(time_gap * self.att_frequency) +1        
    def ex(self):
        global time_start,close
        
        if self.experience >=  self.experience_slot :
            button_group.empty()
            for i in range(3):
                button = choose_button(i)
                button_group.add(button)

            ex_pause = True
            stop_time = time.time()
            choose = 0
            while ex_pause:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                        choose += 1  
                    elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                        choose -= 1
                    if choose < 0: choose = 0
                    elif choose > 2 : choose = 2
                    for i in button_group.sprites():
                        if choose == i.i :
                            i.image = i.img[1]
                        else:i.image = i.img[0]
                        if (pg.key.get_pressed()[pg.K_SPACE] or pg.key.get_pressed()[pg.K_RETURN] )and choose == i.i :
                            i.choose()
                            ex_pause = False
                    if event.type == pg.QUIT:
                        close = True
                if close:break
                button_group.update()
                button_group.draw(screen)
                pg.display.update()
            time_start +=(time.time() - stop_time)
            self.experience -= self.experience_slot
            self.level += 1
            self.experience_slot = 5 * (1.3**self.level)
    def dead(self):
        global close,step
        button_group.empty()
        for i in range(1,3):
            button = stop_choose_button(i)
            button_group.add(button)
        dead_pause = True
        choose = 1
        while dead_pause:
            
            for event in pg.event.get():
                
                if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    choose += 1  
                elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    choose -= 1
                if choose < 1: choose = 1
                elif choose > 2 : choose = 2
                for i in button_group:
                    if choose == i.i:
                        i.image =i.img[1]
                        if (pg.key.get_pressed()[pg.K_SPACE] or pg.key.get_pressed()[pg.K_RETURN] ):
                            if i.choose() == 1:
                                step = 2
                            elif i.choose() == 2 :
                                step = 0
                            dead_pause = False
                    else:i.image = i.img[0]

                if event.type == pg.QUIT:
                    close = True
            if close:break
            map_group.draw(screen)
            play_group.draw(screen)
            button_group.update()
            button_group.draw(screen)

            pg.display.update()             
class bullets(pg.sprite.Sprite):
    def __init__(self, x ,y,angle):
        pg.sprite.Sprite.__init__(self)
        self.angle = angle              #角度
        self.time = time.time()         #出現時間
        self.x = x                      #定位
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.stay_time = int            #滯留時間
        self.move_x =  0                #移動方式
        self.move_y =  0
        self.speed = int                #子彈速度
    def update(self):
        self.x += self.move_x 
        self.y += self.move_y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.anime()
        self.dead()
    def directions(self) :
        if self.rect.centerx - play.rect.centerx < 0:
            direction_x = -1
        elif self.rect.centerx - play.rect.centerx > 0:
            direction_x = 1
        else : direction_x = 0
        if self.rect.centery - play.rect.centery < 0:
            direction_y = -1
        elif self.rect.centery - play.rect.centery > 0:
            direction_y = 1
        else : direction_y = 0
        return direction_x,direction_y
    def dead(self):
        if time.time() - self.time >= self.stay_time:
            self.kill()
    def anime(self):
        pass
class fist(bullets):
    def __init__(self, x, y, angle):
        self.img = pg.image.load(os.path.join('./img/attack/fist','fist.png')).convert_alpha()                                  
        self.image = pg.transform.rotate(self.img,angle)     #翻轉
        self.rect = self.image.get_rect()
        bullets.__init__(self,x, y, angle)
        self.damage = 0
        self.speed = 0.5
        self.stay_time = 0.1
        self.move_x = self.directions()[0]*self.speed  
        self.move_y = self.directions()[1]*self.speed
class magic_wand(bullets):
    def __init__(self, x, y, angle):
        self.img =[ pg.image.load(os.path.join('./img/attack/magic_wand','magic_wand%d.png'%i)).convert_alpha() for i in range(5) ] 

        self.image = pg.transform.rotate(self.img[0],angle)     #翻轉
        self.rect = self.image.get_rect()
        bullets.__init__(self,x, y, angle)
        self.damage = 25
        self.speed =0
    def anime(self):
        self.anime_speed = ((time.time() -self.time)*10)*3
        self.image = pg.transform.rotate(self.img[ int(self.anime_speed) % 5 ],self.angle) 

    def dead(self):
        if int(self.anime_speed) % 5  == 4 :
            self.kill()
class e_gun(bullets):
    def __init__(self, x, y, angle):
        self.img =[ pg.image.load(os.path.join('./img/attack/e_gun','e_gun%d.png'%i)).convert_alpha() for i in range(2)]                                  
        self.image = pg.transform.rotate(self.img[0],angle)     #翻轉
        self.rect = self.image.get_rect()
        bullets.__init__(self,x, y, angle)
        self.damage = 40
        self.speed = 2
        self.move_x = self.directions()[0]*self.speed  
        self.move_y = self.directions()[1]*self.speed    
    def anime(self):
        self.anime_speed = ((time.time() -self.time)*5)
        self.image = pg.transform.rotate(self.img[ int(self.anime_speed) % 2 ],self.angle) 
    def update(self):
        self.x += self.move_x +mo_x
        self.y += self.move_y +mo_y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.anime()
        self.dead()
    def dead(self):
        if not(0 - self.image.get_size()[0] <self.rect.x < screen_w) or not(0-self.image.get_size()[1] <self.rect.y < screen_h) :
            self.kill()
class gun(bullets):
    def __init__(self, x, y, angle):
        self.img =[ pg.image.load(os.path.join('./img/attack/gun','gun%d.png'%i)).convert_alpha() for i in range(3)]                                  
        self.image = pg.transform.rotate(self.img[0],angle)     #翻轉
        self.rect = self.image.get_rect()
        bullets.__init__(self,x, y, angle)
        self.damage = 10
        self.speed = 3
        self.move_x = self.directions()[0]*self.speed  
        self.move_y = self.directions()[1]*self.speed    
    def anime(self):
        self.anime_speed = ((time.time() -self.time)*10)

        if int(self.anime_speed) % 3 == 2:
             self.img =[ pg.image.load(os.path.join('./img/attack/gun','gun2.png')) for i in range(3)]  
        self.image = pg.transform.rotate(self.img[ int(self.anime_speed) % 3 ],self.angle) 
        
            
    def update(self):
        self.x += self.move_x +mo_x
        self.y += self.move_y +mo_y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.anime()
        self.dead()
    def dead(self):
        if not(0 - self.image.get_size()[0] <self.rect.x < screen_w) or not(0-self.image.get_size()[1] <self.rect.y < screen_h) :
            self.kill()
class rapier(bullets):
    def __init__(self, x, y, angle):
        self.img =[ pg.image.load(os.path.join('./img/attack/Rapier','rapier%d.png'%i)).convert_alpha() for i in range(3) ] 

        self.image = pg.transform.rotate(self.img[0],angle)     #翻轉
        self.rect = self.image.get_rect()
        bullets.__init__(self,x, y, angle)
        self.damage = 70
        self.speed =0
    def anime(self):
        self.anime_speed = ((time.time() -self.time)*10)*1.5
        self.image = pg.transform.rotate(self.img[ int(self.anime_speed) % 3 ],self.angle) 

    def dead(self):
        if int(self.anime_speed) % 3  == 2 :
            self.kill() 

class choose_button(pg.sprite.Sprite):
    def __init__(self,i) :
        pg.sprite.Sprite.__init__(self)
        
        self.list_weapon = ['magic_wand','gun','e_gun','rapier']
        self.list_weapon_title = ['魔杖',
                                  '槍',
                                  '能量槍',
                                  '細劍']
        self.list_weapon_word = ['物理傷害',
                                 '這玩意比魔杖還好用阿！！',
                                 '子彈更大！傷害更高！速度更慢！',
                                 '看起來變高尚了' ]
        self.list_buff = ['heart','attack_up','speed_up','restore_health','armor','swing']
        self.list_buff_word = ['提升血量上限',
                               '提升傷害上限',
                               '提升走路速度',
                               '立即回復血量上限的20%血量',
                               '回復防禦力',
                               '小幅度增加攻擊速度']
        self.img = [pg.image.load(os.path.join('./img/choose','choose%d.png'%i)).convert_alpha() for i in range(2)]
        self.image = self.img[0]
        
        self.rect = self.image.get_rect() 
        self.x = screen_w/2
        self.y = screen_h/2 -150 + i*150
        self.w=self.image.get_width()
        self.h=self.image.get_height()
        self.i = i
        self.options()
        
    def update(self):
        
        self.rect = self.image.get_rect() 
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.w=self.image.get_width()
        self.h=self.image.get_height()
        self.image.blit( self.option_img ,(72 - self.option_img.get_size()[0]/2,58-self.option_img.get_size()[1]/2))
        self.image.blit(pg.font.Font('Cubic_11_1.010_R.ttf',28).render( self.title , True, (247, 100, 39) ),(self.image.get_size()[0]/2,self.image.get_size()[1]/6))
        self.image.blit(pg.font.Font('Cubic_11_1.010_R.ttf',28).render( self.word , True, (160,160,160) ),(self.image.get_size()[0]/4,self.image.get_size()[1]/2))

    def colli(self,x,y):
        #碰撞檢測
        if self.x-self.w/2 < x < self.x + self.w/2 and self.y-self.h/2 < y < self.y + self.h/2:
            return True
        else:
            return False
    def choose(self):
        if self.option in self.list_weapon:
            play.weapon = self.option
        elif self.option == 'heart' :
            play.blood_slot *= 1.05
            print('heart',play.blood_slot)
        elif self.option == 'attack_up':
            play.buff_damage *= 1.2
            print('attack_up',play.buff_damage)
        elif self.option == 'speed_up':
            play.mo_speed *= 1.2
            print('speed_up',play.mo_speed)
        elif self.option == 'restore_health':
            play.blood += play.blood_slot * 0.2
            print('restore_health',play.blood)
        elif self.option == 'armor' :
            play.defense = play.defense_slot
        elif self.option == 'swing':
            play.att_frequency_up *=1.1
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def options(self):
        if ((play.level == 4 ) or (play.weapon == 'fist' and play.level == 12 ) )and  self.i != 2:
            if self.i == 0:
                self.option = self.list_weapon[ 0 ]
            elif self.i == 1:
                self.option = self.list_weapon[ 1 ]
        elif self.i == 0 and play.level == 15 and play.weapon != 'fist':
            if play.weapon == 'gun':
                self.option = 'e_gun'
            elif play.weapon == 'magic_wand':
                self.option = 'rapier'
        else : self.option = self.list_buff[ rd.randint(0,len(self.list_buff)-1) ]
        self.option_img = pg.image.load(os.path.join('./img/choose','%s.png'%self.option)).convert_alpha()

        if self.option in self.list_weapon:
            self.title = self.list_weapon_title[ self.list_weapon.index(self.option) ]
            self.word = self.list_weapon_word[ self.list_weapon.index(self.option) ]
        else:
            self.title = ''
            self.word = self.list_buff_word[ self.list_buff.index(self.option) ]
class stop_choose_button(pg.sprite.Sprite):
    def __init__(self,i) :
        pg.sprite.Sprite.__init__(self)
        
        self.img = [pg.image.load(os.path.join('./img/choose','stop_choose%d.png'%j)).convert_alpha() for j in range(2)]
        self.image = self.img[0]
        self.rect = self.image.get_rect() 
        self.x = screen_w/2
        self.y = screen_h/2 -110+ i*80

        self.w=self.image.get_width()
        self.h=self.image.get_height()
        self.i = i
        self.options()
        
    def update(self):
        
        self.rect = self.image.get_rect() 
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.w=self.image.get_width()
        self.h=self.image.get_height()
        self.image.blit(pg.font.Font('Cubic_11_1.010_R.ttf',28).render( self.text , True, (247, 100, 39) ),(self.image.get_size()[0]/2-30,self.image.get_size()[1]/6))
   
    def colli(self,x,y):
        #碰撞檢測
        if self.x-self.w/2 < x < self.x + self.w/2 and self.y-self.h/2 < y < self.y + self.h/2:
            return True
        else:
            return False
    def choose(self):
        return self.i
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def options(self):
        if self.i == 0   : self.text = '繼續'
        elif self.i == 1 : self.text = '重新'
        elif self.i == 2 : self.text = '退出'

class damage_number(pg.sprite.Sprite):
    def __init__(self,x,y,damage,color = (255,255,255)):
        pg.sprite.Sprite.__init__(self) 
        self.damage_num = damage
        self.x = rd.randint(x-15,x+15)
        self.y = y
        self.move_x= rd.uniform(-0.8, 0.8)
        self.time = time.time()
        self.color = color
    def update(self):  
        self.x += self.move_x
        self.y += (-0.5)+((time.time() - self.time)**2 * 9.8)
        screen.blit(pg.font.Font('prstart.ttf',18).render( str(int(self.damage_num)), True, self.color ),(self.x,self.y))
        if time.time() - self.time > 0.4 :
            self.kill()
###############分隔線 以下是怪物##########################################################################
class monster(pg.sprite.Sprite):
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)
        #套用monster要先設定self.img 
        self.image = self.img[0]
        self.img_updata = self.img[:]
        self.rect = self.image.get_rect()
        self.radius = self.rect.width / 2 
        self.speed = 0.1
        self.time = time.time()     #動畫使用
        #pg.draw.circle(self.image , (25,255,25) , self.rect.center , self.radius)
        # if 0 - self.image.re
        self.x=coordinate_x
        self.y=coordinate_y
        if self.x < 0 - self.image.get_size()[0] :
            self.x = 0 - self.image.get_size()[0]
        elif screen_w  < self.x:
            self.x = screen_w
        if self.y < 0 - self.image.get_size()[1] :
            self.y = 0 - self.image.get_size()[1]
        elif screen_h  < self.y:
            self.y = screen_h
        self.de_time = time.time()  #計算攻擊頻率用 #會隨時更新
        self.hurt_time = time.time()
        self.damage = int
        self.blood = int
        self.defense = 0    #防禦力 
        self.invincible_time = 0.1
        self.ex_mon = 0
    def update(self):
        self.move()
        if pg.sprite.collide_mask(play, self) and time.time() - self.de_time >= play.invincible_time:
            self.de_time = time.time()
            play.blood-= self.damage - (self.damage * play.defense / 100 )
            play.defense -= 2
            num = damage_number(play.rect.centerx,play.rect.centery,self.damage - (self.damage * play.defense / 100 ),(223, 52, 0))
            num_group.add(num)
        self.anime()  
        self.dead()
          
    def move(self) :
        distance = ((self.rect.center[0] - play.rect.center[0])**2 + (self.rect.center[1] - play.rect.center[1])**2)**0.5
        if distance != 0 :
            move_distance = distance
        else :move_distance = 0.1
        self.move_x = (self.rect.center[0] - play.rect.center[0]) / move_distance #X移動方向
        self.move_y = (self.rect.center[1] - play.rect.center[1]) / move_distance #Y移動方向
        self.x -= (self.move_x * self.speed) - mo_x
        self.y -= (self.move_y * self.speed) - mo_y
        self.rect.x = self.x
        self.rect.y = self.y
        if self.rect.x <= -30 - self.image.get_size()[0] :
            self.x = screen_w+30
        elif self.rect.x >= screen_w+30:
            self.x = -30 - self.image.get_size()[0]
        if self.rect.y <= -30 - self.image.get_size()[1] :
            self.y = screen_h +30
        elif self.rect.y >= screen_h+30:
            self.y = -30 - self.image.get_size()[1]
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 3+15)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 3+12)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 3+21)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 3+18)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 3)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 3+3)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 3+6)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 3+9)]
    def hurt(self,damage):
        if time.time() - self.hurt_time >= self.invincible_time:
            self.hurt_time = time.time()
            if self.defense > 0:
                self.defense -= 2
            else: self.defense = 0
            self.blood -= (damage - (damage) * (self.defense / 100))
            num = damage_number(self.rect.centerx,self.rect.centery,(damage - (damage) * (self.defense / 100)))
            num_group.add(num)    

            # mask = pg.mask.from_surface(self.image).to_surface()
            # mask.set_colorkey((0,0,0))
            # self.image.blit(mask,(0,0))
        
    def dead(self):
        if self.blood <= 0:
            self.kill()
            play.experience+=self.ex_mon
class eevee(monster):
    def __init__(self):
        self.name = 'eevee'
        self.img = [pg.image.load(os.path.join('./img/eevee','eevee%d.png'%i)).convert_alpha() for i in range(24)]
        monster.__init__(self)
        self.damage = 2
        self.blood = 17
        self.ex_mon = 1
class cubone(monster):
    def __init__(self):
        self.name = 'cubone'
        self.img = [pg.image.load(os.path.join('./img/cubone','cubone%d.png'%i)).convert_alpha() for i in range(32)]
        monster.__init__(self)
        self.damage = 4
        self.blood = 50
        self.ex_mon = 4
        self.defense = 20
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+20)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+16)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+28)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+24)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+12)]
class snack(monster):
    def __init__(self):
        self.name = 'snack'
        self.img = [pg.image.load(os.path.join('./img/snack','snack%d.png'%i)).convert_alpha() for i in range(8)]
        monster.__init__(self)
        self.damage = 2
        self.blood = 20
        self.ex_mon = 1
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 2+6)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 2+4)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 2+6)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 2+4)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 2)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 2+2)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 2+4)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 2+6)]
class Farfetch(monster):
    def __init__(self):
        self.name = 'Farfetch'
        self.img = [pg.image.load(os.path.join("./img/Farfetch'd","Farfetch'd%d.png"%i)).convert_alpha() for i in range(16)]
        monster.__init__(self)
        self.damage = 12
        self.blood = 100
        self.ex_mon = 20
        self.speed = 0.22
        self.defense = 50
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+12)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+12)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+12)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+8)]
class emboar(monster):
    def __init__(self):
        self.name = 'emboar'
        self.img = [pg.image.load(os.path.join('./img/emboar','emboar%d.png'%i)).convert_alpha() for i in range(32)]
        monster.__init__(self)
        self.damage = 4
        self.blood = 15
        self.ex_mon = 3
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+20)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+16)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+28)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+24)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+12)]
class Alolan_Diglett(monster):
    def __init__(self):
        self.name = 'Alolan_Diglett'
        self.img = [pg.image.load(os.path.join('./img/Alolan_Diglett','Alolan_Diglett%d.png'%i)).convert_alpha() for i in range(16)]
        monster.__init__(self)
        self.damage = 2
        self.blood = 15
        self.ex_mon = 1
    
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 2+10)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 2+8)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 2+14)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 2+12)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 2)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 2+2)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 2+4)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 2+6)]
class Snivy(monster):
    def __init__(self):
        self.name = 'Snivy'
        self.img = [pg.image.load(os.path.join('./img/Snivy','Snivy%d.png'%i)).convert_alpha() for i in range(16)]
        monster.__init__(self)
        self.damage = 2
        self.blood = 15
        self.ex_mon = 1
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+12)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+8)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+12)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+8)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+12)]
class Rowlet(monster):
    def __init__(self):
        self.name = 'Rowlet'
        self.img = [pg.image.load(os.path.join('./img/Rowlet','Rowlet%d.png'%i)).convert_alpha() for i in range(16)]
        monster.__init__(self)
        self.damage = 4
        self.blood = 400
        self.ex_mon = 20
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+12)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+8)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+12)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+8)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+12)]
class special_Rowlet(Rowlet):
    def __init__(self,location,x ): #location  0上,1下
        Rowlet.__init__(self)
        self.name = 'special_Rowlet'
        self.damage = 8
        self.blood = 600
        self.ex_mon = 30
        self.speed = 0.5
        self.location = location
        if self.location == 0:
            self.x = 2 * x * self.image.get_size()[0]
            self.y = 0-self.image.get_size()[1]
        elif self.location == 1:
            self.x = ((2 * x - 1 )* self.image.get_size()[0]) 
            self.y = screen_h 
        self.rect.x = self.x
        self.rect.y = self.y 
    def move(self):
        self.move_x = 0

        if self.location == 0:
            self.move_y = -1
            self.x -=  -mo_x
            self.y -= (self.move_y * self.speed) - mo_y
            self.rect.x = self.x
            self.rect.y = self.y
        elif self.location == 1:
            self.move_y = 1
            self.x -= -mo_x
            self.y -= (self.move_y * self.speed)  - mo_y
            self.rect.x = self.x
            self.rect.y = self.y
    def dead(self):
        if self.blood <= 0 :
            self.kill()
            play.experience+=self.ex_mon
        elif self.y < -20 - self.image.get_size()[1] or self.y > screen_h + 20  :
            self.kill()
class Geodude(monster):
    def __init__(self):
        self.name = 'Geodude'
        self.img = [pg.image.load(os.path.join('./img/Geodude','Geodude%d.png'%i)).convert_alpha() for i in range(32)]
        monster.__init__(self)
        self.damage = 10
        self.blood = 1600
        self.ex_mon = 100
        self.defense = 80
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+20)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+16)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+28)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+24)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+12)]
class pikachu(monster):
    def __init__(self):
        self.name = 'pikachu'
        self.img = [pg.image.load(os.path.join('./img/pikachu','pikachu%d.png'%i)).convert_alpha() for i in range(32)]
        self.att_img = [pg.image.load(os.path.join('./img/pikachu/attack','pikachu%d.png'%i)).convert_alpha() for i in range(24)]
        monster.__init__(self)
        self.damage = 4
        self.blood = 15000
        self.ex_mon = 1
        self.speed = 0.3
        self.invincible_time = 0.05
        self.direction=0
        self.att_bool= False
    def update(self):
        self.move()
        if pg.sprite.collide_mask(play, self) and time.time() - self.de_time >= play.invincible_time:
            self.de_time = time.time()
            play.blood-= self.damage - (self.damage * play.defense / 100 )
            play.defense -= 2
            num = damage_number(play.rect.centerx,play.rect.centery,self.damage - (self.damage * play.defense / 100 ),(223, 52, 0))
            num_group.add(num)
        self.anime()  
        self.dead()
        if int(time.time() - self.time) % 8 == 7:
            self.att_time = time.time()
            self.att_bool = True
    def anime(self) :

        if self.att_bool:
            self.speed = 0
            anime_speed = (time.time() - self.time)*2
            if 2 < time.time() - self.att_time <4 :
                self.image = self.att_img[2 + (3 *self.direction)]
                has = 0
                for i in mon_group:
                    if i.name == 'lightning':
                        has +=1
                if has < 10:
                    mon = lightning()
                    all_spr.add(mon)
                    mon_group.add(mon)
            elif time.time() - self.att_time < 2:
                self.image = self.att_img[int(anime_speed) % 2 + (3 *self.direction)]
            else: 
                self.att_bool = False
                self.time = time.time()
                
        else:
            self.speed = 0.3
            anime_speed = self.speed*(time.time() - self.time)*30
            if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
                self.image = self.img[int(anime_speed % 4+20)]
                self.direction=5
            elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
                self.image = self.img[int(anime_speed % 4+16)]   
                self.direction=4
            elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
                self.image = self.img[int(anime_speed % 4+28)]
                self.direction=7
            elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
                self.image = self.img[int(anime_speed % 4+24)] 
                self.direction=6     
            elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
                self.image = self.img[int(anime_speed % 4)]
                self.direction=0
            elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
                self.image = self.img[int(anime_speed % 4+4)]
                self.direction=1
            elif self.move_x > 0:                                       #往左
                self.image = self.img[int(anime_speed % 4+8)]
                self.direction=2
            elif self.move_x < 0:                                       #往右
                self.image = self.img[int(anime_speed % 4+12)]
                self.direction=3
    def dead(self):
        global close,step,title_word 
        if self.blood <= 0:
            self.kill()
            play.experience+=self.ex_mon
            win_pasue = True
            b = pg.Surface((screen_w,screen_h)).convert_alpha()
            a=0
            ti = time.time()
            title_word = '%.4f'%time_gap

            while win_pasue:

                for event in pg.event.get():
                    
                    if event.type == pg.QUIT:
                        close = True
                if close : break
                alpha = (time.time() - ti)*50

                if alpha>=255:
                    step = 0
                    
                    break
                map_group.draw(screen)
                all_spr.draw(screen)
                pg.draw.rect(b,(255,255,255,alpha),(0,0,screen_w,screen_h))
                screen.blit(b,(0,0))
                pg.display.update()
class lightning(monster):
    def __init__(self):
        self.name = 'lightning'
        self.img = [pg.image.load(os.path.join('./img/pikachu/lightning','lightning%d.png'%i)).convert_alpha() for i in range(12)]
        monster.__init__(self)
        self.x = rd.randint(0 ,screen_w) -(self.image.get_size()[0]/2)
        self.y = rd.randint(0, screen_h ) - (self.image.get_size()[1]/2)
        self.damage = 15
        self.speed = 0
    def hurt(self,damage):
        pass
    def anime(self) :
        self.anime_speed = (time.time() -self.time)*8
        self.image = self.img[int(self.anime_speed % 12)]
    def dead(self):
        if int(self.anime_speed % 12) == 11:
            self.kill()
class emboar_up(monster):
    def __init__(self):
        self.name = 'emboar_up'
        self.img = [pg.image.load(os.path.join('./img/emboar_up','emboar_up%d.png'%i)).convert_alpha() for i in range(32)]
        monster.__init__(self)
        self.damage = 10
        self.blood = 300
        self.ex_mon = 25
    def anime(self) :
        anime_speed = self.speed*(time_gap - self.time)*45
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+20)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+16)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+28)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+24)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+12)]
class Golbat(monster):
    def __init__(self,x,y):
        self.name = 'Golbat'
        self.img = [pg.image.load(os.path.join('./img/Golbat','Golbat%d.png'%i)).convert_alpha() for i in range(32)]
        monster.__init__(self)
        self.x = x
        self.y = y
        self.damage = 2
        self.blood = 40
        self.ex_mon = 12
        self.speed = 1
        self.a = 0
    def anime(self) :  
        anime_speed = self.speed*(time_gap - self.time)*10
        if self.move_y < 0 and self.move_x < 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                     #往右 下
            self.image = self.img[int(anime_speed % 4+20)]
        elif self.move_y < 0 and self.move_x > 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往左 下
            self.image = self.img[int(anime_speed % 4+16)]   
        elif self.move_y > 0 and self.move_x < 0 and self.move_x/self.move_y < -1/3 and self.move_y/self.move_x < -1/3 :                #往右 上
            self.image = self.img[int(anime_speed % 4+28)]
        elif self.move_y > 0 and self.move_x > 0 and self.move_x/self.move_y > 1/3 and self.move_y/self.move_x > 1/3:                   #往左 上
            self.image = self.img[int(anime_speed % 4+24)]      
        elif self.move_y < 0 and -1 < self.move_x / self.move_y < 1:                                       #往下
            self.image = self.img[int(anime_speed % 4)]
        elif self.move_y > 0 and -1 < self.move_x / self.move_y < 1:                                       #往上
            self.image = self.img[int(anime_speed % 4+4)]
        elif self.move_x > 0:                                       #往左
            self.image = self.img[int(anime_speed % 4+8)]
        elif self.move_x < 0:                                       #往右
            self.image = self.img[int(anime_speed % 4+12)]
    def move(self) :
        if self.a < 3:
            self.distance = ((self.rect.center[0] - play.rect.center[0])**2 + (self.rect.center[1] - play.rect.center[1])**2)**0.5
            self.move_x = (self.rect.center[0] - play.rect.center[0]) / self.distance #X移動方向
            self.move_y = (self.rect.center[1] - play.rect.center[1]) / self.distance #Y移動方向
            self.a+=1
        self.x -= (self.move_x * self.speed) - mo_x
        self.y -= (self.move_y * self.speed) - mo_y
        self.rect.x = self.x
        self.rect.y = self.y
    
    def dead(self):
        if self.blood <= 0 :
            self.kill()
            play.experience+=self.ex_mon
        elif self.y < -100 - self.image.get_size()[1] or self.y > screen_h + 100 or self.x > screen_w + 100 or self.x < -100 - self.image.get_size()[0]:
            self.kill()
def random_coordinate():  #怪物的隨機定位
    global coordinate_x,coordinate_y
    x = rd.randint(0,screen_w + 600) -300
    y = rd.randint(0,screen_h + 600) -300
    if not (-100 < x < screen_w+100 and -100 < y < screen_h+100):
        coordinate_x , coordinate_y = x,y
###############分隔線 以上是怪物##########################################################################
title_word = '< PRESS START >'
class title(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.img = pg.image.load(os.path.join('./img/title','title.png'))
        size = self.img.get_size()
        self.image = pg.transform.smoothscale(self.img, (screen_w, screen_w/size[0] * size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.start = False
        
    def update(self):
        global step,title_word,close 
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE or event.type == pg.QUIT:
                close = True
            if event.type == pg.KEYDOWN:
                tit.click()

            
        if self.start:
            step +=1
        elif not(self.rect.y <= (-500 *(screen_w/self.img.get_size()[0]))):
            self.rect.y -= (1.5*(screen_w/self.img.get_size()[0]))
        elif int(time.time()) % 2 == 0:
            screen.blit(pg.font.Font('Pixel.ttf',28).render( title_word, True, (255,255,255),(50,50,50) ),(100,100))

    def click(self):

        if not(self.rect.y <=(-500 *(screen_w/self.img.get_size()[0]))):
            self.rect.y = (-500 *(screen_w/self.img.get_size()[0]))
        else: self.start =True
class Map(pg.sprite.Sprite):
    def __init__(self,x,y,right=0,top=0,left=0,bottom=0) :
        pg.sprite.Sprite.__init__(self)
        self.img = [pg.image.load(os.path.join('./img/map','map%d.png'%i)).convert_alpha() for i in range(6)]
        self.img_size = self.img[0].get_size()
        self.img_grid = ( screen_w//self.img_size[0]+1, screen_h//self.img_size[1]+1 )
        self.image = pg.Surface((self.img_grid[0] * self.img_size[0]   ,self.img_grid[1] * self.img_size[1] )).convert_alpha()
        for i in range(self.img_grid[0]):
            for j in range(self.img_grid[1]):
                self.image.blit(self.img[0],(self.img_size[0] * i , self.img_size[1] * j))
                if rd.random()<=0.05:
                    self.image.blit(self.img[rd.randint(1,5)],(self.img_size[0] * i , self.img_size[1] * j))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width / 2 
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.right,self.top,self.left,self.bottom = right,top,left,bottom

    def update(self):
        self.x += mo_x 
        self.y += mo_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.extend()

        
    def extend(self): #right=0,top=0,left=0,bottom=0)
        if self.rect.right <= screen_w and self.right == 0 :
            self.right+=1
            map_ = Map(self.rect.right,self.rect.y,0,0,1,0)
            map_group.add(map_)

        elif self.rect.left >=0 and self.left == 0 :
            self.left+=1
            map_ = Map(self.rect.left - self.image.get_size()[0] , self.rect.y ,1,0,0,0)
            map_group.add(map_)

        elif self.rect.top >=0 and self.top == 0 :
            self.top+=1
            map_ = Map(self.rect.x , self.rect.top - self.image.get_size()[1]  ,1,0,1,1)
            map_group.add(map_)

        elif self.rect.bottom <= screen_h and self.bottom == 0 :
            self.bottom+=1
            map_ = Map(self.rect.x, self.rect.bottom  ,1,1,1,0)
            map_group.add(map_)

class obstacle(pg.sprite.Sprite):
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)
    def update(self):
        pass
def mo() :      #移動
    global mo_x , mo_y 
    keys = pg.key.get_pressed()
    mo_speed = play.mo_speed
    if keys[pg.K_UP] and keys[pg.K_RIGHT]:
        mo_x = -((mo_speed**2)/2)**0.5
        mo_y = ((mo_speed**2)/2)**0.5
        play.mo = 'up_right'
    elif keys[pg.K_DOWN] and keys[pg.K_RIGHT]:
        mo_x = -((mo_speed**2)/2)**0.5
        mo_y = -((mo_speed**2)/2)**0.5
        play.mo = 'down_right'
    elif keys[pg.K_UP] and keys[pg.K_LEFT]:
        mo_x = ((mo_speed**2)/2)**0.5
        mo_y = ((mo_speed**2)/2)**0.5
        play.mo = 'up_left'
    elif keys[pg.K_DOWN] and keys[pg.K_LEFT]:
        mo_x = ((mo_speed**2)/2)**0.5
        mo_y = -((mo_speed**2)/2)**0.5
        play.mo = 'down_left'
    elif keys[pg.K_DOWN]:
        mo_y = -mo_speed
        mo_x =0
        play.mo = 'down'
    elif keys[pg.K_UP]:
        mo_y = mo_speed
        mo_x = 0
        play.mo = 'up'
    elif keys[pg.K_LEFT]:
        mo_x = mo_speed
        mo_y = 0
        play.mo = 'left'
    elif keys[pg.K_RIGHT]:
        mo_x = -mo_speed
        mo_y =0
        play.mo = 'right'
    else :
        mo_x = 0 
        mo_y = 0
        play.mo = 'stop'

generate_x ,generate_y  = 0, 0
upper_limit ,variety , generate_time= 1 , 1.2, time.time()
def generate() :            #怪物生成
    global generate_x,generate_y,upper_limit,variety,generate_time

    if int(time_gap) % 5 == 0 and time.time() - generate_time > 2:
        generate_time = time.time()
        upper_limit *= variety

    if time_gap < 480:
        if generate_x != coordinate_x  and generate_y != coordinate_y and len(mon_group) <upper_limit:
            generate_x,generate_y = coordinate_x,coordinate_y
            if time_gap < 90:                           # <90

                if rd.randint(0,1) == 1:
                    mon = eevee()
                else: mon = snack()
            elif time_gap < 270 :                       #<270
                if upper_limit >= 30:
                    upper_limit = 30

                if rd.randint(0,1) == 1:
                    mon = cubone()
                else: mon = emboar() 
                
            elif time_gap < 360 :                     #<360
                if upper_limit >= 50:
                    upper_limit = 50
                mon = Farfetch()
            elif time_gap < 480 :                     #<480
                if upper_limit >= 60:
                    upper_limit = 60
                if rd.randint(0,1) == 1:
                    mon = Farfetch()
                else: mon = emboar_up() 

            
            all_spr.add(mon)
            mon_group.add(mon)
            
        if int(time_gap) in (90,120,150,270,280,320,350,400,450) :  #蝙蝠
            x=coordinate_x
            y=coordinate_y
            has = False
            for i in mon_group:
                if i.name == 'Golbat':
                    has = True
            if not(has):
                rdd = rd.randint(4,5) 
                for i in range(-rdd*15,rdd*15+1,rdd*15):
                    for j in range(-rdd*15,rdd*15+1,rdd*15):
                        mon = Golbat(x+i,y+j)
                        all_spr.add(mon)
                        mon_group.add(mon)



        if int(time_gap) == 220:                    # =200  石怪
            has = False
            for i in mon_group:
                if i.name == 'Geodude':
                    has = True
            if not(has):
                
                mon = Geodude()
                all_spr.add(mon)
                mon_group.add(mon)   

        elif int(time_gap) == 268 : 
            upper_limit = 1.4
            
        elif int(time_gap) == 290:                  #木木梟
            has = False
            for i in mon_group:
                if i.name == 'special_Rowlet':
                    has = True
            if not(has):
                for i in range(2):
                    for j in range(15):
                        mon = special_Rowlet(i,j-2)
                        all_spr.add(mon)
                        mon_group.add(mon)


    elif time_gap >= 480 :
        has = False
        for i in mon_group:
            if i.name == 'pikachu':
                has = True
        if not(has):
            for i in mon_group:
                i.kill()
            mon = pikachu()
            all_spr.add(mon)
            mon_group.add(mon)

step = 0
time_start = 0
def game_turn():
    global step,time_start,play,map_,tit,upper_limit
    if step == 0:
        bullet_group.empty()
        mon_group.empty()
        map_group.empty()
        play_group.empty()
        all_spr.empty()
        tit = title()
        play_group.add(tit)
        step += 1
    elif step == 1 :
        pass
    elif step == 2:
        upper_limit = 1
        bullet_group.empty()
        mon_group.empty()
        map_group.empty()
        play_group.empty()
        all_spr.empty()
        play = human()
        map_ = Map(0,0)
        play_group.add(play)
        map_group.add(map_)
        all_spr.add(play)
        time_start = time.time()
        step += 1
    elif step == 3:
        generate()
        a =pg.sprite.groupcollide(mon_group,bullet_group,False,False,pg.sprite.collide_mask)
        for i in a:
            i.hurt(a[i][0].damage +play.buff_damage)

def stop() :
    global close,time_start,step
    stop_time =time.time()
    button_group.empty()
    for i in range(3):
        button = stop_choose_button(i)
        button_group.add(button)
    choose = 0
    pause = True

    while pause:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                choose += 1  
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                choose -= 1
            if choose < 0: choose = 0
            elif choose > 2 : choose = 2

            for i in button_group.sprites():
                if choose == i.i :
                    i.image = i.img[1]
                else:i.image = i.img[0]
                if (pg.key.get_pressed()[pg.K_SPACE] or pg.key.get_pressed()[pg.K_RETURN] )and choose == i.i :
                    if i.choose() == 1:
                        step = 2
                    elif i.choose() == 2 :
                        step = 0
                    pause = False

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause = False
            if event.type == pg.QUIT:
                close = True
                
        if close:break
        button_group.update()
        button_group.draw(screen)
        pg.display.update()
    time_start +=(time.time() - stop_time)

mon_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
play = human()
map_ = Map(0,0)
play_group = pg.sprite.Group()
all_spr = pg.sprite.Group()
map_group = pg.sprite.Group()
button_group = pg.sprite.Group()
num_group = pg.sprite.Group()


close = False
while True:
    clock.tick(240)  #偵率
    game_turn()
    random_coordinate() 
    mo()
    
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_t:     #按T +30秒
            time_start -= 30
        elif event.type == pg.KEYDOWN and event.key == pg.K_y :  #按Y -30秒
            if time_gap - 30 <= 0:
                time_start += time_gap
            else :
                time_start += 30
        elif event.type == pg.KEYDOWN and event.key == pg.K_u:  #按u可以升等
            play.experience = play.experience_slot
        elif event.type == pg.KEYDOWN and event.key == pg.K_s:  #按s可以加一萬寫
            play.blood_slot += 10000
            play.blood = play.blood_slot
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            stop()

        if event.type == pg.QUIT:
            close = True
            pg.quit()
        
    if close:break

    keys = pg.key.get_pressed()
    screen.blit(bg, (0,0))
    all_spr.update()
    map_group.update()
    map_group.draw(screen)
    time_gap = time.time() - time_start 
    screen.blit(pg.font.Font('Pixel.ttf',28).render( '%1.0f'%(time_gap), True, (255,255,255),(50,50,50) ),(100,100))
    all_spr.draw(screen)
    play_group.draw(screen)
    
    play_group.update()
    num_group.update()
    
    pg.display.update()
