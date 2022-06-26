from random import shuffle

DEMO = False
PCT_VALID = 0.75

WIDTH = 7
HEIGHT = 5
SPACING = 100

PLAYER = 0
TILE = 1
BROKEN_TILE = 2
ROCK = 3

tile_type_to_art = [
    '🥷 ',
    '🟦',
    '🌀',
    '🪨 '
]


def render(board, win=False, art_size=2):
    image = ' ' * art_size * (len(board[0]) // 2) + '🐉'
    if win:
        image += '\n' + ' ' * art_size * (len(board[0]) // 2) + '||'
    else:
        image += '\n'
    for row in board:
        image += '\n'
        for col in row:
            image += tile_type_to_art[col]
    return image


def draw(board, win=False, spacing=True):
    print('\n' * (SPACING if spacing else 0) + render(board, win=win))


def is_valid_coords(board, coords):
    row, col = coords
    return row >= 0 and row < len(board) \
        and col >= 0 and col < len(board[0])


def is_valid_move(board, coords):
    row, col = coords
    if not is_valid_coords(board, coords):
        return False
    if board[row][col] != TILE:
        return False
    return True


def neighbors(coords):
    row, col = coords
    return [
        (row-1, col),
        (row, col-1),
        (row+1, col),
        (row, col+1)
    ]


def size(board):
    return len(board) * len(board[0])


def randomized(l):
    copy = list(l)
    shuffle(copy)
    return copy


def generate_game(board, start, end, pct_valid=0.75):
    def is_candidate(coords):
        row, col = coords
        return row >= 0 and row < len(board) \
            and col >= 0 and col < len(board[0]) \
            and board[row][col] == BROKEN_TILE

    def backtrack(tile, end, depth):

        if tile == end and depth > int(size(board)*pct_valid):
            return depth

        for candidate in [c for c in randomized(neighbors(tile)) if is_candidate(c)]:
            r, c = candidate
            board[r][c] = TILE  # fix(candidate)

            found_depth = backtrack(candidate, end, depth+1)
            if found_depth:
                return found_depth

            board[r][c] = BROKEN_TILE  # unfix(candidate)

    board[start[0]][start[1]] = TILE
    num_tiles_to_break = backtrack(start, end, 1)

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == BROKEN_TILE:
                board[i][j] = ROCK

    return num_tiles_to_break-1  # -1 because the end tile is not supposed to be broken


########
# game #
########

board = [[BROKEN_TILE for _ in range(WIDTH)] for _ in range(HEIGHT)]
curr_coords = (len(board)-1, len(board[0])//2)
end = (0, len(board[0])//2)

num_tiles_to_break = generate_game(
    board,
    curr_coords,
    end,
    PCT_VALID
)

board[curr_coords[0]][curr_coords[1]] = PLAYER

num_breaks = 0

win = False
lose = False

print(
    '\n' * SPACING
    + 'Make your move:'
    '\n    w'
    '\n  a 🕹  d'
    '\n     s'
    + '\n' * 3
)

draw(board, spacing=False)

while not (win or lose):

    inp = None
    while not inp:
        tmp = input().strip().lower()
        if tmp and tmp[-1] in 'wasd':
            inp = tmp[-1]

    new_coords = None

    if inp == 'w':
        new_coords = (curr_coords[0]-1, curr_coords[1])
    elif inp == 'a':
        new_coords = (curr_coords[0], curr_coords[1]-1)
    elif inp == 's':
        new_coords = (curr_coords[0]+1, curr_coords[1])
    elif inp == 'd':
        new_coords = (curr_coords[0], curr_coords[1]+1)

    if is_valid_move(board, new_coords):
        board[new_coords[0]][new_coords[1]] = PLAYER
        num_breaks += 1
        board[curr_coords[0]][curr_coords[1]] = BROKEN_TILE
        curr_coords = new_coords

    if curr_coords == end \
            and num_breaks == num_tiles_to_break:
        win = True
    elif len([n for n in neighbors(curr_coords) if is_valid_move(board, n)]) == 0:
        lose = True

    draw(board)

draw(board, win=win)

if win:
    print('\nYou won!')
else:
    print('\nYou lost...')
