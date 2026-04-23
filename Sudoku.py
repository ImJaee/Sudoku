import sys
import pygame

from generator import generate_sudoku
from sudokuBoardAndCell import Board, BOARD_PX

WIN_W = BOARD_PX
BTN_AREA = 80
WIN_H = BOARD_PX + BTN_AREA

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 95, 31)
ORANGE_HOV = (255, 157,0)
BG_GREY = (200, 200, 200)

DIFFICULTY = {"easy": 30, "medium": 40, "hard": 50}


def draw_button(screen, text, rect, font, hovered=False):
    colour = ORANGE_HOV if hovered else ORANGE
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = font.render(text, True, WHITE)
    lw, lh = label.get_size()
    screen.blit(label, (rect.x + (rect.w - lw) // 2,
                        rect.y + (rect.h - lh) // 2))

def screen_start(screen, clock):
    font_title = pygame.font.SysFont("times new roman", 48, bold=True)
    font_sub = pygame.font.SysFont("times new roman", 26, bold=True)
    font_btn = pygame.font.SysFont("times new roman", 22, bold=True)
    btn_w, btn_h = 120, 40
    gap = 20
    total = btn_w * 3 + gap * 2
    bx = (WIN_W - total) // 2
    by = WIN_H // 2 + 30
    btn_easy = pygame.Rect(bx, by, btn_w, btn_h)
    btn_medium = pygame.Rect(bx + btn_w + gap, by, btn_w, btn_h)
    btn_hard = pygame.Rect(bx + (btn_w + gap) * 2, by, btn_w, btn_h)
    bg_image = pygame.image.load("posterImage.png")
    bg_image = pygame.transform.scale(bg_image, (WIN_W, WIN_H))
    while True:
        screen.blit(bg_image, (0, 0))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_easy.collidepoint(event.pos):   return "easy"
                if btn_medium.collidepoint(event.pos): return "medium"
                if btn_hard.collidepoint(event.pos):   return "hard"

        tx = (WIN_W - font_title.size("Welcome to Sudoku")[0]) // 2
        ty = WIN_H // 2 - 100
        for ox, oy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            screen.blit(font_title.render("Welcome to Sudoku", True, BLACK), (tx + ox, ty + oy))
        screen.blit(font_title.render("Welcome to Sudoku", True, WHITE), (tx, ty))
        sx = (WIN_W - font_sub.size("Select Board Difficulty:")[0]) // 2
        sy = WIN_H // 2 - 20
        for ox, oy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            screen.blit(font_sub.render("Select Board Difficulty:", True, BLACK), (sx + ox, sy + oy))
        screen.blit(font_sub.render("Select Board Difficulty:", True, WHITE), (sx, sy))
        draw_button(screen, "EASY", btn_easy, font_btn, btn_easy.collidepoint(mx, my))
        draw_button(screen, "MEDIUM", btn_medium, font_btn, btn_medium.collidepoint(mx, my))
        draw_button(screen, "HARD", btn_hard, font_btn, btn_hard.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick()

def screen_game(screen, clock, difficulty):
    removed = DIFFICULTY[difficulty]
    gen = generate_sudoku(9, removed)
    board = Board(WIN_W, WIN_H, screen, removed,
                  gen.get_board(), gen.get_solution())
    font_btn = pygame.font.SysFont("arial", 20, bold=True)
    btn_h = 36
    btn_y = BOARD_PX + (BTN_AREA - btn_h) // 2
    btn_w = 120
    gap = (WIN_W - btn_w * 3) // 4
    btn_reset = pygame.Rect(gap, btn_y, btn_w, btn_h)
    btn_restart = pygame.Rect(gap * 2 + btn_w, btn_y, btn_w, btn_h)
    btn_exit = pygame.Rect(gap * 3 + btn_w * 2, btn_y, btn_w, btn_h)
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_reset.collidepoint(event.pos):
                    board.reset_to_original()
                elif btn_restart.collidepoint(event.pos):
                    return "restart"
                elif btn_exit.collidepoint(event.pos):
                    return None
                else:
                    result = board.click(*event.pos)
                    if result:
                        board.select(result[0], result[1])
            if event.type == pygame.KEYDOWN:
                cell = board.selected_cell
                if cell:
                    r, c = cell.row, cell.col
                    if event.key == pygame.K_UP and r > 0:
                        board.select(r - 1, c)
                    elif event.key == pygame.K_DOWN and r < 8:
                        board.select(r + 1, c)
                    elif event.key == pygame.K_LEFT and c > 0:
                        board.select(r, c - 1)
                    elif event.key == pygame.K_RIGHT and c < 8:
                        board.select(r, c + 1)
                    elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                        board.clear()
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if cell.sketched_value != 0:
                            board.place_number(cell.sketched_value)
                            if board.is_full():
                                return "win" if board.check_board() else "lose"
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        board.sketch(event.key - pygame.K_0)
        screen.fill(WHITE)
        board.draw()
        pygame.draw.rect(screen, BG_GREY, (0, BOARD_PX, WIN_W, BTN_AREA))
        draw_button(screen, "RESET", btn_reset, font_btn, btn_reset.collidepoint(mx, my))
        draw_button(screen, "RESTART", btn_restart, font_btn, btn_restart.collidepoint(mx, my))
        draw_button(screen, "EXIT", btn_exit, font_btn, btn_exit.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick()


def screen_win(screen, clock):
    return _end_screen(screen, clock, "Game Won!", "EXIT")


def screen_lose(screen, clock):
    return _end_screen(screen, clock, "Game Over :(", "RESTART")


def _end_screen(screen, clock, headline, btn_label):
    font_big = pygame.font.SysFont("times new roman", 60, bold=True)
    font_btn = pygame.font.SysFont("times new roman", 24, bold=True)

    btn = pygame.Rect((WIN_W - 140) // 2, WIN_H // 2 + 60, 140, 44)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos):
                    return "restart"

        screen.fill(WHITE)
        ht = font_big.render(headline, True, BLACK)
        screen.blit(ht, ((WIN_W - ht.get_width()) // 2, WIN_H // 2 - 60))
        draw_button(screen, btn_label, btn, font_btn, btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()

    while True:
        difficulty = screen_start(screen, clock)
        if difficulty is None:
            break
        result = screen_game(screen, clock, difficulty)
        if result == "win":
            outcome = screen_win(screen, clock)
        elif result == "lose":
            outcome = screen_lose(screen, clock)
        elif result == "restart":
            continue
        else:
            break
        if outcome != "restart":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

