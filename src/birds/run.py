import utils
import random
import json
import os
import time
import shutil
import replicate_vlm
import numpy as np
import img_utils
import finetune
import argparse
from urllib.request import urlretrieve
random.seed(42)
import pandas as pd
import scipy
STABILITY_MODEL = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
BUFFER = []

parser = argparse.ArgumentParser(description='Diffusion bottleneck.')
# Add arguments
parser.add_argument('--niters', type=int, default=2)
parser.add_argument('--run_name', type=str, default="run name")
parser.add_argument('--baseline_type', type=str, default="llava")
parser.add_argument('--contrast_type', type=str, default="species")


# Parse the arguments
args = parser.parse_args()
# diffusion model
if(args.baseline_type == "alt"):
    baseline_dict = utils.BASELINE_ALT_TEXT
else:
    baseline_dict = utils.BASELINE_LLAVA

def create_train_csv(train_ids, captions_dict, csv_dir):
    csv_dict = {"caption":[], "image_file":[]}
    for image_id in train_ids:
        csv_dict["image_file"].append(str(image_id)+".jpg")
        csv_dict["caption"].append(captions_dict[image_id].replace(",",""))
    df = pd.DataFrame(csv_dict)
    df.to_csv(csv_dir+'/caption.csv', index=False)
    

def get_splits():
    all_ids = sorted(list(utils.ATTRIBUTES.keys()))
    train = all_ids[:int(0.5*len(all_ids))]
    valid = all_ids[int(0.5*len(all_ids)):int(0.75*len(all_ids))]
    test = all_ids[int(0.75*len(all_ids)):]
    return train, valid, test

def create_train_folder(train_img_ids, current_label_dict, chain_i_train_dir):
    create_train_csv(train_img_ids, current_label_dict, chain_i_train_dir)
    for i in train_img_ids:
        shutil.copyfile(utils.DATA_DIR+str(i)+".jpg", chain_i_train_dir+"/"+str(i)+".jpg")


def get_reward(target_img_id, generated_img_file, contrast_type="color"):
    # target
    target_image_file = utils.DATA_DIR+str(target_img_id)+".jpg"
    target_img = np.array(replicate_vlm.get_embeddings(target_image_file))
    # generated
    generated_img = np.array(replicate_vlm.get_embeddings(generated_img_file))
    # contrast
    if(contrast_type == "color"):
        contrast_ids = utils.CONTRAST_SET_COLOR[target_img_id]
    if(contrast_type == "background"):
        contrast_ids = utils.CONTRAST_SET_BACKGROUND[target_img_id]
    if(contrast_type == "species"):
        contrast_ids = utils.CONTRAST_SET_SPECIES[target_img_id]
    contrast_image_files = [utils.DATA_DIR+str(ci)+".jpg" for ci in contrast_ids]
    contrast_imgs = [np.array(replicate_vlm.get_embeddings(cif)) for cif in contrast_image_files]
    generated_dist = np.linalg.norm(generated_img-target_img)
    contrast_dists = [np.linalg.norm(generated_img-ci) for ci in contrast_imgs]
    reward = np.mean(contrast_dists) - generated_dist
    print(generated_dist)
    print(contrast_dists)
    print(reward)
    print("\n")
    return reward

def get_rewards(generation_folder, eval_ids, caption_dict, contrast_type="color"):
    rewards_list = []
    for img_f in os.listdir(generation_folder):
        if(".png" in img_f or ".jpg" in img_f):
            img_id = int(img_f.split("_")[0])
            if(img_id in eval_ids):
                print(caption_dict[img_id])
                reward = get_reward(img_id, generation_folder+img_f, contrast_type)
                rewards_list.append((img_id, reward, caption_dict[img_id]))
    return rewards_list
    
    
    
    
def make_generations(diffusion_model, img_ids, caption_dict, dir_name):
    generations_dir = dir_name+"generations/"
    os.mkdir(generations_dir)
    for i in img_ids: 
        print(i)
        for n in range(1):
            prompt = caption_dict[i]
            print(prompt)
            output = replicate_vlm.generate_img(diffusion_model, prompt)
            urlretrieve(output[0], generations_dir+str(i)+"_"+str(n)+".png")
    return generations_dir
        
def get_samples(rewards):
    global BUFFER
    BUFFER = BUFFER+rewards
    sorted_rewards = sorted(BUFFER, key=lambda x:x[1])
    high_reward_samples = [x[0] for x in sorted_rewards[-3:]]
    high_reward_captions = [x[2] for x in sorted_rewards[-3:]]
    low_reward_samples = [x[0] for x in sorted_rewards[:3]]
    low_reward_captions = [x[2] for x in sorted_rewards[:3]]
    return high_reward_samples, low_reward_samples, high_reward_captions, low_reward_captions
    
def relabel_dict(label_dict, rules):
    print("RELABEL")
    new_label_dict = {}
    for k in label_dict.keys():
        img = utils.DATA_DIR+str(k)+".jpg"
        new_label_dict[k] = replicate_vlm.prompt_label(rules, img)
    return new_label_dict
    
def log_json(json_dict, fp):
    with open(fp, "a") as fp:
        json.dump(json_dict, fp)
        fp.write('\n')
        
def run(n_chains=2, 
        start_label_dict=utils.BASELINE_LLAVA, 
        do_finetune=False,
        contrast_type="species", 
        run_name="llava_species_"):
    run_id = str(int(time.time()))
    chain_dir = "chains/chain_"+run_id+"_"+run_name+"/"
    log_file = "logs/chain_"+run_id+"_"+run_name+".json"
    os.mkdir(chain_dir)
    current_label_dict = start_label_dict
    train, valid, test = get_splits()
    for chain_i in range(n_chains):
        chain_i_dir = chain_dir+str(chain_i)+"/"
        os.mkdir(chain_dir+str(chain_i)+"/")
        with open(chain_dir+'train_data_'+str(chain_i)+'.json', 'w') as fp:
            json.dump(current_label_dict, fp)
        # prepare images for training diffusion model
        if(do_finetune):
            chain_i_train_dir = chain_i_dir+"train"
            os.mkdir(chain_i_train_dir)
            create_train_folder(train, current_label_dict, chain_i_train_dir)
            # create train zip
            shutil.make_archive(chain_i_train_dir, 'zip', chain_i_train_dir)
            shutil.rmtree(chain_i_train_dir)
            #upload finetuning data
            serving_url = finetune.upload_data(chain_i_train_dir+".zip")
            training = finetune.train(serving_url)
            while(training.status != "succeeded"):
                training.reload()
            diffusion_model = training.output["version"]
        else:
            diffusion_model = STABILITY_MODEL
        generations_folder = make_generations(diffusion_model, valid+test, current_label_dict, chain_i_dir)
        valid_rewards =  get_rewards(generations_folder, valid, current_label_dict, contrast_type=contrast_type)
        test_rewards =  get_rewards(generations_folder, test, current_label_dict, contrast_type=contrast_type)
        log_json({"type":"reward", "step":chain_i, "mean":np.mean([x[1] for x in test_rewards])},log_file)
        high_reward_samples, low_reward_samples, high_reward_captions, low_reward_captions = get_samples(valid_rewards)
        bottleneck_rule = img_utils.get_rules(high_reward=high_reward_samples, low_reward=low_reward_samples, high_reward_captions=high_reward_captions, low_reward_captions=low_reward_captions)
        log_json({"type":"rule", "step":chain_i, "output":bottleneck_rule},log_file)
        current_label_dict = relabel_dict(current_label_dict, bottleneck_rule)


            
        
    
run(args.niters, 
    start_label_dict=baseline_dict, 
    run_name=args.run_name, 
    contrast_type=args.contrast_type,
    do_finetune=False)
