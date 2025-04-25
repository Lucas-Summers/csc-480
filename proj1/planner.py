import sys
import heapq
import itertools

class VacuumWorld:
    def __init__(self, fname):
        """
        Init the vacuum grid world by parsing the formatted file
        """
        self.actions = ['V', 'W', 'E', 'S', 'N']
        self.nrows = self.ncols = 0
        self.grid = []
        self.dirty = []  # positions of dirty cells
        self.start = None  # position of start cell

        with open(fname, 'r') as f:
            self.ncols = int(f.readline().strip())
            self.nrows = int(f.readline().strip())
            
            for r in range(self.nrows):
                line = list(f.readline().strip())
                self.grid.append(line)

                for c in range(self.ncols):
                    if line[c] == '@':
                        self.start = (r, c)
                    elif line[c] == '*':
                        self.dirty.append((r, c))
    
    def is_valid_cell(self, pos):
        """
        Returns true if the given position is in the grid and not blocked
        """
        return 0 <= pos[0] < self.nrows and \
                0 <= pos[1] < self.ncols and \
                self.grid[pos[0]][pos[1]] != '#'

    def is_clean(self, state):
        """
        Returns true if the given world state is clean (all dirty cells removed)
        """
        return len(state[1]) == 0
    
    def next_states(self, state):
        """
        Return the next possible states by taking all possible actions from the
        given state
        """
        pos, dirty_cells = state
        next_states = []

        for action in self.actions:
            if action == 'V':
                # if cell is dirty, clean it!
                if pos in dirty_cells:
                    new_dirty = frozenset(d for d in dirty_cells if d != pos)
                    next_states.append(((action, (pos, new_dirty)), 1))
                continue
            elif action == 'N':
                r_off, c_off = -1, 0
            elif action == 'S':
                r_off, c_off = 1, 0
            elif action == 'E':
                r_off, c_off = 0, 1
            elif action == 'W':
                r_off, c_off = 0, -1
            else:
                r_off, c_off = 0, 0 # not a supported action, do nothing

            new_pos = (pos[0] + r_off, pos[1] + c_off)
            if self.is_valid_cell(new_pos):
                next_states.append(((action, (new_pos, dirty_cells)), 1))
        
        return next_states
    

class VacuumBot:
    def __init__(self, world):
        """
        Init the vacuum bot in the given VacuumWorld
        """
        # using frozenset allows for hashing and comparisons for states
        self.start = (world.start, frozenset(world.dirty))
        self.world = world
        self.goal = None  # stores goal state found in a search
        self.parents = {}  # stores parent of states for path reconstruction
        
    def find_path(self):
        """
        Reconstruct the bots chosen path given the goal state and parent pointers
        """
        if not self.goal:
            return []

        path = []
        child = self.goal
        while child in self.parents and self.parents[child] is not None:
            parent, action = self.parents[child]
            path.append(action)
            child = parent
        return reversed(path)

    def run_ucs(self):
        """
        Run uniform-cost search for the bot in the world
        """
        gen = exp = id = 0
        id = itertools.count() # unique id for comparing if costs are equal
        costs = {self.start: 0}
        heap = []
        heapq.heappush(heap, (0, next(id), self.start))

        while heap:
            exp += 1
            
            cost, _, state = heapq.heappop(heap)
            if cost > costs[state]:
                continue
            
            for (action, next_state), move_cost in self.world.next_states(state):
                gen += 1

                if self.world.is_clean(next_state):
                    self.parents[next_state] = (state, action)
                    self.goal = next_state
                    return gen, exp
                
                new_cost = cost + move_cost
                if next_state not in costs or new_cost < costs[next_state]:
                    costs[next_state] = new_cost
                    heapq.heappush(heap, (new_cost, next(id), next_state))
                    self.parents[next_state] = (state, action)
        
        return gen, exp

    def run_dfs(self):
        """
        Run depth-first search for the bot in the world
        """
        gen = exp = 0
        visited = set()  # tracks visited states to avoid cycles
        stack = [self.start]

        while stack:
            exp += 1

            state = stack.pop()
            if state in visited:
                continue
            
            visited.add(state)
            for (action, next_state), _ in self.world.next_states(state):
                gen += 1
                
                if self.world.is_clean(next_state):
                    self.parents[next_state] = (state, action)
                    self.goal = next_state
                    return gen, exp
                
                if next_state not in visited and next_state not in self.parents:
                    stack.append(next_state)
                    self.parents[next_state] = (state, action)
        
        return gen, exp


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vacuum_planner.py [algorithm] [world_file]")
        sys.exit(1)
    
    try:
        world = VacuumWorld(sys.argv[2])
        vac = VacuumBot(world)
        
        if sys.argv[1] == "uniform-cost":
            gen, exp = vac.run_ucs()
        elif sys.argv[1] == "depth-first":
            gen, exp = vac.run_dfs()
        else:
            print("Algorithm must be 'depth-first' or 'uniform-cost'.")
            sys.exit(1)
        
        for action in vac.find_path():
            print(action)
        print(f"{gen} nodes generated")
        print(f"{exp} nodes expanded")

    except FileNotFoundError:
        print(f"File '{sys.argv[2]}' not found.")
        sys.exit(1)
