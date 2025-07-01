Folder Structure:
in the root folder can be found
- the last version of the thesis
- Slideshow folder in which is present a slide presentation of the thesis
- Coding folder in which can be found the used programs, the submitted questions and the raw results
- Results folder containing the .ods files with the final Plot Boxes and the final data used
[More info can be found in the README of the subfolder]

Workflow:
1- Executing the python program inside "./Coding/LLMs_tesing" can be launched multiple remote request to different models of Gemini with different accounts. Local requests to Ollama can, even, be performed but only with a single account. The speed of local LLMs using Ollama depends strongly to the VRAM and Graphics chipset.
This program asks to the selected LLM the questions inside "./Coding/questions", where are separated by typology and save the resulted raw data inside "./Coding/response", where the data is categorized by model, account and question.
2 - Executing the program in "./Coding/response_to_csv" the raw data can be transformed in csv files. This program takes the raw data from "./Coding/response" and executing the question specific function, that can be found in the file "./Coding/response/src/question_csv" and are named as the question file (e.x. def q101(...)), the corresponding csv files are produced and can be found in "./Coding/csv".
3 - The file named as the questions (e.x. q101.csv) in "./Coding/csv" must be opened, interpreted and saved as .odf in the folder "./Results", once this have been done the macroes inside "./Results/UsedMacroes" can be executed, these will import all the sub csv files of the question, produce the final data and the Plot Boxes.
