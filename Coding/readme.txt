- "question" folder -> contains the question submitted to the LLMs dived per category. 
HOW TO FORMAT THE QUESTION FILES:
	- the file name must be QuestionXXX.txt.
	- Each question start with "%OS" or "%COT" or "%POT", the methodology that the program must use.
	- Questions are dived by "%%%".
	-  Multiple iteration in the same chat with the LLMs are needed for "%COT" methodology and are separated by "%%".
	- The file must end with "%%%%"

- "LLMs_testing" folder contain the python program that perform the requests to the LLMs taking the questions from "question" folder and putting the result in "response" folder.

- "response" folder contains the raw responses of the LLMs divided per model, account, question, methodology.

- "response_to_csv" folder contains the Python program that elaborate the responses in "response", compairing them with the correct results and putting the final csv in "csv" folder.

- "csv" folder -> contains the csv files created by the "response_to_csv" python program.