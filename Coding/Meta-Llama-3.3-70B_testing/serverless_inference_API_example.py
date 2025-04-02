import requests

model_id = "meta-llama/Llama-3.2-3B-Instruct"#"meta-llama/Llama-3.1-405B-Instruct"#"meta-llama/Meta-Llama-3-8B-Instruct"

url = "https://api-inference.huggingface.co/models/"+model_id #https://huggingface.co/docs/api-inference/index#serverless-inference-api
rw_token = "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"

#huggingface-cli download meta-llama/Llama-3.3-70B-Instruct --include "original/*" --local-dir Llama-3.3-70B-Instruct

def req(query):
    parameters = {
        "max_new_tokens": 5000,
        "temperature": 0.01,
        "top_k": 50,
        "top_p": 0.95,
        "return_full_text": False
    }

    prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful and smart assistant. You accurately provide answer to the provided user query.<|eot_id|><|start_header_id|>user<|end_header_id|> Here is the query: ```{query}```.
      Provide precise and concise answer.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    headers = {
        'Authorization': f'Bearer {rw_token}',
        'Content-Type': 'application/json'
    }

    prompt = prompt.replace("{query}", query)

    payload = {
        "inputs": prompt,
        "parameters": parameters
    }

    response = requests.post(url, headers=headers, json=payload)
    response_text = response.json()

    return response_text#[0]['generated_text'].strip()

print(req('write a python program to generate fibonacci series'))