model_to_limits = {
    "gemini-2.0-flash-001": (15,1500),
    "gemini-2.0-flash-lite-001": (30,1500),
    "gemini-1.5-flash-002": (15,1500),
    "gemini-1.5-flash-8b-001": (15,1500),
}

model_images = {
    "gemini-2.0-flash-001": True,
    "gemini-2.0-flash-lite-001": True,
    "gemini-1.5-flash-002": True,
    "gemini-1.5-flash-8b-001": True,
    "Meta-Llama-3-8B-Instruct": True,
    "llama3.1:8b": False,
    "llama3.2:3b": False,
    "llama3.2:1b": False,
    "gemma3:1b": True,
    "gemma3:4b": True
}

gemini_models = ["gemini-2.0-flash-001", "gemini-2.0-flash-lite-001", "gemini-1.5-flash-002",
                                 "gemini-1.5-flash-8b-001"]

serveless_huggingface_models = []#["Meta-Llama-3-8B-Instruct"]
#Forse serve specificare il tipo di immagine richiesta PIL.Image (?)

ollama_models = ["llama3.1:8b","llama3.2:3b","llama3.2:1b","gemma3:1b","gemma3:4b"]
