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

def menu():
    """
    Presents the menu to the user
    :return: int
    """

    print("""
    WELCOME TO ELK ISLAND CALCULATOR

    1. Search Population Growth
    2. Add to Database
    3. Exit
    """)

    USER_INPUT = input("Select your choice: ")
    USER_INPUT = checkInt(USER_INPUT)

    if 4 > USER_INPUT > 0:

        return USER_INPUT
    else:
        print("Select an option from the menu")
        return menu()


def checkInt(INPUT):
    """

    :return:
    """

    if INPUT.isnumeric():
        return int(INPUT)
    else:
        print("Please enter a valid number")
        NEW_INPUT = input("Enter the number again: ")
        checkInt(NEW_INPUT)


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
                TEXT_LIST[i][j] = "No data has been recorded"
            if TEXT_LIST[i][j] == 'NA':
                TEXT_LIST[i][j] = "No data has been recorded"
            if TEXT_LIST[i][j].isnumeric():
                TEXT_LIST[i][j] = int(TEXT_LIST[i][j])

    return (TEXT_LIST)


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
                survey_year,
                survey_month,
                survey_day,
                species_name TEXT,
                unknown_age,
                adult_male_count,
                adult_female_count,
                adult_unknown_count,
                yearling_count,
                calf_count,
                survey_total,
                sightability_correction_factor,
                additional_captive_count,
                animals_removed_prior_to_survey,
                fall_population_estimate INTEGER,
                survey_comment,
                estimate_method

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


def insertData(LIST):
    """
    Inserts new data into the list
    :param LIST: list
    :return: none
    """

    global CURSOR, CONNECTION

    CURSOR.execute(f"""
        INSERT INTO
            data (
                coordinate,
                population_year,
                survey_year,
                survey_month,
                survey_day,
                species_name,
                unknown_age,
                adult_male_count,
                adult_female_count,
                adult_unknown_count,
                yearling_count,
                calf_count,
                survey_total,
                sightability_correction_factor,
                additional_captive_count,
                animals_removed_prior_to_survey,
                fall_population_estimate,
                survey_comment,
                estimate_method
            )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? 
        )
    ;""", LIST)

    CONNECTION.commit()


def userData():
    """
    Adds data to the database
    :return:list
    """

    print("""
    Please enter the values for the following fields. 
    If you would not like to add any data in a specific field, leave it blank. 
    Do not leave the Area of park, population year, species name, and species population field blank. 
    """)

    USER_DATA = []

    USER_DATA.append(input("North or South?: "))
    USER_DATA.append(input("Population year?: "))
    USER_DATA.append(input("Survey Year?: "))
    USER_DATA.append(input("Survey Month?: "))
    USER_DATA.append(input("Survey Day?: "))
    USER_DATA.append(input("What animal?: "))
    USER_DATA.append(input("Unknown age and sex count: "))
    USER_DATA.append(input("Adult male count: "))
    USER_DATA.append(input("Adult female count: "))
    USER_DATA.append(input("Adult unknown count: "))
    USER_DATA.append(input("Yearling count: "))
    USER_DATA.append(input("Calf count: "))
    USER_DATA.append(input("Survey total: "))
    USER_DATA.append(input("Sightability correction factor"))
    USER_DATA.append(input("Additional captive count: "))
    USER_DATA.append(input("Animals removed prior to survey: "))
    USER_DATA.append(input("What is the population?: "))
    USER_DATA.append(input("Survey comment: "))
    USER_DATA.append(input("Estimate method: "))

    if USER_DATA[0] == "" or USER_DATA[1] == "" or USER_DATA[5] == "" or USER_DATA[16] == "":
        print("You have not entered all the required data")
        return userData()

    for i in range(len(USER_DATA)):
        if USER_DATA[i] == "":
            USER_DATA[i] = "No data has been recorded"

    print("Data has been successfully added to the database!")

    return USER_DATA



def populationGrowth(START_YEAR, END_YEAR, USER_ANIMAL):

    global CURSOR, CONNECTION

    if USER_ANIMAL == 1:
        ANIMAL = "Bison"
    if USER_ANIMAL == 2:
        ANIMAL = "Moose"
    if USER_ANIMAL == 3:
        ANIMAL = "Elk"
    if USER_ANIMAL == 4:
        ANIMAL = "Deer"

        POPULATION_1 = CURSOR.execute("""
            SELECT
                fall_population_estimate
            FROM
                data
            WHERE
                species_name= ?
            AND
                population_year = ?
        
        ;""", [ANIMAL, START_YEAR]).fetchall()

        TOTAL_POPULATION_1 = int(POPULATION_1[0]) + int(POPULATION_1[1])
        print(TOTAL_POPULATION_1)

### OUTPUTS


if __name__ == "__main__":

    ### INPUTS

    MY_LIST = []

    LIST = getData(ELK_ISLAND_RAW_DATA)

    if FIRST_RUN:

        LIST = getData(ELK_ISLAND_RAW_DATA)

        Database(LIST)  # Creates the database

        print("Database created")



    else:

        while True:

            # print("This is not the first run")
            CHOICE = menu()

            if CHOICE == 1:
                START_YEAR = input("Start year: ")
                END_YEAR = input("End year: ")
                USER_ANIMAL = int(input("Bison (1), Moose (2), Elk (3), Deer (4), All (5): "))

                populationGrowth(START_YEAR, END_YEAR, USER_ANIMAL)

            if CHOICE == 2:
                USER_DATA = userData()
                insertData(USER_DATA)

            if CHOICE == 3:
                exit()

        # USER_DATA = userData()  # takes data from user
        # insertData(USER_DATA)

    ### PROCESSING

    ### OUTPUTS
