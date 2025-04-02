model_to_limits = {
    "gemini-2.0-flash-001": (15,1500),
    "gemini-2.0-flash-lite-001": (30,1500),
    "gemini-1.5-flash-002": (15,1500),
    "gemini-1.5-flash-8b-001": (15,1500),
    "gemini-2.0-flash-thinking-exp": (10,1500)
}

model_images = {
    "gemini-2.0-flash-001": True,
    "gemini-2.0-flash-lite-001": True,
    "gemini-1.5-flash-002": True,
    "gemini-1.5-flash-8b-001": True,
    "gemini-2.0-flash-thinking-exp": True
}

gemini_models = ["gemini-2.0-flash-001", "gemini-2.0-flash-lite-001", "gemini-1.5-flash-002",
                                 "gemini-1.5-flash-8b-001", "gemini-2.0-flash-thinking-exp"]

#Forse serve specificare il tipo di immagine richiesta PIL.Image (?)