from PIL.ImageFile import ImageFile

from src.LLMs.Gemini.request import launch_request as gemini_launch_request
from src.LLMs.models_details import gemini_models, serveless_huggingface_models, ollama_models
from src.LLMs.ollama.request import launch_request as ollama_launch_request, ollama_create
from src.LLMs.serverless_llama.request import launch_request as llama_launch_request
from src.counter_thread import CounterThread
from src.logging_thread import LoggerInteracter
from src.structures.question_typology_class import QuestionTypology


def process_main(api_key: str, q_name: str, account: str, msg_list: list[tuple[list[str | list[ImageFile, str]], QuestionTypology]], iteration: int,
                 model: str, logger: LoggerInteracter):

    counter_t =  CounterThread(model, account)
    counter_t.start()
    my_model = "my_" + model
    ollama_create(model)

    for j in range(iteration):
        for msg_type_tuple in msg_list:
            file_path: str
            if msg_type_tuple[1] is QuestionTypology.OS:
                file_path = "src\\..\\..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "one_shot.txt"
            elif msg_type_tuple[1] is QuestionTypology.COT:
                file_path = "src\\..\\..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "CoT.txt"
            elif msg_type_tuple[1] is QuestionTypology.POT:
                file_path = "src\\..\\..\\response\\" + model + "\\" + account + "\\" + q_name + "\\" + "PoT.txt"
            else:
                raise ValueError("Error in QuestionTypology enum while looking for the type")
            # one-shots require about 0.6 sec per request => 8
            # Chain of Thoughts require about 5.2 sec => 1
            # Programming of Thoughts require about 1.9 sec => 3
            if model in gemini_models:
                gemini_launch_request(msg_type_tuple[1], account, file_path, msg_type_tuple[0], model, logger, counter_t, api_key)
            elif model in serveless_huggingface_models:
                llama_launch_request(msg_type_tuple[1], account, file_path, msg_type_tuple[0], model, logger, counter_t, api_key)
            elif model.replace("_",":") in ollama_models:
                ollama_launch_request(msg_type_tuple[1],account,file_path,msg_type_tuple[0],model.replace("_",":"),logger,counter_t, my_model)
            else:
                raise ValueError("Can't find the specified model")

        print("In " + account + ", repetition: " + str(j), flush=True)
    print(account + " done", flush=True)

    logger.terminate()

    counter_t.join()