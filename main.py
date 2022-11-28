# Elk Island Database

"""
Title: Elk Island Populations
Author: Parth Sakpal
Date-Create: 2022-11-25
"""

import pathlib
import sqlite3



ELK_ISLAND_FILE = "Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv"

CONNECTION = sqlite3.connect(ELK_ISLAND_FILE)
CURSOR = CONNECTION.cursor()

FIRST_RUN = True

if (pathlib.Path.cwd() / ELK_ISLAND_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(ELK_ISLAND_FILE)
CURSOR = CONNECTION.cursor()

## INPUTS

LIST = [1, "species", "coordinate", 2006, 100]

### PROCESSING

def getData(FILENAME):
    """
    Gets the data from the file
    :param FILENAME: str
    :return: list -> str
    """

    FILE = open(FILENAME)
    TEXT_LIST = FILE.readlines()
    FILE.close()

    for i in range(5):
        if TEXT_LIST[i][-1] == "\n":
            TEXT_LIST[i] = TEXT_LIST[i][:-1]
        TEXT_LIST[i] = TEXT_LIST[i].split(",")
        for j in range(len(TEXT_LIST[i])):
            if TEXT_LIST[i][j] == "":
                TEXT_LIST[i][j] = "None"
            if TEXT_LIST[i][j].isnumeric():
                TEXT_LIST[i][j] = int(TEXT_LIST[i][j])
        print(TEXT_LIST[i])

def Database(LIST):
    """
    Creates the database
    :param LIST: list
    :return: none
    """

    global CURSOR, CONNECTION

    CURSOR.execute("""
            CREATE TABLE
                elk_island (
                    id INTEGER PRIMARY KEY,
                    species TEXT NOT NULL,
                    coordinate TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    population INTEGER NOT NULL
                )
        ;""")

    CURSOR.execute("""
        INSERT INTO
            elk_island
        VALUES (
            ?,?,?,?
        )
    
    ;""", LIST)

    CONNECTION.commit()

### OUTPUTS


if __name__ == "__main__":

    ### INPUTS

        getData(ELK_ISLAND_FILE)
        Database(LIST)



    ### PROCESSING

    ### OUTPUTS

