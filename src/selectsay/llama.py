import together
import requests
API_KEY = "YOURAPIKEY"
MODEL = "togethercomputer/llama-2-70b-chat"
SYSTEM_PROMPT = "Be a helpful assistant"



def prompt_model(prompt, max_tokens=500, temp=0.5):
    for i in range(20):
        print(i)
        full_prompt = "[INST] <<SYS>>\n"+SYSTEM_PROMPT+"\n\n"+prompt+" [/INST]"
        prompt_json={"model":MODEL, "prompt":full_prompt, "stop": ['[/INST]', '</s>'], "top_p":0.7, "top_k":50, "temperature":temp, "max_tokens":max_tokens} 
        endpoint = 'https://api.together.xyz/inference'
        try:
            res = requests.post(endpoint, json=prompt_json, headers={"Authorization":"Bearer "+API_KEY}, timeout=4)
        except:
            continue
        if(res.json()):
            response_text = res.json()["output"]["choices"][0]['text']
            print(response_text)
            return response_text
    return None
