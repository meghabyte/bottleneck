import sys
from PIL import Image
import replicate_vlm
import utils

DATA_DIR = "data/"

def concat_images(image_ids):
    images = [Image.open(DATA_DIR+str(x)+".jpg") for x in image_ids]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    return new_im

def enumerate_list(l):
    counter = 1
    list_text = ""
    for li in l:
        list_text+=str(counter)+". "+li+"\n"
        counter += 1
    return list_text

def get_rules(high_reward_captions, low_reward_captions, high_reward=[766, 2356, 5876], 
             low_reward=[4453, 6165, 1074]):
    high_reward_imgs = concat_images(high_reward)
    low_reward_imgs = concat_images(low_reward)
    high_reward_captions = enumerate_list(high_reward_captions)
    low_reward_captions = enumerate_list(low_reward_captions)
    full_im = Image.new('RGB', (max([high_reward_imgs.size[0], low_reward_imgs.size[0]]),
                                high_reward_imgs.size[1]+low_reward_imgs.size[1]))
    full_im.paste(high_reward_imgs, (0, 0))
    full_im.paste(low_reward_imgs, (0, high_reward_imgs.size[1]))
    rules_prompt = "The top row of three images have the following HIGH REWARD descriptions:\n"+high_reward_captions+"The bottom row of three images have the following LOW REWARD descriptions:\n"+low_reward_captions+"Provide a set of two rules I should follow in order to provide image descriptions with HIGH REWARD, NOT LOW REWARD. Provide the rules after the prefix RULES:"
    print(rules_prompt)
    print(high_reward)
    print(low_reward)
    output = replicate_vlm.prompt_vlm_from_image(rules_prompt,
                          full_im, 0.05)
    rules = output.split("RULES:")[-1].strip()
    print(rules)
    return rules
    
#get_rules(all_captions=utils.BASELINE_ALT_TEXT)
#get_rules(all_captions=utils.BASELINE_LLAVA)