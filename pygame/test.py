import itertools, sys, time, random, math, pygame
from pygame.locals import *
from test2 import *

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x,y))

def calc_velocity(direction, vel=1.0):
    velocity = Point(0,0)
    if direction == 0: #上
        velocity.y = -vel
    elif direction == 2: #右
        velocity.x = vel
    elif direction == 4: #下
        velocity.y = vel
    elif direction == 6: #左
        velocity.x = -vel
    return velocity


pygame.init()
screen = pygame.display.set_mode((1000,780))
pygame.display.set_caption("test")
font = pygame.font.Font(None, 90)
timer = pygame.time.Clock() #创建时钟对象

player_group = pygame.sprite.Group()
doge_group = pygame.sprite.Group()


player = MySprite()
player.load("people.png", 96, 96, 8)
player.position = 0,0
player.direction = 4
player_group.add(player)

x=13
for n in range(1,x):
    doge = MySprite();
    doge.load("doge.png", 90,90,1)
    doge.position = random.randint(50,900),random.randint(50,700)
    doge_group.add(doge)



win = False
fail = False
player_moving = False
time = 100
score = 0

while True:
    timer.tick(30)  # 设置帧率
    if not fail and not win:
        time -= 0.4;
    ticks = pygame.time.get_ticks()

    #关闭
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_w]:
        player.direction = 0
        player_moving = True
    elif keys[K_d]:
        player.direction = 2
        player_moving = True
    elif keys[K_s]:
        player.direction = 4
        player_moving = True
    elif keys[K_a]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False

    if not fail and not win:
        #根据角色的不同方向，使用不同的动画帧
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns-1
        if player.frame < player.first_frame:
            player.frame = player.first_frame
        if not player_moving:
            #当停止按键（即人物停止移动的时候），停止更新动画帧
            player.frame = player.first_frame = player.last_frame
        else: 
            player.velocity = calc_velocity(player.direction, 1.5)
            player.velocity.x *= 7
            player.velocity.y *= 7


        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0:
                player.X = 0
            elif player.X > 950:
                player.X = 950
            if player.Y < 0:
                player.Y = 0
            elif player.Y > 730:
                player.Y = 730

        #检测碰撞
        attacker = pygame.sprite.spritecollideany(player, doge_group)
        if attacker != None:
            doge_group.remove(attacker);
            score += 100

        #判断游戏胜利失败
        if time <= 0:
            fail = True
        elif len(doge_group) == 0:
            win = True


        player_group.update(ticks, 50)
        doge_group.update(ticks, 50)


    screen.fill((0,0,0))

    doge_group.draw(screen)
    player_group.draw(screen)


    if win:
        print_text(font, 250, 100, "win score = " + str(score))
    elif fail:
        print_text(font, 250, 100, "Fail score = " + str(score))

    pygame.draw.rect(screen, (50,150,50,180), Rect(400,750,time * 2,25))
    pygame.draw.rect(screen, (100,200,100,180), Rect(400,750,200,25), 2)
    
    pygame.display.update()
