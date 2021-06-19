import sys
from tkinter import *
import random
import time
from tkinter import messagebox
import os
ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

tk = Tk()
canvas = Canvas(tk, width=800, height=600)
canvas.pack()

backgroup_image = PhotoImage(file=str(ROOT_DIR) + "\\image\\Backgroup.png")
backgroup_id = canvas.create_image(400,300,anchor=CENTER,image=backgroup_image)

card1 = PhotoImage(file=str(ROOT_DIR) + "\\image\\laser_tank.png")
card2 = PhotoImage(file=str(ROOT_DIR) + "\\image\\maid.png")
card3 = PhotoImage(file=str(ROOT_DIR) + "\\image\\GI.png")
card4 = PhotoImage(file=str(ROOT_DIR) + "\\image\\seal.png")
card5 = PhotoImage(file=str(ROOT_DIR) + "\\image\\tank.png")

place1 = PhotoImage(file=str(ROOT_DIR) + "\\image\\Laser_tank_card.png")
place2 = PhotoImage(file=str(ROOT_DIR) + "\\image\\Maid_card_id.png")
place3 = PhotoImage(file=str(ROOT_DIR) + "\\image\\card_GI.png")
place4 = PhotoImage(file=str(ROOT_DIR) + "\\image\\card_SEAL.png")
place5 = PhotoImage(file=str(ROOT_DIR) + "\\image\\card_tank.png")

status = 0
funds = 50
price = 0
tags = 'stand by'
barmoney = canvas.create_text(686,570, fill ="white" , font="Times 18 italic bold" , text="Money: "+str(int(funds)))

canvas.create_image(94,515,anchor=CENTER,image=place1,tags="obj1Tag")
canvas.create_image(191,515,anchor=CENTER,image=place2,tags="obj2Tag")
canvas.create_image(288,515,anchor=CENTER,image=place3,tags="obj3Tag")
canvas.create_image(385,515,anchor=CENTER,image=place4,tags="obj4Tag")
canvas.create_image(482,515,anchor=CENTER,image=place5,tags="obj5Tag")
tk.title('Military VS Dangerous(Alpha Test)')

def spawnzombie(count):
    if count > 0:
        tk.after(1000, spawnzombie, count-1)
    else:
        select = [183,298,420]
        for i in range(2):
            x = random.randint(800,810)
            y = random.choice(select)
            enemy.append(Zombie(canvas,x,y))
        spawnzombie(10)

def spawnmoney(count):
    if count > 0:
        tk.after(1000, spawnmoney, count-1)
    else:
        x = random.randint(80,725)
        money.append(Money(canvas,x))
        spawnmoney(5)
        
def cancel(event):
    global status
    global check
    if status == 1:
        canvas.delete(check)
        status = 0

def motion(event):
    global status
    global check
    if status == 1:
        x, y = event.x, event.y
        canvas.coords(check,x,y)
    
def click(event):
    global status
    global check
    global tags
    global funds
    global price
    global barmoney
    global use
    global damage 
    item = canvas.find_closest(event.x,event.y)[0]
    tags = canvas.gettags(item)
    if status == 0:    
        if tags[0] == "obj1Tag":
            price = 200
            if funds >= price:
                card1_id = canvas.create_image(event.x,event.y,anchor=CENTER,image=card1)
                check = card1_id
                use = PhotoImage(file=str(ROOT_DIR) + "\\image\\laser_tank.png")
                damage = 5
                status = 1
            else:
                pass
        
        elif tags[0] == "obj2Tag":
            price = 150
            if funds >= price:
                card2_id = canvas.create_image(event.x,event.y,anchor=CENTER,image=card2)
                check = card2_id
                use = PhotoImage(file=str(ROOT_DIR) + "\\image\\maid.png")
                damage = 4
                status = 1
            else:
                pass
        
        elif tags[0] == "obj3Tag":
            price = 35
            if funds >= price:
                card3_id = canvas.create_image(event.x,event.y,anchor=CENTER,image=card3)
                check = card3_id
                use = PhotoImage(file=str(ROOT_DIR) + "\\image\\GI.png")
                damage = 2
                status = 1
            else:
                pass
            
        elif tags[0] == "obj4Tag":
            price = 25
            if funds >= price:
                card4_id = canvas.create_image(event.x,event.y,anchor=CENTER,image=card4)
                check = card4_id
                use = PhotoImage(file=str(ROOT_DIR) + "\\image\\seal.png")
                damage = 1
                status = 1
            else:
                pass
        
        elif tags[0] == "obj5Tag":
            price = 100
            if funds >= price:
                card5_id = canvas.create_image(event.x,event.y,anchor=CENTER,image=card5)
                check = card5_id
                use = PhotoImage(file=str(ROOT_DIR) + "\\image\\tank.png")
                damage = 3
                status = 1
            else:
                pass
        
        elif tags[0] == "money":
            pass

            
    else:
        canvas.delete(check)
        unit.append(Defense(canvas,event.x,event.y,use,damage))
        funds -= price
        canvas.delete(barmoney)
        barmoney = canvas.create_text(686,570, fill ="white" , font="Times 18 italic bold" , text="Money: "+str(int(funds)))
        status = 0
        tags = 'stand by'
    

class Zombie:
    def __init__(self, canvas,x,y):
        self.live = random.randint(10,20)
        self.images = PhotoImage(file=str(ROOT_DIR) + "\\image\\zombie.png")
        self.canvas = canvas
        self.x = x
        self.v = 2
        self.y = y
        self.canvas_id = canvas.create_image(self.x ,self.y, anchor=SW,
                                             image=self.images)
        self.damage = 1
    
    def move(self):
        self.x -= self.v
        self.canvas.move(self.canvas_id, -self.v,0)
                
    def update(self):
        if self.live <= 0:
            self.canvas.delete(self.canvas_id)
            enemy.remove(self)
            

class Defense:
    def __init__(self, canvas,x,y,images,damage):
        self.live = 5
        self.images = images
        self.canvas = canvas
        self.ammo = []
        self.x = x
        self.y = y
        self.damage = damage
        self.canvas_id = canvas.create_image(self.x ,self.y, anchor=CENTER,
                                             image=self.images)    

    def build_bullet(self):
        for check in enemy:
            if len(self.ammo) < 1:
                self.ammo.append(Bullet(canvas,self.x+60,self.y))
    
    def update(self):
        for check in enemy:
            if self.x >= check.x and self.x <= check.x+109 and self.y >= check.y-62 and self.y <= check.y+62:
                self.canvas.delete(self.canvas_id)
                unit.remove(self)
    
class Bullet:
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.images = PhotoImage(file=str(ROOT_DIR) + "\\image\\bullet.png")
        self.v = 5
        self.x = x
        self.y = y
        self.canvas_id = canvas.create_image(self.x ,self.y, anchor=SW,
                                             image=self.images)
    def move_hit(self):
        self.x += self.v
        self.canvas.move(self.canvas_id, self.v,0)
                
class Money:
    def __init__(self,canvas,x):
        self.x = x
        self.y = 10
        self.v = 0.5
        self.fund = 25
        self.canvas = canvas
        self.images = PhotoImage(file=str(ROOT_DIR) + "\\image\\money.png")
        self.canvas_id = canvas.create_image(self.x ,self.y, anchor=CENTER,
                                             image=self.images,tags = 'money')
        
    def move(self):
        self.y += self.v
        self.canvas.move(self.canvas_id, 0, +self.v)
        
    def update(self):
        global tags
        global funds
        global barmoney
        if tags[0] == 'money':
            canvas.delete(self.canvas_id)
            money.remove(self)
            funds += self.fund
            canvas.delete(barmoney)
            tags = 'stand by'
            barmoney = canvas.create_text(686,570, fill ="white" , font="Times 18 italic bold" , text="Money: "+str(int(funds)))
        
unit = []
enemy = []
money = []
count = 0
messagebox.showinfo("Message","Prees OK to Start the game.")
spawnzombie(3)
spawnmoney(8)

canvas.bind("<Button-1>", click)
canvas.bind("<Button-3>", cancel)
canvas.bind('<Motion>', motion)
while True:
    
    for zombies in enemy:
        zombies.move()
        if zombies.x <= -100:
            messagebox.showinfo("Message","Game Over.")
            tk.destroy()
    
    for down in money:
        down.move()
        down.update()
    
    for units in unit:
        for zombies in enemy:
            if units.x < zombies.x:
                units.build_bullet()
                for fire in units.ammo:
                        fire.move_hit()
                        if fire.x >= zombies.x and fire.x <= zombies.x+109 and fire.y <= zombies.y+62 and fire.y >= zombies.y-62:
                            zombies.live -= units.damage
                            canvas.delete(fire.canvas_id)
                            units.ammo.remove(fire)
                            if zombies.live <= 0:
                                zombies.update()
                                count += 1
    
    for units in unit:                    
        for fire in units.ammo:
            if fire.x >= 800:
                canvas.delete(fire.canvas_id)
                units.ammo.remove(fire)
            elif len(enemy) <= 0:
                canvas.delete(fire.canvas_id)
                units.ammo.remove(fire)
    
    for units in unit:             
        units.update()
    
    if count >=20:
        messagebox.showinfo("Message","Great Job, You Pass.")
        tk.destroy()
    time.sleep(0.03)
    tk.update()
