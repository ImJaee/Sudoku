import random

class SudokuGenerator:
    
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * row_length for _ in range(row_length)]
        self.solution = [[0] * row_length for _ in range(row_length)]
    
    def get_board(self):
        return self.board
    
    def get_solution(self):
        return self.solution
    
    def print_board(self):
        for i in range(self.row_length):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            for j in range(self.row_length):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.board[i][j], end=" ")
            print()
    
    def valid_in_row(self, row, num):
        return num not in self.board[row]
    
    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True
    
    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True
    
    def is_valid(self, row, col, num):
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        
        return (self.valid_in_row(row, num) and 
                self.valid_in_col(col, num) and 
                self.valid_in_box(box_row_start, box_col_start, num))
    
    def unused_in_box(self, row_start, col_start):
        used = set()
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] != 0:
                    used.add(self.board[row][col])
        
        unused = [num for num in range(1, 10) if num not in used]
        random.shuffle(unused)
        return unused
    
    def fill_box(self, row_start, col_start):
        unused = self.unused_in_box(row_start, col_start)
        num_index = 0
        
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == 0 and num_index < len(unused):
                    self.board[row][col] = unused[num_index]
                    num_index += 1
    
    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)
    
    def fill_remaining(self):
        for row in range(self.row_length):
            for col in range(self.row_length):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            
                            if self.fill_remaining():
                                return True
                            
                            self.board[row][col] = 0
                    
                    return False
        return True
    
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()
    
    def remove_cells(self):
        removed_count = 0
        removed_cells = set()
        
        while removed_count < self.removed_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            cell = (row, col)
            if cell not in removed_cells:
                removed_cells.add(cell)
                self.board[row][col] = 0
                removed_count += 1
    
    def generate_sudoku(self):
        self.fill_values()
        self.solution = [row[:] for row in self.board]
        self.remove_cells()


def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    generator.generate_sudoku()
    return generator
