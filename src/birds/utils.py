import os
import random
random.seed(42)
import numpy as np
import pickle

DATA_DIR = "data/"

CLASSES = {14: "Indigo_Bunting", 
           17:"Cardinal",
           29:"American_Crow",
           59:"California_Gull",
           73:"Blue_Jay",
           77:"Tropical_Kingbird",
           20:"Yellow_breasted_Chat",
           101:"White_Pelican",
           42:"Vermilion_Flycatcher",
           106:"Horned_Puffin"}

ATTRIBUTES = {749:["blue", "tree", "Indigo_Bunting"],
              754:["blue", "tree", "Indigo_Bunting"],
              756:["blue", "tree", "Indigo_Bunting"],
              758:["blue", "tree", "Indigo_Bunting"],
              766:["blue", "tree", "Indigo_Bunting"],
              899:["red", "snow", "Cardinal"],
              900:["red", "snow", "Cardinal"],
              908:["red", "tree", "Cardinal"],
              912:["red", "snow", "Cardinal"],
              920:["red", "tree", "Cardinal"],
              1074:["yellow", "sky", "Yellow_breasted_Chat"],
              1078:["yellow", "tree", "Yellow_breasted_Chat"],
              1094:["yellow", "sky", "Yellow_breasted_Chat"],
              1105:["yellow", "tree", "Yellow_breasted_Chat"],
              1112:["yellow", "sky", "Yellow_breasted_Chat"],
              1584:["black", "tree", "American_Crow"],
              1600:["black", "sky", "American_Crow"],
              1601:["black", "sky", "American_Crow"],
              1608:["black", "tree", "American_Crow"],
              1610:["black", "sky", "American_Crow"],
              2356:["red", "tree", "Vermilion_Flycatcher"],
              2375:["red", "tree", "Vermilion_Flycatcher"],
              2381:["red", "sky", "Vermilion_Flycatcher"],
              2385:["red", "tree", "Vermilion_Flycatcher"],
              2399:["red", "sky", "Vermilion_Flycatcher"],
              3379:["white", "ocean", "California_Gull"],
              3393:["white", "ocean", "California_Gull"],
              3413:["white", "sky", "California_Gull"],
              3420:["white", "sky", "California_Gull"],
              3425:["white", "ocean", "California_Gull"],
              4198:["blue", "tree", "Blue_Jay"],
              4201:["blue", "tree", "Blue_Jay"],
              4219:["blue", "snow", "Blue_Jay"],
              4229:["blue", "tree", "Blue_Jay"],
              4231:["blue", "snow", "Blue_Jay"],
              4440:["yellow", "tree", "Tropical_Kingbird"],
              4453:["yellow", "sky", "Tropical_Kingbird"],
              4462:["yellow", "sky", "Tropical_Kingbird"],
              4471:["yellow", "tree", "Tropical_Kingbird"],
              4483:["yellow", "sky", "Tropical_Kingbird"],
              5868:["white", "ocean", "White_Pelican"],
              5874:["white", "ocean", "White_Pelican"],
              5876:["white", "sky", "White_Pelican"],
              5891:["white", "sky", "White_Pelican"],
              5903:["white", "ocean", "White_Pelican"],
              6146:["black", "ocean", "Horned_Puffin"],
              6150:["black", "tree", "Horned_Puffin"],
              6165:["black", "ocean", "Horned_Puffin"],
              6172:["black", "ocean", "Horned_Puffin"],
              6187:["black", "tree", "Horned_Puffin"]}


CONTRAST_SET_COLOR = {749: [2375, 1584, 4471], 754: [2375, 1584, 4471], 756: [2375, 1584, 4471], 758: [1584, 4471, 3413], 766: [1584, 4471, 3413], 899: [758, 766, 1584], 900: [758, 766, 1584], 908: [758, 766, 1584], 912: [758, 766, 1584], 920: [
758, 766, 1584], 1074: [6187, 766, 1584], 1078: [2356, 766, 1584], 1094: [766, 1584, 4219], 1105: [758, 766, 1584], 1112: [1600, 1601, 1608], 1584: [766, 4219, 4471], 1600: [1112, 2356, 2375], 1601: [2356, 2375, 2385], 1608:
 [1112, 2356, 2375], 1610: [1112, 2381, 2385], 2356: [766, 1584, 4219], 2375: [766, 1584, 4219], 2381: [1601, 766, 1112], 2385: [1601, 766, 1584], 2399: [4198, 1601, 1112], 3379: [2356, 6187, 766], 3393: [6187, 766, 1584], 3413: [766, 1584, 4219], 3420: [766, 1584, 4219], 3425: [6146, 6165, 1600], 4198: [2375, 1094, 1584], 4201: [2375
, 1584, 4471], 4219: [1584, 4471, 3413], 4229: [1584, 4471, 2356], 4231: [1584, 4471, 3413], 4440: [2375, 766, 1584], 4453: [766, 1584, 4219], 4462: [766, 1584, 4219], 4471: [766, 1584, 4219], 4483: [2375, 766, 1584], 5868: 
[6187, 766, 1584], 5874: [766, 1584, 4219], 5876: [6187, 766, 1584], 5891: [6187, 766, 1584], 5903: [766, 1584, 4219], 6146: [3379, 3425, 3393], 6150: [766, 4219, 4471], 6165: [3379, 5876, 2356], 6172: [766, 4219, 4471], 6187: [766, 3413, 4219]} 

CONTRAST_SET_BACKGROUND = {749: [4219, 3413, 3420], 754: [4219, 3413, 3420], 756: [4219, 3420, 3413], 758: [4219, 3413, 3420], 766: [4219, 3413, 3420], 899: [920, 758, 2356], 900: [758, 2375, 2381], 908: [912, 900, 899], 912: [920, 758, 2375], 920: [
4219, 3413, 912], 1074: [1105, 4440, 6187], 1078: [1112, 4462, 1094], 1094: [766, 1584, 4219], 1105: [4462, 1074, 1094], 1112: [1078, 1608, 1105], 1584: [4219, 3413, 3420], 1600: [1608, 6165, 2356], 1601: [1608, 2356, 2375], 1608: [1600, 1610, 1601], 1610: [1608, 2385, 6165], 2356: [4219, 3413, 3420], 2375: [4219, 3413, 3420], 2381: [
2385, 900, 912], 2385: [2381, 1601, 4219], 2399: [2385, 900, 912], 3379: [5876, 5891, 3413], 3393: [5876, 3413, 6187], 3413: [766, 1584, 4219], 3420: [766, 1584, 4219], 3425: [5876, 5891, 3420], 4198: [1094, 4219, 1601], 4201: [4219, 3413, 3420], 4219: [766, 1584, 4471], 4229: [4219, 3413, 3420], 4231: [758, 766, 1584], 4440: [4462, 1094, 4219], 4453: [766, 1584, 4219], 4462: [4440, 766, 1584], 4471: [4219, 3413, 3420], 4483: [1078, 1105, 2375], 5868: [3413, 5891, 6187], 5874: [5876, 3420, 766], 5876: [6187, 766, 1584], 5891: [5868, 6187, 766], 5903: [5876, 3420, 766], 6146: [1600, 1601, 1608], 6150: [4219, 3413, 3420], 6165: [6187, 1600, 5876], 6172: [766, 1584, 4219], 6187: [3413, 4219, 3420]}

CONTRAST_SET_SPECIES = {749: [4201, 2375, 1584], 754: [2375, 1584, 4219], 756: [2375, 4201, 1584], 758: [1584, 4219, 4471], 766: [1584,4219, 4471], 899: [758, 2356, 2385], 900: [758, 2375, 2381], 908: [2381, 2385, 2399], 912: [758, 2375, 2381], 920: [758, 766, 1584], 1074: [4462, 4440, 6187], 1078: [4462, 2356, 766], 1094: [766, 1584, 4219], 1105: [4440, 4462, 758], 1112: [4462, 1600, 4483], 1584: [766, 4219, 4471], 1600: [1112, 6165, 2356], 1601: [2356, 2375, 2385], 1608: [1112, 6165, 2356], 1610: [1112, 2381, 2385], 2356: [766, 1584, 4219], 2375: [766, 1584, 4219], 2381: [900, 912, 1601], 2385: [1601, 766, 1584], 2399: [900, 912, 899], 3379: [5876, 5891, 2356], 3393: [5876, 5868, 6187], 3413: [766, 1584, 4219], 3420: [766, 1584, 4219], 3425: [5903, 6146, 5874], 4198: [2375, 766, 1094], 4201: [754, 749, 2375], 4219: [766, 1584, 4471], 4229: [758, 766, 1584], 4231: [758, 766, 1584], 4440: [1094, 1105, 2375], 4453: [766, 1584, 4219], 4462: [766, 1584, 4219], 4471: [766, 1584, 4219], 4483: [1078, 1112, 1105], 5868: [3413, 6187, 766], 5874: [3420, 766, 1584], 5876: [3413, 6187, 766], 5891: [3413, 6187, 766], 5903: [3420, 766, 1584], 6146: [3379, 1600, 3425], 6150: [766, 1584, 4219], 6165: [1600, 3379, 5876], 6172: [766, 1584, 4219], 6187: [766, 1584, 3413]}


BASELINE_ALT_TEXT = {749:"A blue bird perched on a branch",
            754:"A blue bird on a branch",
            756:"A blue bird perched on a branch",
            758:"A blue bird sitting on a branch",
            766:"A blue bird on a branch",
            899:"A red bird sitting on a branch in the snow",
            900:"A red bird sitting in the snow",
            908:"A red bird with a beak open",
            912:"A red bird standing in the snow",
            920:"A red bird standing in grass",
            1074:"A bird on a branch",
            1078:"A bird perched on a branch",
            1094:"A bird on a branch",
            1105:"A bird perched on a branch",
            1112:"A bird on a wire",
            1584:"A black bird standing on a pile of peanuts",
            1600:"A bird on a wire",
            1601:"A crow perched on a post",
            1608:"A black bird on a branch",
            1610:"A black bird on a branch",
            2356:"A red and black bird perched on a barbed wire",
            2375:"A bird perched on a branch",
            2381:"A bird sitting on a branch",
            2385:"A bird on a branch",
            2399:"A bird sitting on a wire",
            3379:"A close-up of a seagull",
            3393:"A seagull standing on a pole",
            3413:"A bird flying in the sky",
            3420:"A bird flying in the sky",
            3425:"A seagull standing on a rock near the ocean",
            4198:"A bird on a tree branch",
            4201:"A blue bird sitting on a fence",
            4219:"A bird sitting on a branch",
            4229:"A bird on a branch",
            4231:"A blue jay sitting on a fence",
            4440:"A bird perched on a branch",
            4453:"A bird on a wire",
            4462:"A bird perched on a wire",
            4471:"A bird sitting on a branch",
            4483:"A bird perched on a branch",
            5868:"A white bird with a long beak floating on water",
            5874:"A white bird with a long beak swimming in water",
            5876:"A white bird flying in the sky",
            5891:"A bird flying in the sky",
            5903:"A white bird with a long beak swimming in water",
            6146:"A puffin swimming in the water",
            6150:"A puffin sitting on a rock",
            6165:"A bird flying over the water",
            6172:"A bird swimming in water",
            6187:"A bird with its beak open"}

BASELINE_LLAVA = {5868: 'A  white  pelican  bird  is  swimming  in  the  water.', 908: 'A  red  cardinal  bird  is  sitting  on  a  black  object.', 749: 'A  blue  bird  with  a  yellow  beak  sits  on  a  tree  branch.', 1074: 'A  small  yellow  and  grey  bird  with  yellow  eyes  and  a  black  beak  stands  on  a  tree  branch.', 1584: 'A  black  bird  is  standing  on  a  pile  of  peanuts.', 756: 'A  blue  bird  sits  on  a  branch  in  the  sunlight.', 899: 'A  red  cardinal  in  the  snow.', 3420: 'A  bird  is  flying  through  the  sky  in  front  of  a  blue  sky.', 758: 'A  blue  bird  sits  on  a  thin  branch.', 4462: 'A  small  bird  perched  on  a  wire  against  a  blue  sky.', 900: 'a  red  bird  sits  in  the  snow.', 4440: 'A  small  yellow  and  white  bird  with  a  blueish  gray  head  sitting  on  a  branch.', 2385: 'A  small  red  and  black  bird  perched  on  a  branch.', 5903: 'A  pelican  is  floating  in  the  water.', 4229: 'A  blue  bird  perched  on  a  tree  branch.', 5876: 'The  bird  is  flying  in  the  sky  and  has  a  yellow  beak.', 3413: 'A  seagull  flying  in  the  air.', 4231: 'A  blue  jay  with  white  feathers  on  his  wings  and  tail  is  perched  on  a  wooden  railing.', 766: 'A  blue  bird  is  sitting  on  a  thin  branch.', 920: 'A  red  cardinal  is  standing  in  the  grass.', 1600: 'A  black  bird  perched  on  a  power  line.', 4483: 'A  small  bird  perched  on  a  tree  branch.', 3425: 'A  seagull  is  standing  on  a  rock  in  the  ocean.', 754: 'a  blue  bird  sitting  on  a  tree  branch.', 2399: 'A  red  bird  sits  on  a  wire,  looking  straight  ahead.', 6146: 'A  bird  with  a  yellow  beak  and  black  and  white  coloring  is  swimming  in  the  ocean.', 5891: 'A  pelican  is  flying  in  the  sky  with  its  wings  out.', 912: 'A  red  cardinal  in  the  snow  with  a  tree  branch  behind  him.', 1078: 'A  yellow  bird  with  a  black  head  sits  on  a  branch.', 6150: 'A  bird  is  looking  at  the  ground.', 2381: 'A  bird  with  red  on  its  face,  perched  on  a  thin  branch.', 3393: 'A  bird  is  standing  on  a  wooden  post.', 4471: 'A  colorful  bird  with  a  yellow  chest  and  black  legs  sits  on  a  tree  branch.', 1112: 'A  small,  yellow  bird  is  perched  on  a  wire.', 6165: 'A  seagull  is  flying  over  the  water.', 3379: 'A  bird  is  standing  on  a  red  pole  next  to  the  water.', 4453: 'A  small  bird  perched  on  a  wire.', 4201: 'A  blue  jay  is  perched  on  a  fence.', 2375: 'A  red  bird  sits  on  a  branch.', 1601: 'A  large  black  crow  is  sitting  on  a  wooden  post.', 1608: 'A  bird  perches  on  a  tree  branch.', 6172: 'A  black  and  white  bird  with  a  yellow  beak  is  swimming  in  the  water.', 5874: 'A  large  white  bird  with  a  long  orange  beak  floating  in  the  ocean.', 1105: 'A  yellow  bird  with  a  black  eye  is  sitting  on  a  branch  of  a  tree.', 1094: 'A  yellow  and  black  bird  with  a  yellow  and  black  beak  sitting  on  a  tree  branch.', 4198: 'A  bird  perched  on  a  branch  of  a  tree.', 1610: 'A  bird  is  perched  on  a  branch  with  a  piece  of  grass  in  its  mouth.', 2356: 'A  red  bird  is  perched  on  a  barbed  wire  fence.', 4219: 'A  blue  bird  with  a  black  face  stands  on  a  snow  covered  branch.', 6187: 'A  bird  perched  on  a  rock  with  its  beak  open.'}

