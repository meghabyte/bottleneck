import random
import pickle
import time
from collections import defaultdict
import copy 



INSTRUCTIONS_1 = ["<b>(Type A)</b> Draw a magenta dot at x=0.29, y=0.19. Draw three green triangles at x=0.2, y=0.74, x=0.23, y=0.72, and x=0.26, y=0.74. Draw a green triangle at x=0.25, y=0.87. Draw a magenta dot at x=0.21, y=0.27.",
                "<b>(Type A)</b> Draw six green triangles: two at (0.71, 0.69) and (0.26, 0.28), two at (0.75, 0.75) and (0.78, 0.77), and two at (0.87, 0.73) and (0.74, 0.73).",
                "<b>(Type A)</b> Draw six red dots at specified coordinates: (0.48, 0.21), (0.5, 0.29), (0.87, 0.58), (0.49, 0.28), (0.56, 0.17), and (0.51, 0.21).",
                "<b>(Type A)</b> Draw 4 blue squares, 1 at (0.71, 0.26), 1 at (0.79, 0.27), 1 at (0.65, 0.31), and 1 at (0.71, 0.22). Draw 2 magenta dots, 1 at (0.46, 0.81), 1 at (0.46, 0.69). Draw 1 blue square at (0.83, 0.24).",
                "<b>(Type A)</b> Draw a magenta triangle at (0.5, 0.27) and (0.42, 0.24), and four blue triangles at (0.83, 0.89), (0.75, 0.73), (0.74, 0.71), and (0.71, 0.79).",
                "<b>(Type B)</b> A collection of shapes in various shades of pink and purple, including two squares, three triangles, and four irregularly-shaped objects arranged around the center coordinates (x=0.25, y=0.77).",
                "<b>(Type B)</b> Four dots in various locations (x=0.84, y=0.76; x=0.8, y=0.75; x=0.67, y=0.78; x=0.74, y=0.71) with one square at x=0.35, y=0.21.",
                "<b>(Type B)</b> Three red shapes in the top left quadrant, including two triangles and a square. One triangle located at (0.2, 0.73), another at (0.27, 0.72), and a third at (0.31, 0.84). Additionally, there is a red square positioned at (0.24, 0.25) and two more triangles, one at (0.23, 0.68) and the other at (0.21, 0.73).",
                "<b>(Type B)</b> A red square at (0.46, 0.75) and multiple green dots at various locations, including (0.28, 0.25), (0.35, 0.25), (0.25, 0.22), (0.25, 0.22), (0.43, 0.73), (0.23, 0.23), and (0.22, 0.35).",
                "<b>(Type B)</b> Three red triangles located near the top edge of the image, with two triangles positioned left of center and one triangle positioned right of center. Additionally, there is a single red dot located towards the bottom left corner of the image."]

INSTRUCTIONS_2 = ["<b>(Type B)</b> A collection of shapes in various shades of pink and purple, including two squares, three triangles, and four irregularly-shaped objects arranged around the center coordinates (x=0.25, y=0.77).",
                "<b>(Type B)</b> Four dots in various locations (x=0.84, y=0.76; x=0.8, y=0.75; x=0.67, y=0.78; x=0.74, y=0.71) with one square at x=0.35, y=0.21.",
                "<b>(Type B)</b> Three red shapes in the top left quadrant, including two triangles and a square. One triangle located at (0.2, 0.73), another at (0.27, 0.72), and a third at (0.31, 0.84). Additionally, there is a red square positioned at (0.24, 0.25) and two more triangles, one at (0.23, 0.68) and the other at (0.21, 0.73).",
                "<b>(Type B)</b> A red square at (0.46, 0.75) and multiple green dots at various locations, including (0.28, 0.25), (0.35, 0.25), (0.25, 0.22), (0.25, 0.22), (0.43, 0.73), (0.23, 0.23), and (0.22, 0.35).",
                "<b>(Type B)</b> Three red triangles located near the top edge of the image, with two triangles positioned left of center and one triangle positioned right of center. Additionally, there is a single red dot located towards the bottom left corner of the image.",
                "<b>(Type A)</b> Draw a magenta dot at x=0.29, y=0.19. Draw three green triangles at x=0.2, y=0.74, x=0.23, y=0.72, and x=0.26, y=0.74. Draw a green triangle at x=0.25, y=0.87. Draw a magenta dot at x=0.21, y=0.27.",
                "<b>(Type A)</b> Draw six green triangles: two at (0.71, 0.69) and (0.26, 0.28), two at (0.75, 0.75) and (0.78, 0.77), and two at (0.87, 0.73) and (0.74, 0.73).",
                "<b>(Type A)</b> Draw six red dots at specified coordinates: (0.48, 0.21), (0.5, 0.29), (0.87, 0.58), (0.49, 0.28), (0.56, 0.17), and (0.51, 0.21).",
                "<b>(Type A)</b> Draw 4 blue squares, 1 at (0.71, 0.26), 1 at (0.79, 0.27), 1 at (0.65, 0.31), and 1 at (0.71, 0.22). Draw 2 magenta dots, 1 at (0.46, 0.81), 1 at (0.46, 0.69). Draw 1 blue square at (0.83, 0.24).",
                "<b>(Type A)</b> Draw a magenta triangle at (0.5, 0.27) and (0.42, 0.24), and four blue triangles at (0.83, 0.89), (0.75, 0.73), (0.74, 0.71), and (0.71, 0.79)."]

INSTRUCTIONS = [INSTRUCTIONS_1, INSTRUCTIONS_2]
class BuilderExperiment:
    def __init__(self, username):
        self.username = username
        self.colors = defaultdict(list)
        self.shapes = defaultdict(list)
        self.locations = defaultdict(list)
        self.times = defaultdict(list)
        self.instructions_choice = random.choice([0, 1])
        self.instructions_list = copy.deepcopy(INSTRUCTIONS[self.instructions_choice])
        #random.shuffle(self.instructions_list)
        self.counter = -1


    def add_steps(self, colors, shapes, positions):
        print("Add!")
        print((colors, shapes, positions))
        self.colors[self.counter] = colors
        self.shapes[self.counter] = shapes
        self.locations[self.counter] = positions
        self.times[self.counter].append(time.time())

          
    def get_next_instruction(self):
        self.counter += 1
        if(self.counter < len(self.instructions_list)):
            self.times[self.counter].append(time.time())
            return self.instructions_list[self.counter], self.counter
        else:
            return None, None
        
         
    def save(self):
        self.experiment_end = True
        save_fn = "logs/builder_data_"+self.username+"_"+time.strftime("%Y%m%d-%H%M%S")+".pkl"
        with open(save_fn, 'wb') as f:
            pickle.dump((self.instructions_choice, self.times, self.colors, self.shapes, self.locations, self.instructions_list), f)
        print("Saved!")
        print(save_fn)
        
        
    
    