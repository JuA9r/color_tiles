import pygame as pg
from pygame.locals import *
import sys
import random
from time import sleep


# ブロックサイズを20に指定
# 6つの色をリストに格納
rect_s = 20
colors: list[str] = ["cyan", "orange", "lime", "gold", "magenta", "pink"]
field_s: list[int] = [20, 15]
field = [[None for j in range(field_s[0])] for i in range(field_s[1])]

# 面の横と縦のサイズ
WIDTH = 600
HEIGHT = 450
title = "Start"
n = 250  # ブロックの生成個数
Time = 5  # タイマーの時間
g_time = 90  # ゲームの制限時間


def gene_rand_rect():
    """
    Generate blocks with random colors and coordinates
    """
    return [
        random.randint(0, len(field[0])-1),
        random.randint(0, len(field)-1),
        colors[random.randint(0, len(colors)-1)]
    ]
    # リスト内にある色をランダムに取り出す


def draw_rect(screen, field, rect_s):
    """
    Export background blocks at random coordinates
    """
    for y, field_row in enumerate(field):
        for x, data in enumerate(field_row):
            if (x+y) % 2 == 0:
                pg.draw.rect(
                            screen, (245, 245, 245),
                            (
                                x*(rect_s+10), y*(rect_s+10),
                                rect_s+10, rect_s+10
                            )
                        )
            if data is None:
                continue
            pg.draw.rect(
                screen, data[2], (
                    data[0]*(rect_s+10)+5, data[1]*(rect_s+10)+5,
                    rect_s, rect_s
                                  )
                         )
    pg.display.update()


def mouse_click():
    """
    :return:
    Delete field block data on screen
    """
    comp_c = []
    mouse_pos = pg.mouse.get_pos()
    x_i = mouse_pos[0]//(rect_s+10)
    y_i = mouse_pos[1]//(rect_s+10)

    try:
        if field[y_i][x_i] is not None:  # fieldに色のデータがあったら処理を行わない
            return
    except IndexError:
        pass

    for direct in [-1, 1]:
        try:
            for x_d in range(0, direct * field_s[0], direct):
                data = field[y_i][x_d+x_i]
                if data is None:
                    continue
                comp_c.append(data[2])
                break
        except IndexError:
            pass

        try:
            for y_d in range(0, direct*field_s[1], direct):
                data = field[y_d+y_i][x_i]
                if data is None:
                    continue
                comp_c.append(data[2])
                break
        except IndexError:
            pass

    col_lst = [x for i, x in enumerate(comp_c) if x in comp_c[:i]]  # comp_cに同じ色のデータがあるか調べる
    print(col_lst)

    print(comp_c)
    print(f"index of x and y --> x[{x_i}], y[{y_i}]\n")


def start_timer(secs):
    """
    five seconds countdown
    """
    for i in range(secs, -1, -1):
        print(i)
        sleep(1)
    print(title)

start_timer(Time)


class Score:
    """
    Score calculation
    :score_count:
    Add score according to the number of disappeared blocks
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT-50

    def score_count(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)


def main():
    """
    n = number of blocks : 220
    :while True:
    event,type processing: Processing by pressed key
    """
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("color tail")
    screen.fill((223, 223, 223))
    for i in range(n):
        while True:
            rect = gene_rand_rect()
            if field[rect[1]][rect[0]] is not None:
                continue
            field[rect[1]][rect[0]] = rect
            break
    draw_rect(screen, field, rect_s)

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f"mouse clicked --> ({x}, {y})")

            if event.type == MOUSEBUTTONDOWN:
                mouse_click()


if __name__ == "__main__":
    main()
