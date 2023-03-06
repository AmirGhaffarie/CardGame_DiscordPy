from utilities.constants import *
import pandas as pd

dictionary = {}


def get_text(label, language):
    if language in dictionary and label in dictionary[language]:
        return (dictionary[language])[label]
    return ""


def has_language(language):
    return language in dictionary


async def load():
    excel_data_frame = pd.read_excel(LOCALIZATION_FILE_ADDRESS, index_col=0)
    for col in excel_data_frame.columns:
        diclet = excel_data_frame[col].to_dict()
        dictionary[col] = diclet
