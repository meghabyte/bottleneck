import replicate
import requests
#REPLICATE_API_TOKEN = "PLACEHOLDER"


def train(serving_url, model_name="test"):
    training = replicate.trainings.create(version="stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={"input_images": serving_url, 
           "seed": 42, 
           "token_string":"bird",
           "checkpointing_steps":5000,
           "max_train_steps":1000},
    destination="meghabyte/"+model_name,)
    return training

def upload_data(data_zip):
    # First command
    response = requests.post("https://dreambooth-api-experimental.replicate.com/v1/upload/data.zip", headers={"Authorization": "Token " + REPLICATE_API_TOKEN})

    # Second command
    upload_url = response.json()["upload_url"]
    with open(data_zip, "rb") as file:
        requests.put(upload_url, headers={"Content-Type": "application/zip"}, data=file)

    # Third command
    serving_url = response.json()["serving_url"]
    return serving_url