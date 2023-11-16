import pygame as pg
from pygame.locals import *
import os
import json

value = 0
pg.font.init()
font = pg.font.SysFont('cutoutoffontregular', 32)
pg.init()

screen = pg.display.set_mode([720, 1000])
running = True
pg.display.set_caption('Habit')
clock = pg.time.Clock()

class Data:

    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            self.stats = json.loads(file.read())
            file.close()

    def set_value(self, category, val):
        if category == 'health':
            if val >= 100:
                self.stats['health'] = 100
            else:
                self.stats[category] = val
        if category == 'coins':
            if val < 0:
                self.stats["coins"] = 0
            else:
                self.stats[category] = val
        if category == 'exp':
            self.stats[category] = val
        if category == 'inventory_items':
            self.stats[category] = val
        with open('data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.stats))
            file.close()


class FoodItem:
    def __init__(self, img_path, name, weight):
        self.name = name
        self.image = pg.transform.scale(pg.image.load(img_path), (140, 140))
        self.rect = None
        self.weight = weight

    def __str__(self):
        return self.name

class ShopItem:
    def __init__(self, name, cost, x, y):
        self.img = pg.transform.scale(pg.image.load(f'img/food/{name}.png'), (180, 180))
        self.name = name
        self.cost = cost
        self.cost_font = font.render(str(cost), True, (255, 255, 255))
        self.coin_img = pg.transform.scale(pg.image.load(f'img/coin.png'), (50, 50))
        self.rect = pg.draw.rect(screen, (0, 0, 0), pg.Rect(x, y, 200, 200), 10, 3)

class InventoryItem:
    def __init__(self, x, y, name = None, amount = None):
        self.name = name
        self.amount = amount
        if self.amount:
            self.amount_font = font.render(str(self.amount), True, (255, 255, 255))
        if name:
            self.img = pg.transform.scale(pg.image.load(f'img/food/{name}.png'), (180, 180))
        self.rect = pg.draw.rect(screen, (0, 0, 0), pg.Rect(x, y, 200, 200), 10, 3)

    def __str__(self):
        return str(self.name)

class ContainerItem:
    def __init__(self, name, cost, y):
        self.name = font.render(name, True, (0, 0, 0))
        self.cost_font = font.render(str(cost), True, (0, 0, 0))
        self.cost = cost
        self.rect = pg.Rect(20, y, 680, 100)
        

data = Data('data.json')

class Menu:

    def __init__(self):
        self.state = False
        self.bad = False
        self.good = False
        self.shop = False
        self.inventory = False
        self.myitems = False
        
        self.images = [pg.image.load("img/pet/"+str(i)+".png") for i in range(1, 16)]
        self.value = 0
        self.coin_positions = [225, 345, 465, 585, 705, 825]

        self.levels = [100, 150, 250, 400, 600, 850, 1050, 1400, 1800, 2250]
        
        self.food_positions = [10, 190, 370, 550]
        self.food_list = [FoodItem(f'img/food/{i[0]}.png', i[0], i[1]) for i in data.stats["food_list_quick"]]

        self.positions = [200, 320, 440, 560, 680, 800]
        self.coin_img = pg.image.load('img/coin.png')
        self.coin_img = pg.transform.scale(self.coin_img, (50, 50))
        
        self.shop_positions = [[20, 220], [260, 220], [500, 220],
                               [20, 485], [260, 485], [500, 485],
                               [20, 750], [260, 750], [500, 750]]
        
        self.shop_coins_positions = [[20, 420], [260, 420], [500, 420],
                                     [20, 685], [260, 685], [500, 685],
                                     [20, 950], [260, 950], [500, 950]]
        self.shop_items = []
        
        
        self.inventory_items = []
        self.temp_inv = data.stats["inventory_items"]

                
        for i, item in enumerate(data.stats["shop_items"]):
                self.shop_items.append(ShopItem(item[0], item[1], *self.shop_positions[i]))

        self.good_img = pg.image.load('img/good.png')
        self.goods = self.good_img.get_rect()
        self.goods_btn = pg.Rect((310, 0), (315, 100))
        self.good_list = data.stats['good_list']
        

        self.bad_img = pg.image.load('img/bad.png')
        self.bads = self.bad_img.get_rect()
        self.bads_btn = pg.Rect((0, 0), (310, 100))
        self.bad_list = data.stats["bad_list"]

        self.inventory_img = pg.image.load('img/inventory.png')
        self.cart_img = pg.transform.scale(pg.image.load('img/cart.png'), (160, 160))
        self.heart_img = pg.transform.scale(pg.image.load('img/heart.png'), (50, 50))
        self.close_btn = pg.Rect((625, 0), (95, 100))

    def bad_habits(self):
        if self.state:
            self.bad = True
            self.good = False
            self.shop = False
            self.myitems = False
            self.bad_rect_list = []
            screen.blit(self.bad_img, self.bads)
            screen.blit(self.heart_img, (20, 125))
            screen.blit(font.render(str(data.stats["health"]), True, (255, 255, 255)), (70, 125, 400, 100))
            pg.draw.rect(screen, (0, 0, 0), (0, 0, 310, 100), 10)

            for i, hab in enumerate(self.bad_list):
                self.bad_rect_list.append(ContainerItem(hab[0], hab[1], self.positions[i]))
                
            for i, hub in enumerate(self.bad_rect_list):
                pg.draw.rect(screen, (255, 255, 255), hub.rect)
                screen.blit(hub.name, (20, self.positions[i]+30, 680, 100))
                screen.blit(self.heart_img, (625, self.coin_positions[i]))
                screen.blit(hub.cost_font, (495, self.coin_positions[i]))
            

    def good_habits(self):
        if self.state:
            self.good = True
            self.bad = False
            self.shop = False
            self.myitems = False
            self.good_rect_list = []
            screen.blit(self.good_img, self.goods)
            screen.blit(self.coin_img, (20, 125))
            screen.blit(font.render(str(data.stats["coins"]), True, (255, 255, 255)), (70, 125, 400, 100))
            pg.draw.rect(screen, (0, 0, 0), (310, 0, 315, 100), 10)
            
            for i, hab in enumerate(self.good_list):
                self.good_rect_list.append(ContainerItem(hab[0], hab[1], self.positions[i]))
                
            for i, hub in enumerate(self.good_rect_list):
                pg.draw.rect(screen, (255, 255, 255), hub.rect)
                screen.blit(hub.name, (20, self.positions[i]+30, 680, 100))
                screen.blit(self.coin_img, (625, self.coin_positions[i]))
                screen.blit(hub.cost_font, (540, self.coin_positions[i]))
    
    def shop_meth(self):
        if self.inventory:
            self.myitems = False
            self.bad = False
            self.good = False
            self.shop = True
            screen.blit(self.inventory_img, self.inventory_img.get_rect()) 
            screen.blit(self.coin_img, (285, 125))
            screen.blit(font.render(str(data.stats["coins"]), True, (255, 255, 255)), (335, 125, 400, 100))
            pg.draw.rect(screen, (255, 255, 255), (0, 0, 310, 100), 10)
            
            for i, item in enumerate(self.shop_items):
                screen.blit(item.coin_img, self.shop_coins_positions[i])
                screen.blit(item.cost_font, [self.shop_coins_positions[i][0]+50, self.shop_coins_positions[i][1]+25])
                screen.blit(item.img, [self.shop_positions[i][0]+10, self.shop_positions[i][1]+10])
                pg.draw.rect(screen, (0, 0, 0), item.rect, 10, 3)

    def inventory_meth(self):
        if self.inventory:
            self.myitems = True
            self.bad = False
            self.good = False
            self.shop = False   
            screen.blit(self.inventory_img, self.inventory_img.get_rect())
            pg.draw.rect(screen, (255, 255, 255), (310, 0, 315, 100), 10)
            self.temp_inv = data.stats["inventory_items"]
            self.inventory_items = []
            for i in range(9):
                try:    
                    self.inventory_items.append(InventoryItem(*self.shop_positions[i], data.stats["inventory_items"][i][0], data.stats["inventory_items"][i][1]))
                except:
                    self.inventory_items.append(InventoryItem(*self.shop_positions[i]))
            for i, item in enumerate(self.inventory_items):
                
                pg.draw.rect(screen, (0, 0, 0), item.rect, 10, 3)
                try:
                    
                    if item.amount > 0:
                        screen.blit(item.img, (self.shop_positions[i][0]+10, self.shop_positions[i][1]+10))
                        screen.blit(item.amount_font, (self.shop_positions[i][0]+15, self.shop_positions[i][1]+160))
                except: pass
                
            
            
            
    def draw_menu(self):

        if self.state:
            if self.good: self.good_habits()
            else: self.bad_habits()
        elif self.inventory:
            if self.shop: self.shop_meth()
            else: self.inventory_meth()
        

    def close_menu(self, screen):
        self.state = False
        self.inventory = False
        self.shop = False
        self.myitems = False
        self.good = False
        self.bad = False
        screen.fill((20, 20, 20))
        
        self.value+=1
        pg.draw.rect(screen, (255, 255, 255), (635, 20, 75, 10))
        pg.draw.rect(screen, (255, 255, 255), (635, 40, 75, 10))
        pg.draw.rect(screen, (255, 255, 255), (635, 60, 75, 10))
    
    def animate(self):
        
        if self.value >= len(self.images):
            self.value = 0
        screen.blit(self.images[self.value], (100, 250))
        clock.tick(7)
        self.value+=1
        for i, pos in enumerate(self.food_positions[:-1]):
            pg.draw.rect(screen, (255, 255, 255), pg.Rect(pos, 800, 160, 160), 10, 3)
            screen.blit(self.food_list[i].image, (pos+10, 810))
            self.food_list[i].rect = pg.Rect((pos+10, 810), (140, 140))
        screen.blit(self.cart_img, (self.food_positions[-1], 800))
        
        pg.draw.rect(screen, (20, 80, 0), pg.Rect((10, 90),(300, 20 )), 5, 3)
        
        for i in range(len(self.levels)):
            if data.stats["exp"] < self.levels[i]:
                curr_lvl = i+1
                break
        pg.draw.rect(screen, (0, 255, 0), pg.Rect((15, 95), (290*(data.stats["exp"] - self.levels[curr_lvl-2])/(self.levels[curr_lvl-1]-self.levels[curr_lvl-2]), 10)), 5, 1)
        screen.blit(font.render(str( data.stats["exp"] - self.levels[curr_lvl-2])+f" / {self.levels[curr_lvl-1] - self.levels[curr_lvl-2]}", True, (255, 255, 255)), (20, 125, 400, 100))
        screen.blit(font.render(str(curr_lvl), True, (255, 255, 255)), (325, 100, 400, 100))

    

menu = Menu()

while running:
    
    if menu.state == False and menu.inventory == False:
            screen.fill((20, 20, 20))
            pg.draw.rect(screen, (255, 255, 255), (635, 20, 75, 10))
            pg.draw.rect(screen, (255, 255, 255), (635, 40, 75, 10))
            pg.draw.rect(screen, (255, 255, 255), (635, 60, 75, 10))
            pg.draw.rect(screen, (89, 17, 4), (10, 10, 500, 70), 10)
            pg.draw.rect(screen, (255, 0, 0), (20, 20, int(4.8*data.stats["health"]), 50))
            menu.animate()


    for event in pg.event.get():
        menu.draw_menu()
        
        if event.type == pg.QUIT:
            running = False
        

        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if menu.state == True:
                if menu.bad:
                    for i in menu.bad_rect_list:
                        if i.rect.collidepoint(pos):
                            pg.draw.rect(screen, (0, 255, 0), i.rect)
                            data.set_value("health", data.stats["health"]+i.cost)
                elif menu.good:
                    for i in menu.good_rect_list:
                        if i.rect.collidepoint(pos):
                            pg.draw.rect(screen, (0, 255, 0), i.rect)
                            data.set_value("coins", data.stats["coins"]+i.cost)
            elif menu.state == False and menu.inventory == False:
                for i in menu.food_list:
                    if i.rect.collidepoint(pos):
                        for j in menu.temp_inv:
                            if j[0] == i.name:
                                j[1] -= 1
                                data.set_value("inventory_items", menu.temp_inv)
                        screen.blit(font.render("+"+str(i.weight), True, (255, 255, 255)), (510, 15, 10, 10))
                        clock.tick(3)
                        data.set_value("health", data.stats["health"]+i.weight)
                        data.set_value("exp", data.stats["exp"]+i.weight)
            if pg.Rect((550, 800), (160, 160)).collidepoint(pos) and menu.state == False and menu.inventory == False:
                menu.inventory = True
                menu.bad = False
                menu.good = False
                menu.shop = True
                menu.myitems = False
                menu.state = False
                

            elif menu.bads_btn.collidepoint(pos) and menu.state:
                
                menu.bad = False
                menu.good = True
                

            elif menu.goods_btn.collidepoint(pos) and menu.state:

                menu.bad = True
                menu.good = False
                


            elif menu.bads_btn.collidepoint(pos) and menu.inventory:
                
                menu.shop = True
                menu.myitems = False
                

            elif menu.goods_btn.collidepoint(pos) and menu.inventory:

                menu.shop = False
                menu.myitems = True
                
            
            elif menu.close_btn.collidepoint(pos):
                if menu.state or menu.inventory:
                
                    pg.draw.rect(screen, (255, 255, 255), (625, 0, 95, 100), 10)
                    menu.close_menu(screen)
                elif not(menu.state) and not(menu.inventory):
                    menu.state = True
                    menu.good = True

            elif menu.shop:
                for i in menu.shop_items:
                    if i.rect.collidepoint(pos):
                        if data.stats["coins"] >= i.cost:
                            pg.draw.rect(screen, (255, 255, 255), i.rect, 10, 3)
                            data.set_value("coins", data.stats["coins"]-i.cost)
                            for j, item in enumerate(menu.temp_inv):
                                if item[0] == i.name:
                                    item[1]+=1
                                    data.set_value("inventory_items", menu.temp_inv)
                                    print(menu.temp_inv)
                                    print(data.stats["inventory_items"])
                            
                                    
            
            

    pg.display.update()
    
    pg.display.flip()

pg.quit()
