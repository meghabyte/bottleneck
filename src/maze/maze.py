import pygame
import numpy as np
from collections import defaultdict
import pygame
import time
import numpy as np
import argparse
import json

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 100  # Size of the cell
WALL_THICKNESS = 6  # Thickness of the wall
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (105, 173, 255)
RED = (255, 102, 102)
AGENT_SIZE = CELL_SIZE // 2  # Size of the agent
AGENT_COLOR = BLACK  # Green color for the agent
GOAL_COLOR = (0, 255, 0)
GREY = (200, 200, 200)


# Unseen maze used in experiments -- when test flag is False
maze_array_unseen = np.array([[2, 2, 1, 1, 1, 1, 2],
       [2, 2, 2, 1, 2, 8, 2],
       [2, 1, 2, 8, 1, 8, 1],
       [4, 4, 2, 8, 4, 4, 8],
       [8, 2, 1, 8, 8, 2, 1],
       [8, 4, 4, 2, 8, 1, 8],
       [8, 1, 1, 4, 4, 4, 8]], dtype=int)

color_dict_unseen = defaultdict(None, {0: defaultdict(None, {0: 0}),
                                1: defaultdict(None, {0: 0}),
                                2: defaultdict(None, {0: 0}),
                                3: defaultdict(None, {0:1, 1: 1, 2:0}),
                                4: defaultdict(None, {2:2, 1: 0}),
                                5: defaultdict(None, {1:1, 2:0 , 3: 0}),
                                6: defaultdict(None, {3:1, 4:0, 5:1})})

# Seen maze that language and visual stimuli were based on -- when test flag is True
maze_array_seen = np.array([[2, 2, 1, 2, 4, 2, 1],
       [2, 4, 8, 4, 8, 4, 2],
       [4, 4, 8, 8, 2, 2, 1],
       [8, 4, 4, 8, 2, 2, 8],
       [8, 1, 1, 8, 1, 4, 2],
       [2, 4, 8, 4, 8, 2, 1],
       [4, 8, 1, 1, 1, 1, 8]])

color_dict_seen = defaultdict(None, {0: defaultdict(None, {0: 0}),
                                1: defaultdict(None, {0: 0}),
                                2: defaultdict(None, {0: 0}),
                                3: defaultdict(None, {0:0}),
                                4: defaultdict(None, {0:1, 1:1, 2:0}),
                                5: defaultdict(None, {2:2, 1:0, 5:1, 6:0}),
                                6: defaultdict(None, {1:0, 2:1, 3:1, 4:0, 5:0})})


number2dir = {8: 'left', 4:'bottom', 2:'right', 1:'top'}


def cell_has_top_wall(pos, maze_array, maze_shape):
    if pos[1] == 0:
        return True
    else:
        pos_above = pos.copy()
        pos_above[1] -= 1
    if number2dir[maze_array[tuple(pos)]] != 'top' and number2dir[maze_array[tuple(pos_above)]] != 'bottom':
        return True
    else:
        return False


def cell_has_bottom_wall(pos, maze_array, maze_shape):
    if pos[1] == maze_shape[1] - 1:
        return True
    else:
        pos_below = pos.copy()
        pos_below[1] += 1
    if number2dir[maze_array[tuple(pos)]] != 'bottom' and number2dir[maze_array[tuple(pos_below)]] !=  'top':
        return True
    else:
        return False

def cell_has_left_wall(pos, maze_array, maze_shape):
    if pos[0] == 0:
        return True
    else:
        pos_left = pos.copy()
        pos_left[0] -= 1
    if number2dir[maze_array[tuple(pos)]] !=  'left' and number2dir[maze_array[tuple(pos_left)]] !=  'right':
        return True
    else:
        return False

def cell_has_right_wall(pos, maze_array, maze_shape):
    if pos[0] == maze_shape[0] - 1:
        return True
    else:
        pos_right = pos.copy()
        pos_right[0] += 1
    if number2dir[maze_array[tuple(pos)]] !=  'right' and number2dir[maze_array[tuple(pos_right)]] !=  'left':
        return True
    else:
        return False

class MazeGame:
    def __init__(self, maze_array, color_dict, with_colors, n_episodes=5, max_steps=200, hide_unvisited=True):
        self.maze_array = maze_array
        self.color_dict = color_dict
        self.n_episodes = n_episodes
        self.max_steps = max_steps
        self.hide_unvisited = hide_unvisited
        self.maze_shape = self.maze_array.shape
        self.colors_array = []
        for row in range(self.maze_shape[0]):
            self.colors_array.append([])
            for col in range(self.maze_shape[1]):
                try:
                    self.colors_array[-1].append(color_dict[row][col])
                except:
                    self.colors_array[-1].append(0)
        self.with_colors = with_colors
        # Window size
        north_south = self.maze_shape[1] * CELL_SIZE
        west_east = self.maze_shape[0] * CELL_SIZE
        self.screen = pygame.display.set_mode((west_east, north_south))
        self.agent_init = np.array((0, 0))
        self.agent_pos = None
        self.goal_pos = (self.maze_shape[0] - 1, self.maze_shape[1] - 1)

    def reset(self):
        self.agent_pos = self.agent_init.copy()  # reset agent pos
        self.visited_cells = {tuple(self.agent_init) : set()}  # reset visited cells + movements attempted
        self.update()

    def update(self):
        self.screen.fill(WHITE)  # Clear the screen
        self.draw_maze()
        self.draw_agent()
        pygame.display.flip()  # Update the display

    def draw_agent(self):
        # add agent
        agent_rect = pygame.Rect(self.agent_pos[0] * CELL_SIZE + (CELL_SIZE - AGENT_SIZE) // 2, self.agent_pos[1] * CELL_SIZE + (CELL_SIZE - AGENT_SIZE) // 2,
                                 AGENT_SIZE, AGENT_SIZE)
        pygame.draw.rect(self.screen, AGENT_COLOR, agent_rect)


    def wall_has_been_seen(self, pos, loc):
        if loc == 'top':
            if pos[1] == 0:
                return True
            above_cell = (pos[0], pos[1] - 1)
            if (pos in self.visited_cells.keys() and 'top' in self.visited_cells[pos]) or (above_cell in self.visited_cells.keys() and 'bottom' in self.visited_cells[above_cell]):
                return True
            else:
                return False
        elif loc == 'bottom':
            if pos[1] == self.maze_shape[1] - 1:
                return True
            below_cell = (pos[0], pos[1] + 1)
            if (pos in self.visited_cells.keys() and 'bottom' in self.visited_cells[pos]) or (below_cell in self.visited_cells.keys() and 'top' in self.visited_cells[below_cell]):
                return True
            else:
                return False
        elif loc == 'right':
            if pos[0] == self.maze_shape[0] - 1:
                return True
            right_cell = (pos[0] + 1, pos[1])
            if (pos in self.visited_cells.keys() and 'right' in self.visited_cells[pos]) or (right_cell in self.visited_cells.keys() and 'left' in self.visited_cells[right_cell]):
                return True
            else:
                return False
        elif loc == 'left':
            if pos[0] == 0:
                return True
            left_cell = (pos[0] - 1, pos[1])
            if (pos in self.visited_cells.keys() and 'left' in self.visited_cells[pos]) or (left_cell in self.visited_cells.keys() and 'right' in self.visited_cells[left_cell]):
                return True
            else:
                return False
        else: raise NotImplementedError
    def draw_maze(self):
        # draw goal
        pygame.draw.rect(self.screen, GOAL_COLOR, (self.goal_pos[0] * CELL_SIZE,  self.goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if self.hide_unvisited:
            for west_east in range(self.maze_shape[0]):
                for north_south in range(self.maze_shape[1]):
                    pos = np.array([west_east, north_south])
                    if tuple(pos) not in self.visited_cells:
                        pygame.draw.rect(self.screen, GREY, (west_east * CELL_SIZE ,
                                                             north_south * CELL_SIZE ,
                                                             CELL_SIZE ,
                                                             CELL_SIZE))

        for west_east in range(self.maze_shape[0]):
            for north_south in range(self.maze_shape[1]):
                pos = np.array([west_east, north_south])


                if not self.hide_unvisited or tuple(pos) in self.visited_cells:
                    if self.with_colors:
                        # add color code
                        if self.colors_array[west_east][north_south] == 1:
                            pygame.draw.rect(self.screen, RED, (west_east * CELL_SIZE, north_south * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        elif self.colors_array[west_east][north_south] == 2:
                            pygame.draw.rect(self.screen, BLUE, (west_east * CELL_SIZE, north_south * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    # Top wall
                    if cell_has_top_wall(pos, self.maze_array, self.maze_shape) and self.wall_has_been_seen(tuple(pos), 'top'):
                        pygame.draw.rect(self.screen, BLACK, (west_east * CELL_SIZE, north_south * CELL_SIZE - WALL_THICKNESS // 2, CELL_SIZE, WALL_THICKNESS))
                        # bottom
                    if cell_has_bottom_wall(pos, self.maze_array, self.maze_shape)  and self.wall_has_been_seen(tuple(pos), 'bottom'):
                        pygame.draw.rect(self.screen, BLACK, (west_east * CELL_SIZE, (north_south + 1) * CELL_SIZE - WALL_THICKNESS // 2, CELL_SIZE, WALL_THICKNESS))
                    # Left wall
                    if cell_has_left_wall(pos, self.maze_array, self.maze_shape)  and self.wall_has_been_seen(tuple(pos), 'left'):
                        pygame.draw.rect(self.screen, BLACK, (west_east * CELL_SIZE - WALL_THICKNESS // 2, north_south * CELL_SIZE, WALL_THICKNESS, CELL_SIZE))
                    # right
                    if cell_has_right_wall(pos, self.maze_array, self.maze_shape)  and self.wall_has_been_seen(tuple(pos), 'right'):
                        pygame.draw.rect(self.screen, BLACK, ((west_east+1) * CELL_SIZE - WALL_THICKNESS // 2, north_south * CELL_SIZE, WALL_THICKNESS, CELL_SIZE))


    def loop(self):
        n_steps = []
        successes = []
        times = []
        for i_ep in range(self.n_episodes):
            print(f'Playing episode {i_ep+1}')
            self.reset()
            steps, success, runtime = self.run()
            print(f'  > {"Success!" if success else "Failed."} (in {steps} steps).')
            n_steps.append(steps)
            successes.append(success)
            times.append(runtime)

        print(f"{np.sum(np.array(successes))}/{len(successes)} successes, avg n_steps = {np.mean(np.array(n_steps))}")
        pygame.quit()
        return n_steps, successes, times

    def update_visited_cell(self, pos, mov=None):
        if pos not in self.visited_cells.keys():
            self.visited_cells[pos] = set()
        if mov is not None:
            self.visited_cells[pos].add(mov)

    def run(self):
        running = True
        n_steps = 0
        success = False
        start_time = time.time()
        while running:
            moved = False
            update = False
            if n_steps > self.max_steps:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        n_steps += 1
                        if(n_steps == 1):
                            start_time = time.time() # set start time at first step
                        update = True
                        if event.key == pygame.K_LEFT:
                            self.update_visited_cell(tuple(self.agent_pos), 'left')
                            if self.agent_pos[0] > 0 and not cell_has_left_wall(self.agent_pos, self.maze_array, self.maze_shape):
                                self.agent_pos[0] -= 1  # Move left
                                moved = True
                        elif event.key == pygame.K_RIGHT:
                            self.update_visited_cell(tuple(self.agent_pos), 'right')
                            if self.agent_pos[0] < self.maze_shape[0] - 1 and not cell_has_right_wall(self.agent_pos, self.maze_array, self.maze_shape):
                                self.agent_pos[0] += 1  # Move right
                                moved = True
                        elif event.key == pygame.K_UP:
                            self.update_visited_cell(tuple(self.agent_pos), 'top')
                            if self.agent_pos[1] > 0 and not cell_has_top_wall(self.agent_pos, self.maze_array, self.maze_shape):
                                self.agent_pos[1] -= 1  # Move up
                                moved = True
                        elif event.key == pygame.K_DOWN:
                            self.update_visited_cell(tuple(self.agent_pos), 'bottom')
                            if self.agent_pos[1] < self.maze_shape[1] - 1 and not cell_has_bottom_wall(self.agent_pos, self.maze_array, self.maze_shape):
                                self.agent_pos[1] += 1  # Move down
                                moved = True

                    if moved:
                        self.update_visited_cell(tuple(self.agent_pos))
                        if tuple(self.agent_pos) == tuple(self.goal_pos):
                            success = True
                            running = False
                    if update:
                        self.update()
        end_time = time.time()
        total_time = end_time-start_time
        time.sleep(3)
        return n_steps, success, total_time



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Maze user study")
    parser.add_argument("--name", default="test", help="First number", required=False)
    parser.add_argument("--test", default="false", help="test", required=False)
    parser.add_argument("--case", default="A", help="Case", required=True)
    args = parser.parse_args()
    if(args.test == "true"):
        maze_array = maze_array_seen
        color_dict = color_dict_seen
    elif(args.test == "false"):
        maze_array = maze_array_unseen
        color_dict = color_dict_unseen
    maze = MazeGame(maze_array, color_dict, with_colors=True, n_episodes=1, max_steps=200, hide_unvisited=True)
    n_steps, successes, times =  maze.loop()
    with open("logs/"+args.name+"_"+str(int(time.time()))+"_"+args.case+"_"+args.test+".json", "w") as f:
        json.dump({"n_steps":n_steps, "successes":successes, "times":times}, f)