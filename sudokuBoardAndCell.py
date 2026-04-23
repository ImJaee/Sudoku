import pygame

# ── Constants ──────────────────────────────────────────────────────────────────
BOARD_SIZE = 9
CELL_SIZE = 60  # pixels per cell
BOARD_PX = CELL_SIZE * BOARD_SIZE  # 540
LINE_THIN = 1
LINE_THICK = 3

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (220, 220, 220)
MID_GREY = (160, 160, 160)
DARK_GREY = (50, 50, 50)
RED = (200, 30, 30)
BLUE = (30, 80, 180)
PENCIL = (100, 100, 200)  # sketched-value colour


# ══════════════════════════════════════════════════════════════════════════════
# Cell
# ══════════════════════════════════════════════════════════════════════════════
class Cell:
    """Represents one square on the Sudoku board."""

    def __init__(self, value: int, row: int, col: int, screen: pygame.Surface):
        self.value = value  # confirmed value (0 = empty)
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0  # pencilled-in guess
        self.selected = False
        # A cell is "fixed" (pre-generated) when it starts with a non-zero value
        self.fixed = (value != 0)

    # ── Setters ───────────────────────────────────────────────────────────────
    def set_cell_value(self, value: int):
        self.value = value

    def set_sketched_value(self, value: int):
        self.sketched_value = value

    # ── Drawing ───────────────────────────────────────────────────────────────
    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        # Background
        bg = (240, 240, 255) if self.selected else WHITE
        pygame.draw.rect(self.screen, bg, (x, y, CELL_SIZE, CELL_SIZE))

        # Selection border
        border_colour = RED if self.selected else LIGHT_GREY
        border_width = 2 if self.selected else LINE_THIN
        pygame.draw.rect(self.screen, border_colour,
                         (x, y, CELL_SIZE, CELL_SIZE), border_width)

        font_big = pygame.font.SysFont("comicsans", 36, bold=True)
        font_small = pygame.font.SysFont("comicsans", 20)

        if self.value != 0:
            colour = DARK_GREY if self.fixed else BLUE
            text = font_big.render(str(self.value), True, colour)
            tw, th = text.get_size()
            self.screen.blit(text,
                             (x + (CELL_SIZE - tw) // 2,
                              y + (CELL_SIZE - th) // 2))
        elif self.sketched_value != 0:
            text = font_small.render(str(self.sketched_value), True, PENCIL)
            self.screen.blit(text, (x + 4, y + 4))


# ══════════════════════════════════════════════════════════════════════════════
# Board
# ══════════════════════════════════════════════════════════════════════════════
class Board:
    """Represents the full 9×9 Sudoku board."""

    def __init__(self, width: int, height: int,
                 screen: pygame.Surface, difficulty: int,
                 board_data: list[list[int]], solution: list[list[int]]):
        """
        Parameters
        ----------
        width, height  : window dimensions
        screen         : pygame Surface
        difficulty     : number of removed cells (30 / 40 / 50)
        board_data     : 9×9 list of ints (0 = empty)
        solution       : 9×9 solved board
        """
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.solution = solution

        # Build Cell objects from board_data
        self.cells: list[list[Cell]] = [
            [Cell(board_data[r][c], r, c, screen) for c in range(BOARD_SIZE)]
            for r in range(BOARD_SIZE)
        ]
        # Keep original state for reset
        self.original: list[list[int]] = [row[:] for row in board_data]

        self.selected_cell: Cell | None = None

    # ── Drawing ───────────────────────────────────────────────────────────────
    def draw(self):
        self.screen.fill(WHITE, (0, 0, BOARD_PX, BOARD_PX))

        # Cells first
        for row in self.cells:
            for cell in row:
                cell.draw()

        # Grid lines on top
        for i in range(BOARD_SIZE + 1):
            width = LINE_THICK if i % 3 == 0 else LINE_THIN
            colour = BLACK if i % 3 == 0 else MID_GREY
            # horizontal
            pygame.draw.line(self.screen, colour,
                             (0, i * CELL_SIZE),
                             (BOARD_PX, i * CELL_SIZE), width)
            # vertical
            pygame.draw.line(self.screen, colour,
                             (i * CELL_SIZE, 0),
                             (i * CELL_SIZE, BOARD_PX), width)

    # ── Selection ─────────────────────────────────────────────────────────────
    def select(self, row: int, col: int):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x: int, y: int):
        """Return (row, col) if click is inside the board, else None."""
        if 0 <= x < BOARD_PX and 0 <= y < BOARD_PX:
            return y // CELL_SIZE, x // CELL_SIZE
        return None

    # ── Editing ───────────────────────────────────────────────────────────────
    def clear(self):
        """Remove sketched value (and confirmed value) of selected cell,
        but only if it was not a fixed/pre-generated cell."""
        cell = self.selected_cell
        if cell and not cell.fixed:
            cell.set_cell_value(0)
            cell.set_sketched_value(0)

    def sketch(self, value: int):
        """Pencil in a digit for the selected cell."""
        cell = self.selected_cell
        if cell and not cell.fixed:
            cell.set_sketched_value(value)

    def place_number(self, value: int):
        """Confirm the sketched value (called on Enter)."""
        cell = self.selected_cell
        if cell and not cell.fixed:
            cell.set_cell_value(value)
            cell.set_sketched_value(0)

    # ── Board state ───────────────────────────────────────────────────────────
    def reset_to_original(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = self.cells[r][c]
                cell.set_cell_value(self.original[r][c])
                cell.set_sketched_value(0)
                cell.fixed = (self.original[r][c] != 0)
        if self.selected_cell:
            self.selected_cell.selected = False
            self.selected_cell = None

    def is_full(self) -> bool:
        return all(self.cells[r][c].value != 0
                   for r in range(BOARD_SIZE)
                   for c in range(BOARD_SIZE))

    def update_board(self):
        """Sync cell values back into a 2-D list (used by check_board)."""
        self._current = [
            [self.cells[r][c].value for c in range(BOARD_SIZE)]
            for r in range(BOARD_SIZE)
        ]

    def find_empty(self):
        """Return (row, col) of the first empty cell, or None."""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.cells[r][c].value == 0:
                    return r, c
        return None

    def check_board(self) -> bool:
        """Return True if the board matches the solution exactly."""
        self.update_board()
        return self._current == self.solution
