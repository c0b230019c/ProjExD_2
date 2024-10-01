import os
from random import randint
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数 : こうかとん または 爆弾のRect
    戻り値 : 真理値タプル(横判定結果, 縦判定結果)
    画面内ならTrue, 画面内ならFalse
    """
    line, vartical = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        line = False
    if obj_rct.top < 0 or  HEIGHT < obj_rct.bottom:
        vartical = False
    return line, vartical


def game_over(screen: pg.display) -> tuple[int, int]:
    """
    引数 : screen
    戻り値 : なし
    """
    bl_img = pg.Surface((WIDTH, HEIGHT)) # 空のSurface
    pg.draw.rect(bl_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    bl_img.set_alpha(128)
    go_font = pg.font.Font(None, 80)
    txt = go_font.render("Game Over", True,
                        (255, 255, 255))
    go_img = pg.image.load("fig/8.png")
    go_rct = go_img.get_rect()
    go_rct2 = go_img.get_rect()
    go_rct = (WIDTH-360)/2 , HEIGHT/2
    go_rct2 = (WIDTH+350)/2 , HEIGHT/2
    bl_rct = bl_img.get_rect()
    bl_rct = 0, 0
    screen.blit(bl_img, bl_rct)
    screen.blit(txt, [(WIDTH-270)/2, HEIGHT/2])
    screen.blit(go_img, go_rct)
    screen.blit(go_img, go_rct2)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    DELTA = {
        pg.K_UP:(0, -5),
        pg.K_DOWN:(0, 5),
        pg.K_LEFT:(-5, 0),
        pg.K_RIGHT:(5, 0)
        }
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20, 20)) # 空のSurface
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    # bl_img = pg.Surface((WIDTH, HEIGHT)) # 空のSurface
    # pg.draw.rect(bl_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    # bl_img.set_alpha(128)
    # go_font = pg.font.Font(None, 80)
    # txt = go_font.render("Game Over", True,
    #                      (255, 255, 255))
    # go_img = pg.image.load("fig/8.png")
    # go_rct = go_img.get_rect()
    # go_rct2 = go_img.get_rect()
    # go_rct = (WIDTH-360)/2 , HEIGHT/2
    # go_rct2 = (WIDTH+350)/2 , HEIGHT/2


    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect() # 爆弾rectの抽出
    bb_rct.center = randint(0, WIDTH), randint(0, HEIGHT)
    # bl_rct = bl_img.get_rect()
    # bl_rct = 0, 0
    vx, vy = 5 ,5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct): # こうかとんと爆弾が重なっていたら
            # screen.blit(bl_img, bl_rct)
            # screen.blit(txt, [(WIDTH-270)/2, HEIGHT/2])
            # screen.blit(go_img, go_rct)
            # screen.blit(go_img, go_rct2)
            game_over(screen)
            pg.display.update()
            time.sleep(5)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0] # 横方向
                sum_mv[1] += tpl[1] # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        line, vartical = check_bound(bb_rct)
        if not line:
            vx *= -1
        if not vartical:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
