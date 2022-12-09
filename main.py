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
    for i in range(15):
        LIST.append("No data has been recorded")

    global CURSOR, CONNECTION

    CURSOR.execute(f"""
        INSERT INTO
            data (
                coordinate,
                population_year,
                species_name,
                fall_population_estimate,
                survey_year,
                survey_month,
                survey_day,
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

    USER_DATA = []

    USER_DATA.append(input("North or South?: "))
    USER_DATA.append(input("What year?: "))
    USER_DATA.append(input("What animal?: "))
    USER_DATA.append(input("What is the population?: "))

    return USER_DATA


def populationGrowth(START_YEAR, END_YEAR, USER_ANIMAL):
    """
    Determines the population growth
    :param START_YEAR: INT
    :param END_YEAR: INT
    :param USER_ANIMAL: INT
    :return: None
    """

    global CURSOR

    START_YEAR = int(START_YEAR)
    END_YEAR = int(END_YEAR)

    if USER_ANIMAL == 1:
        ANIMAL = "Bison"
    if USER_ANIMAL == 2:
        ANIMAL = "Moose"
    if USER_ANIMAL == 3:
        ANIMAL = "Elk"
    if USER_ANIMAL == 4:
        ANIMAL = "Deer"


    START_YEAR_POPULATION = CURSOR.execute("""
        SELECT
            fall_population_estimate
        FROM
            data
        WHERE
            species_name = ? 
        AND
            population_year = ?
    ;""", [ANIMAL, START_YEAR]).fetchall()

    END_YEAR_POPULATION = CURSOR.execute("""
        SELECT
            fall_population_estimate
        FROM
            data
        WHERE
            species_name = ?
        AND
            population_year = ?
    ;""", [ANIMAL, END_YEAR]).fetchall()

    END_POPULATION = []
    START_POPULATION = []



    for i in range(len(START_YEAR_POPULATION)):
        START_YEAR_POPULATION[i] = list(START_YEAR_POPULATION[i])
        START_POPULATION.append(START_YEAR_POPULATION[i][0])

    for i in range(len(END_YEAR_POPULATION)):
        END_YEAR_POPULATION[i] = list(END_YEAR_POPULATION[i])
        END_POPULATION.append(END_YEAR_POPULATION[i][0])

    for i in range(2):
        END_POPULATION.append(0)
        START_POPULATION.append(0)

    for i in range(len(START_POPULATION)):
        if START_POPULATION[i] == "No data has been recorded":
            START_POPULATION[i] = 0

    for i in range(len(END_POPULATION)):
        if END_POPULATION[i] == "No data has been recorded":
            END_POPULATION[i] = 0

    TOTAL_START_YEAR = START_POPULATION[0] + START_POPULATION[1]
    TOTAL_END_YEAR = END_POPULATION[0] + END_POPULATION[1]

    print(TOTAL_START_YEAR)
    print(TOTAL_END_YEAR)

    #TOTAL_GROWTH = (TOTAL_END_YEAR - TOTAL_START_YEAR) / (END_YEAR - START_YEAR)

    #print(TOTAL_GROWTH)



    """


    for i in range(len(START_POPULATION)):
        if START_POPULATION[i][0] == "No data has been recorded":
            START_POPULATION[i][0] = 0

    for i in range(len(END_YEAR_POPULATION)):
        END_YEAR_POPULATION[i] = list(END_YEAR_POPULATION[i])
        if END_YEAR_POPULATION[i][0] == "No data has been recorded":
            END_YEAR_POPULATION[i][0] = 0

    for i in range(2):
        START_YEAR_POPULATION.append(0)
        END_YEAR_POPULATION.append(0)

   

   


    NORTH_POPULATI0N_1 = int(START_YEAR_POPULATION[0][0])
    SOUTH_POPULATION_1 = int(START_YEAR_POPULATION[1][0])

    NORTH_POPULATI0N_2 = int(END_YEAR_POPULATION[0][0])
    SOUTH_POPULATION_2 = int(END_YEAR_POPULATION[1][0])

    

    TOTAL_GROWTH = (TOTAL_END_YEAR - TOTAL_START_YEAR)/(END_YEAR - START_YEAR)

    print(TOTAL_GROWTH)

"""











def populationGrowthAll(START_YEAR, END_YEAR):


    global CURSOR



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

                if 5 > USER_ANIMAL > 0:
                    populationGrowth(START_YEAR, END_YEAR, USER_ANIMAL)
                if USER_ANIMAL == 5:
                    print("pass")

            if CHOICE == 2:
                USER_DATA = userData()
                insertData(USER_DATA)

            if CHOICE == 3:
                exit()

        # USER_DATA = userData()  # takes data from user
        # insertData(USER_DATA)

    ### PROCESSING

    ### OUTPUTS
