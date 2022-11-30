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
                TEXT_LIST[i][j] = "NULL"
            if TEXT_LIST[i][j] =='NA':
                TEXT_LIST[i][j] = "NULL"
            if TEXT_LIST[i][j].isnumeric():
                TEXT_LIST[i][j] = int(TEXT_LIST[i][j])

    return(TEXT_LIST)




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
                population_year INTEGER,
                survey_year INTEGER,
                survey_month TEXT,
                survey_day TEXT,
                species_name TEXT,
                unknown_age TEXT,
                adult_male_count INTEGER,
                adult_female_count INTEGER,
                adult_unknown_count INTEGER,
                yearling_count INTEGER,
                calf_count INTEGER,
                survey_total INTEGER,
                sightability_correction_factor TEXT,
                additional_captive_count INTEGER,
                animals_removed_prior_to_survey INTEGER,
                fall_population_estimate INTEGER,
                survey_comment TEXT,
                estimate_method TEXT
                
            )
    
    ;""")

    for i in range(1, len(LIST)):
        CURSOR.execute("""
            INSERT INTO
                data 
            VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )

        ;""", LIST[i][:19])


    CONNECTION.commit()

def addData():
    """
    Adds data to the database
    :return:
    """

    global CURSOR, CONNECTION

    USER_DATA = []

    USER_DATA.append(input("North or South?: "))
    USER_DATA.append(input("What year?: "))
    USER_DATA.append(input("What animal?: "))
    USER_DATA.append(input("What is the population?: "))

    CURSOR.execute("""
        INSERT INTO
            data (
                coordinate,
                population_year,
                species_name,
                fall_population_estimate
            )
        VALUES (
            ?, ?, ?, ?
        )
    ;""", USER_DATA)



    CONNECTION.commit()

### OUTPUTS


if __name__ == "__main__":

    ### INPUTS

    MY_LIST = []

    LIST = getData(ELK_ISLAND_RAW_DATA)



    if FIRST_RUN:

        LIST = getData(ELK_ISLAND_RAW_DATA)

        print(LIST)

        Database(LIST) # Creates the database

        print("Database created")



    else:
        print("This is not the first run")
        addData()  # adds data







    ### PROCESSING

    ### OUTPUTS

