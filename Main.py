import pygame
from pygame import *

from Board import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 640
BACKGROUND_COLOR = "#A60000"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Reversi")

    background = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background.fill(Color(BACKGROUND_COLOR))

    board = Board()

    text_font = pygame.font.Font(None, 30)
    current_move_text = text_font.render("Ход", 1, pygame.Color('black'))
    winner_text = text_font.render("Победитель", 1, pygame.Color('black'))
    help_text = text_font.render("Нет хода", 1, pygame.Color('black'))
    draw_text = text_font.render("Ничья", 1, pygame.Color('black'))
    run = True
    gold = pygame.image.load("gold1.png")
    black = pygame.image.load("black1.png")
    screen.blit(background, (0, 0))
    draw_board(screen)
    screen.blit(gold, (4 * 80 + 5, 3 * 80 + 5))
    screen.blit(black, (4 * 80 + 5, 4 * 80 + 5))
    screen.blit(black, (3 * 80 + 5, 3 * 80 + 5))
    screen.blit(gold, (3 * 80 + 5, 4 * 80 + 5))
    display_current_move(screen, current_move_text, black)
    screen.blit(help_text, (680, 600))
    pygame.display.update()
    while run:
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                check_pos(e.pos, board)
                screen.blit(background, (0, 0))
                screen.blit(help_text, (680, 600))
                draw_board(screen)
                for i in range(8):
                    for j in range(8):
                        if board.board[i][j] == "1":
                            screen.blit(gold, (j * 80 + 5, i * 80 + 5))
                        elif board.board[i][j] == "0":
                            screen.blit(black, (j * 80 + 5, i * 80 + 5))
                if board.current_move() == "0" and board.discs_on_board < 64:
                    display_current_move(screen, current_move_text, black)
                elif board.current_move() == "1" and board.discs_on_board < 64:
                    display_current_move(screen, current_move_text, gold)
                else:
                    get_winner(board, screen, winner_text, draw_text, gold, black)
                pygame.display.update()


def display_current_move(screen, text, disc_color):
    screen.blit(text, (700, 20))
    screen.blit(disc_color, (685, 60))


def check_pos(pos: tuple, board: Board):
    if 641 < pos[0] < 800 and 600 < pos[1] < 640:
        l = []
        for i in range(8):
            for j in range(8):
                if board.board[i][j] == "-":
                    l.append((i * 80, j * 80))
        if l:
            count = 0
            for k in l:
                if c(k, board):
                    break
                else:
                    count += 1
            if count == len(l):
                board.change_move()
    else:
        xpos, ypos = pos[0] // 80, pos[1] // 80
        slist = c(pos, board)
        if slist:
            board.board[ypos][xpos] = board.current_move()
            for fpos in slist:
                if board.current_move() == "1":
                    board.board[fpos[0]][fpos[1]] = "1"
                else:
                    board.board[fpos[0]][fpos[1]] = "0"
            board.discs_on_board += 1
            board.change_move()


def c(pos, board):
    pos = pos[0] // 80, pos[1] // 80
    xpos, ypos = pos[0], pos[1]
    if xpos <= 7 and ypos <= 7:
        lst = []  # проверяем есть ли вокруг выбранной клетки клетки другого цвета
        if board.board[pos[1]][pos[0]] == "-":
            for i in range(ypos - 1, ypos + 2):
                for j in range(xpos - 1, xpos + 2):
                    if i < 0 or i > 7 or j < 0 or j > 7:
                        continue
                    elif board.current_move() == "0" and board.board[i][j] == "1" \
                            or board.current_move() == "1" and board.board[i][j] == "0":
                        lst.append((j, i))  # lst[0] - x, lst[1] - y
        if lst:  # если нужные клетки есть, то перебираем
            slist = []
            for i in lst:
                if i[0] - xpos > 0:
                    xstep = 1
                elif i[0] - xpos < 0:
                    xstep = -1
                else:
                    xstep = 0
                if i[1] - ypos > 0:
                    ystep = 1
                elif i[1] - ypos < 0:
                    ystep = -1
                else:
                    ystep = 0
                flist = []
                for k in range(0, 8):
                    q = i[0] + xstep * k
                    w = i[1] + ystep * k
                    if q < 0 or w < 0 or q > 7 or w > 7:
                        continue
                    try:
                        if board.board[w][q] == "1" and board.current_move() == "0" or \
                                board.board[w][q] == "0" and board.current_move() == "1":
                            flist.append((w, q))
                            continue
                        if board.board[w][q] == "0" and board.current_move() == "0" or \
                                board.board[w][q] == "1" and board.current_move() == "1":
                            for e in flist:
                                slist.append(e)
                            break
                        if board.board[w][q] == "-":
                            flist.clear()
                            break
                    except IndexError:
                        continue
            return slist


def get_winner(board, screen, text, draw, gold, black):
    if board.discs_on_board == 64:
        count_1 = 0
        count_0 = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if board.board[i][j] == "1":
                    count_1 += 1
                else:
                    count_0 += 1
        if count_1 > count_0:
            screen.blit(text, (660, 20))
            screen.blit(gold, (685, 60))
        elif count_0 > count_1:
            screen.blit(text, (660, 20))
            screen.blit(black, (685, 60))
        else:
            screen.blit(draw, (660, 20))


def start_screen():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Reversi")

    background = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background.fill(Color(BACKGROUND_COLOR))

    play_font = pygame.font.Font(None, 120)
    rules_font = pygame.font.Font(None, 60)
    s_start = play_font.render("Играть", 1, pygame.Color('black'))
    s_rules = rules_font.render("Правила", 1, pygame.Color('black'))

    run = True
    screen.blit(background, (0, 0))
    screen.blit(s_start, (265, 300))
    screen.blit(s_rules, (315, 400))
    pygame.display.update()
    while run:
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if 270 <= e.pos[0] <= 540 and 306 <= e.pos[1] <= 390:
                    main()
                    run = False
                elif 310 <= e.pos[0] <= 495 and 400 <= e.pos[1] <= 450:
                    rules_screen()
                    run = False


def rules_screen():
    pygame.init()
    screen = pygame.display.set_mode((1300, WINDOW_HEIGHT))
    pygame.display.set_caption("Reversi")
    arrow = pygame.image.load("long-arrow-left.png")
    arrow = pygame.transform.scale(arrow, (70, 70))
    background = Surface((1300, WINDOW_HEIGHT))
    background.fill(Color(BACKGROUND_COLOR))
    text_font = pygame.font.Font(None, 30)
    intro_text = ["• Первый ход делают чёрные. Далее игроки ходят по очереди.",
                  "• Делая ход, игрок должен поставить свою фишку на одну из клеток доски таким образом, чтобы между этой поставленной",
                  "фишкой и одной из имеющихся уже на доске фишек его цвета находился непрерывный ряд фишек соперника,",
                  "горизонтальный, вертикальный или диагональный (другими словами, чтобы непрерывный ряд фишек",
                  "соперника оказался «закрыт» фишками игрока с двух сторон). Все фишки соперника, входящие в «закрытый»",
                  "на этом ходу ряд, переворачиваются на другую сторону (меняют цвет) и переходят к ходившему игроку.",
                  "• Если в результате одного хода «закрывается» одновременно более одного ряда фишек противника,",
                  "то переворачиваются все фишки, оказавшиеся на всех «закрытых» рядах.",
                  "• Игрок вправе выбирать любой из возможных для него ходов. Если игрок имеет возможные ходы, он не может отказаться",
                  "от хода. Если игрок не имеет допустимых ходов, то ход передаётся сопернику.",
                  "• Игра прекращается, когда на доску выставлены все фишки или когда ни один из игроков не может сделать хода. ",
                  "По окончании игры проводится подсчёт фишек каждого цвета, и игрок, чьих фишек на доске выставлено больше,",
                  "объявляется победителем. В случае равенства количества фишек засчитывается ничья."]
    run = True
    screen.blit(background, (0, 0))
    screen.blit(arrow, (10, 10))
    for i in range(len(intro_text)):
        s = text_font.render(intro_text[i], 1, pygame.Color("black"))
        screen.blit(s, (20, 90 + 40 * i))
    pygame.display.update()
    while run:
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN:
                if 5 <= e.pos[0] <= 85 and 5 <= e.pos[1] <= 85:
                    run = False
                    start_screen()


def draw_board(screen):
    pygame.draw.line(screen, Color("#000000"), (0, 0), (0, 640), 10)
    for i in range(8):
        pygame.draw.line(screen, Color("#000000"), (i * 80, 0), (i * 80, 640), 5)
    pygame.draw.line(screen, Color("#000000"), (640, 0), (640, 640), 5)
    pygame.draw.line(screen, Color("#000000"), (0, 0), (640, 0), 10)
    pygame.draw.line(screen, Color("#000000"), (0, 640), (640, 640), 12)
    for i in range(8):
        pygame.draw.line(screen, Color("#000000"), (0, i * 80), (640, i * 80), 5)


if __name__ == '__main__':
    start_screen()
