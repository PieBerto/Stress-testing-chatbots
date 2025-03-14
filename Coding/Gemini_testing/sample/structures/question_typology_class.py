from enum import Enum


class QuestionTypology(Enum):
    OS = "one-shot"
    COT = "chain of thought"
    POT = "programming of thought"