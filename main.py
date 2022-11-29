# Elk Island Database

"""
Title: Elk Island Populations
Author: Parth Sakpal
Date-Create: 2022-11-25
"""

import pathlib
import sqlite3



ELK_ISLAND_RAW_DATA = "Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv"

DATABASE_FILE = "elk_island.db"

FIRST_RUN = True

if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

## INPUTS



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

    for i in range(len(TEXT_LIST)):
        if TEXT_LIST[i][-1] == "\n":
            TEXT_LIST[i] = TEXT_LIST[i][:-1]
        TEXT_LIST[i] = TEXT_LIST[i].split(",")
        for j in range(len(TEXT_LIST[i])):
            if TEXT_LIST[i][j] == "":
                TEXT_LIST[i][j] = "None"
            if TEXT_LIST[i][j].isnumeric():
                TEXT_LIST[i][j] = int(TEXT_LIST[i][j])

    return TEXT_LIST




def Database(LIST):
    """
    Creates the database
    :param LIST: list
    :return: none
    """
    global CURSOR, CONNECTION

    CURSOR.execute("""
        CREATE TABLE
            data (
                coordinate TEXT,
                year INT,
                animal TEXT,
                population INT
            )
    
    ;""")

    for i in range(len(LIST)):
        CURSOR.execute("""
            INSERT INTO
                data 
            VALUES (
                ?, ?, ?, ?
            )
        
        ;""", LIST[i][:4])

    CONNECTION.commit()

### OUTPUTS


if __name__ == "__main__":

    ### INPUTS

    MY_LIST = []

    LIST = getData(ELK_ISLAND_RAW_DATA)



    if FIRST_RUN:

        LIST = getData(ELK_ISLAND_RAW_DATA)

        for i in range(len(LIST)):
            MY_LIST.append(LIST[0])
            MY_LIST.append(LIST[1])
            MY_LIST.append(LIST[5])
            MY_LIST.append(LIST[16])
            MY_LIST[i] = MY_LIST[i].split(",")

        print(MY_LIST)


        Database(LIST)

    else:
        print("This is not the first run")

        for i in range(len(LIST)):
            MY_LIST.append([])
            for j in range(1):
                MY_LIST[i].append(LIST[i][0])
                MY_LIST[i].append(LIST[i][1])
                MY_LIST[i].append(LIST[i][5])
                MY_LIST[i].append(LIST[i][16])

        del MY_LIST[0]
        print(MY_LIST)




    ### PROCESSING

    ### OUTPUTS

