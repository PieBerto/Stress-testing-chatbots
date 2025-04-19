import argparse
import os

from src.LLMs.models_details import gemini_models, serveless_huggingface_models, ollama_models
from src.main import main


#TODO: 1- catch SIGNINT (ctrl + c) e chiudere i processi gracefully.
#TODO: 2- un programma che avvii tutte le richieste, per tutti i modelli selezionando la domanda

# python .\gemini_testing.py -q 106 -r 1 -m gemini-2.0-flash-001 -k C:\Users\pietr\Desktop\Gemini_API_key.txt


def command_line_args():
    file_name = "src\\..\\..\\questions\\"
    opt_image_path: str | None = None
    parser = argparse.ArgumentParser(
        description="This program submit multiple times the question written in the specified file to Gemini and save "
                    "the results in the 'response' folder.",
        epilog="An example: python geminy_testing.py -q 101 -r 101")
    parser.add_argument("-q", "--question", required=True, type=int,
                        help="The question number: if the question is in the file named 'Question101', this parameter "
                             "should be 101.")
    parser.add_argument("-m", "--model", required=True, type=str,
                        choices=[*gemini_models,*serveless_huggingface_models,*ollama_models],
                        help="The Gemini model to be used.")
    parser.add_argument("-r", "--repetitions", required=False, type=int,
                        help="The number of time the question will be submitted to Gemini, default: 100.", default=100)
    parser.add_argument("-k", "--api_key_file", required=True, type=str,
                        help="The path to the file containing the API key. If using Ollama is not required, any string can be used (e.x. placeholder)")
    args = parser.parse_args()
    question_typology = int(args.question/100)
    img_path = file_name + "typology"+str(question_typology)+"\\img" + str(args.question) + ".png"
    file_name = file_name + "typology"+str(question_typology)+"\\Question" + str(args.question) + ".txt"

    if not os.path.isfile(file_name):
        raise ValueError("Error, Question File '" + file_name + "' does not exist")
    if os.path.isfile(img_path):
        opt_image_path = img_path
    file = open(file_name, "r")
    account_api_key = list()
    if args.model in [*gemini_models,*serveless_huggingface_models]:
        if not os.path.isfile(args.api_key_file):
            raise ValueError("Error, API_key File '" + args.api_key_file + "' does not exist")
        # Retrieving the api_keys from the file
        api_key_file = open(args.api_key_file, "r")
        for line in api_key_file:
            if not line.startswith("#"):
                account_api_key.append(line.replace("\"", "").strip())
        print("Number of api_keys: " + str(len(account_api_key)), flush=True)
    elif args.model in [*ollama_models]:
        account_api_key.append("")
    else:
        raise ValueError("Error, Model '" + args.model + "' has not been recognized.")
    return file_name, file, opt_image_path, account_api_key, args.repetitions, args.model


if __name__ == '__main__':
    (_file_name, _file, _opt_image_path, _account_api_key, _repetitions, _model) = command_line_args()
    main(_file_name, _file, _opt_image_path, _account_api_key, _repetitions, _model.replace(":","_"))
