import argparse
import os

from API_testing.main import main

#TODO: 1- catch SIGNINT (ctrl + c) e chiudere i processi gracefully.
#TODO: 2- un programma che avvii tutte le richieste, per tutti i modelli selezionando la domanda

# python .\gemini_testing.py -q 106 -r 1 -m gemini-2.0-flash-001 -k C:\Users\pietr\Desktop\Gemini_API_key.txt


def command_line_args():
    file_name = "..\\questions\\"
    opt_image_path: str | None = None
    parser = argparse.ArgumentParser(
        description="This program submit multiple times the question written in the specified file to Gemini and save "
                    "the results in the 'response' folder.",
        epilog="An example: python geminy_testing.py -q 101 -r 101")
    parser.add_argument("-q", "--question", required=True, type=int,
                        help="The question number: if the question is in the file named 'Question101', this parameter "
                             "should be 101.")
    parser.add_argument("-m", "--model", required=True, type=str,
                        choices=["gemini-2.0-flash-001", "gemini-2.0-flash-lite-001", "gemini-1.5-flash-002",
                                 "gemini-1.5-flash-8b-001", "gemini-2.0-flash-thinking-exp"],
                        help="The Gemini model to be used.")
    parser.add_argument("-r", "--repetitions", required=False, type=int,
                        help="The number of time the question will be submitted to Gemini, default: 100.", default=100)
    parser.add_argument("-k", "--api_key_file", required=True, type=str,
                        help="The path to the file containing the API key.")
    args = parser.parse_args()
    if 100 <= args.question < 200:
        img_path = file_name + "typology1\\img" + str(args.question) + ".png"
        file_name = file_name + "typology1\\Question" + str(args.question) + ".txt"
    elif 200 <= args.question < 300:
        img_path = file_name + "typology2\\img" + str(args.question) + ".png"
        file_name = file_name + "typology2\\Question" + str(args.question) + ".txt"
    elif 300 <= args.question < 400:
        img_path = file_name + "typology1\\img" + str(args.question) + ".png"
        file_name = file_name + "typology3\\Question" + str(args.question) + ".txt"
    else:
        raise ValueError("Error, Wrong parameters: The question number must be between 100 and 399")
    if not os.path.isfile(file_name):
        raise ValueError("Error, Question File '" + file_name + "' does not exist")
    if os.path.isfile(img_path):
        opt_image_path = img_path
    file = open(file_name, "r")
    if not os.path.isfile(args.api_key_file):
        raise ValueError("Error, API_key File '" + args.api_key_file + "' does not exist")
    # Retrieving the api_keys from the file
    api_key_file = open(args.api_key_file, "r")
    account_api_key = list()
    for line in api_key_file:
        if not line.startswith("#"):
            account_api_key.append(line.replace("\"", "").strip())
    print("Number of api_keys: " + str(len(account_api_key)), flush=True)
    return file_name, file, opt_image_path, account_api_key, args.repetitions, args.model


if __name__ == '__main__':
    (file_name, file, opt_image_path, account_api_key, repetitions, model) = command_line_args()
    main(file_name, file, opt_image_path, account_api_key, repetitions, model)
