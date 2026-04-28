class Environment:

    def __init__(self):
        self.steps = 10  # iteraciones
        self.project_board()
        self.agent = (4, 1)  # agent position (row, col) — starts at 'S'
        self.goal = (1, 7)   # goal position (row, col) — the 'E' cell
        self.carrying = None  # item the agent is physically holding (e.g. 'K')

    def project_board(self):
        self.board = [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', '#', ' ', 'E', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', 'K', '#', ' ', ' ', ' ', ' ', '#'],
            ['#', 'S', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', 'B', 'D', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        ]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _cell_is_passable(self, row, col):
        """Return True if the agent can move into (row, col)."""
        cell = self.board[row][col]
        if cell == '#':
            return False
        if cell == 'D':          # door blocks movement unless agent has the key
            return self.carrying == 'K'
        return True

    def is_done(self):
        """The episode ends when the agent reaches the goal or runs out of steps."""
        return self.agent == self.goal or self.steps <= 0

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    
    DIRECTIONS = {
        'up':    (-1,  0),
        'down':  ( 1,  0),
        'left':  ( 0, -1),
        'right': ( 0,  1),
    }

    def get_possible_actions(self, state=None):
        """Return the list of valid action strings from the current (or given) state."""
        if state is None:
            state = self.agent

        actions = []
        for direction, (dr, dc) in self.DIRECTIONS.items():
            nr, nc = state[0] + dr, state[1] + dc
            if 0 <= nr < len(self.board) and 0 <= nc < len(self.board[0]):
                if self._cell_is_passable(nr, nc):
                    actions.append(direction)

        # Recoger objetos (Llave = 'K' ; Bola = 'B')
        cell = self.board[state[0]][state[1]]
        if cell in ('K', 'B') and self.carrying is None:
            actions.append('pickup')

        # El agente puede soltar lo que lleva (solo en casillas vacías)
        if self.carrying is not None and cell == ' ':
            actions.append('drop')

        return actions


    def do_action(self, action):

        reward = -1         
        row, col = self.agent

        if action in self.DIRECTIONS:
            # Sumar la posicion actual con la cardinalidad destino
            dr, dc = self.DIRECTIONS[action]
            nr, nc = row + dr, col + dc

            if not (0 <= nr < len(self.board) and 0 <= nc < len(self.board[0])):
                return self.agent, reward, self.is_done()

            cell = self.board[nr][nc]

            if cell == '#':
                reward -= 5
                return self.agent, reward, self.is_done()

            if cell == 'D':
                if self.carrying != 'K':
                    reward -= 5
                    return self.agent, reward, self.is_done()
                # Usar llave para la puerta
                self.carrying = None
                self.board[nr][nc] = ' '
                reward += 50

            if self.board[row][col] == 'S':
                self.board[row][col] = ' '
            self.agent = (nr, nc)

            if self.agent == self.goal:
                reward += 100

        # recoger objeto 
        elif action == 'pickup':
            cell = self.board[row][col]
            if cell == 'K':
                reward += 30
                self.carrying = cell
                self.board[row][col] = ' '
            elif cell == 'B':
                reward += 10
                self.carrying = cell
                self.board[row][col] = ' '
            

        # soltar objeto 
        elif action == 'drop':
            if self.carrying is not None and self.board[row][col] == ' ':
                reward += 20
                self.board[row][col] = self.carrying
                self.carrying = None

        self.steps -= 1
        done = self.is_done()
        return self.agent, reward, done

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def render(self):
        
        for r, row in enumerate(self.board):
            line = ''
            for c, cell in enumerate(row):
                if (r, c) == self.agent:
                    line += 'A '
                else:
                    line += cell + ' '
            print(line)
        print(f"Steps left: {self.steps}  |  Carrying: {self.carrying or 'nothing'}")
        print()