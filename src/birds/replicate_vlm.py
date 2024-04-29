import replicate
import os
import utils
import PIL


MODEL = "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5"
LARGE_MODEL = "yorickvp/llava-v1.6-34b:41ecfbfb261e6c1adf3ad896c9066ca98346996d7c4045c5bc944a79d430f174"


PROMPT_PREFIX_LABEL = "Provide a one-sentence description of this image, using the followings RULES:\n"


EMBEDDING_CACHE = {}

def prompt_vlm_from_image(prompt, img, temp=0.6):
    img.save("tmp_img.jpg")
    with open("tmp_img.jpg", "rb") as the_image:
        input={
            "image": the_image,
            "top_p": 1,
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": temp
        }
        output = replicate.run(LARGE_MODEL, input)
    output_list = []
    for x in output:
        output_list.append(x)
    return " ".join(output_list)

def prompt_label(rules="", img="data/749.jpg"):
    prompt = PROMPT_PREFIX_LABEL+rules
    with open(img, "rb") as the_image:
        input={
            "image": the_image,
            "top_p": 1,
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.6
        }
        output = replicate.run(MODEL, input)
    output_list = []
    for x in output:
        output_list.append(x)
    print(output_list)
    return " ".join(output_list)

def get_baseline_dict():
    baseline_dict = {}
    for f in os.listdir(utils.DATA_DIR):
        img_id = int(f.split(".")[0])
        baseline_dict[img_id] = prompt_label(rules="", img=utils.DATA_DIR+f)
    return baseline_dict

def get_embeddings(img_file):
    if(img_file in EMBEDDING_CACHE.keys()):
        return EMBEDDING_CACHE[img_file]
    with open(img_file, "rb") as the_image:
        output = replicate.run(
        "krthr/clip-embeddings:1c0371070cb827ec3c7f2f28adcdde54b50dcd239aa6faea0bc98b174ef03fb4",
        input={
            "image": the_image
        })
    EMBEDDING_CACHE[img_file] = output["embedding"]
    return output["embedding"]


def generate_img(diffusion_model, prompt):
    output = replicate.run(
    diffusion_model,
    input={
        "width": 1024,
        "height": 1024,
        "prompt": prompt,
        "refine": "no_refiner",
        "scheduler": "K_EULER",
        "lora_scale": 0.6,
        "num_outputs": 1,
        "guidance_scale": 7.5,
        "apply_watermark": True,
        "high_noise_frac": 0.8,
        "negative_prompt": "",
        "prompt_strength": 0.8,
        "num_inference_steps": 10
    })
    return output

