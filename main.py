# Elk Island Database

"""
Title: Elk Island Populations
Author: Parth Sakpal
Date-Create: 2022-11-25
"""

## Imports
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

def menu():
    """
    Presents the menu to the user
    :return: int
    """

    print("""
    WELCOME TO ELK ISLAND CALCULATOR.
    This program will allow you to determine the growth rate of animals from a specfic year. 

    1. Search Population Growth
    2. Add to Database
    3. View data of a specific animal during a certain year
    4. Exit
    """)

    USER_INPUT = input("Select your choice: ")
    if USER_INPUT.isnumeric() is False:
        print("Enter a number value.")
        return menu()

    USER_INPUT = int(USER_INPUT)

    if 5 > USER_INPUT > 0:
        return USER_INPUT
    else:
        print("Select an option from the menu")
        return menu()

def userAnimal():
    """
    Allows user to input the animal they want to calculate the growth rate for.
    :return: Int
    """

    USER_ANIMAL = int(input("Bison (1), Moose (2), Elk (3), Deer (4), All (5): "))

    if 0 > USER_ANIMAL or USER_ANIMAL > 5:
        print("Enter an option from the list provided.")
        return userAnimal()
    else:
        return USER_ANIMAL

## PROCESSING

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
                TEXT_LIST[i][j] = "NA"
            if TEXT_LIST[i][j] == 'NA':
                TEXT_LIST[i][j] = "NA"
            if TEXT_LIST[i][j].isnumeric():
                TEXT_LIST[i][j] = int(TEXT_LIST[i][j])

    return (TEXT_LIST)


def Database(LIST):
    """
    Creates the database
    :param LIST: list
    :return: None
    """
    global CURSOR, CONNECTION

    CURSOR.execute("""
        CREATE TABLE
            data (
                area_of_park TEXT,
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
    Inserts new data into the database.
    :param LIST: list
    :return: None
    """

    global CURSOR, CONNECTION

    CURSOR.execute(f"""
        INSERT INTO
            data (
                area_of_park,
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
    Allows user to input the values they want to add to the database
    :return:List
    """

    print("""
       Please enter the values for the following fields.
       If you would not like to add any data in a specific field, leave it blank.
       Do not leave the Area of park, population year, species name, and species population field blank.
       """)

    USER_DATA = []

    USER_DATA.append(input("Area of Park (North or South)?: "))
    USER_DATA.append(input("Population year?: "))
    USER_DATA.append(input("Survey Year?: "))
    USER_DATA.append(input("Survey Month?: "))
    USER_DATA.append(input("Survey Day?: "))
    USER_DATA.append(input("Species Name?: "))
    USER_DATA.append(input("Unknown age and sex count?: "))
    USER_DATA.append(input("Adult male count?: "))
    USER_DATA.append(input("Adult female count?: "))
    USER_DATA.append(input("Adult unknown count?: "))
    USER_DATA.append(input("Yearling count?: "))
    USER_DATA.append(input("Calf count?: "))
    USER_DATA.append(input("Survey total?: "))
    USER_DATA.append(input("Sightability correction factor?: "))
    USER_DATA.append(input("Additional captive count?: "))
    USER_DATA.append(input("Animals removed prior to survey?: "))
    USER_DATA.append(input("What is the population?: "))
    USER_DATA.append(input("Survey comment?: "))
    USER_DATA.append(input("Estimate method?: "))

    if USER_DATA[0] == "" or USER_DATA[1] == "" or USER_DATA[5] == "" or USER_DATA[16] == "":
        print("You have not entered all the required data")
        return userData()

    for i in range(len(USER_DATA)):
        if USER_DATA[i] == "":
            USER_DATA[i] = "NA"

    print("Data has been successfully added to the database!")

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
        if START_POPULATION[i] == "NA":
            START_POPULATION[i] = 0

    for i in range(len(END_POPULATION)):
        if END_POPULATION[i] == "NA":
            END_POPULATION[i] = 0

    TOTAL_START_YEAR = START_POPULATION[0] + START_POPULATION[1]
    TOTAL_END_YEAR = END_POPULATION[0] + END_POPULATION[1]

    TOTAL_GROWTH = (TOTAL_END_YEAR - TOTAL_START_YEAR) / (END_YEAR - START_YEAR)
    TOTAL_GROWTH = round(TOTAL_GROWTH)

    print(f"The total growth of {ANIMAL} from {START_YEAR} to {END_YEAR} is {TOTAL_GROWTH} {ANIMAL}/year.")

def allPopulationGrowth(START_YEAR, END_YEAR):
    """
    Calculates population growth for all populations
    :param START_YEAR:
    :param END_YEAR:
    :return: None
    """

    global CURSOR

    START_YEAR = int(START_YEAR)
    END_YEAR = int(END_YEAR)

    START_YEAR_POPULATION = CURSOR.execute("""
        SELECT
            fall_population_estimate
        FROM    
            data
        WHERE
            population_year = ?
    ;""", [START_YEAR]).fetchall()

    END_YEAR_POPULATION = CURSOR.execute("""
            SELECT
                fall_population_estimate
            FROM    
                data
            WHERE
                population_year = ?
        ;""", [END_YEAR]).fetchall()

    START_POPULATION = []
    END_POPULATION = []


    for i in range(len(START_YEAR_POPULATION)):
        START_YEAR_POPULATION[i] = list(START_YEAR_POPULATION[i])
        START_POPULATION.append(START_YEAR_POPULATION[i][0])

    for i in range(len(END_YEAR_POPULATION)):
        END_YEAR_POPULATION[i] = list(END_YEAR_POPULATION[i])
        END_POPULATION.append(END_YEAR_POPULATION[i][0])

    for i in range(len(START_POPULATION)):
        if START_POPULATION[i] == "NA":
            START_POPULATION[i] = 0

    for i in range(len(END_POPULATION)):
        if END_POPULATION[i] == "NA":
            END_POPULATION[i] = 0

    START_TOTAL = sum(START_POPULATION)
    END_TOTAL = sum(END_POPULATION)

    TOTAL_GROWTH = (END_TOTAL - START_TOTAL)/(END_YEAR - START_YEAR)
    TOTAL_GROWTH = round(TOTAL_GROWTH)

    print(f"The total growth of all animals from {START_YEAR} to {END_YEAR} is {TOTAL_GROWTH} animals/year.")


def viewData(YEAR, USER_ANIMAL):
    """
    View the data of an animal from a specific year in a table
    :return: None
    """

    if USER_ANIMAL == 1:
        ANIMAL = "Bison"
    if USER_ANIMAL == 2:
        ANIMAL = "Moose"
    if USER_ANIMAL == 3:
        ANIMAL = "Elk"
    if USER_ANIMAL == 4:
        ANIMAL = "Deer"


    global CURSOR

    DATA = CURSOR.execute("""
        SELECT
            *
        FROM 
            data
        WHERE
            population_year = ?
        AND
            species_name = ?  
    ;""", [YEAR, ANIMAL]).fetchall()




    print("| Area of park | Population Year | Survey Year | Survey Month | Survey Day | Species name | Unknown age and sex count | Adult male count | Adult female count | Adult unknown count | Yearling count | Calf count | Survey total | Sightability correction factor | Additional captive count | Animals removed prior to survey | Fall population estimate | Any additional survey comments | Estimate method | ")

    for i in range(len(DATA)):
        DATA[i] = list(DATA[i])
        print("|", DATA[i][0], " "*(11-len(DATA[i][0])), "|",
              DATA[i][1], " "*(14-len(str(DATA[i][1]))), "|",
              DATA[i][2], " "*(10-len(str(DATA[i][2]))), "|",
              DATA[i][3], " "*(11-len(str(DATA[i][3]))), "|",
              DATA[i][4], " "*(9-len(str(DATA[i][4]))), "|",
              DATA[i][5], " "*(11-len(DATA[i][5])), "|",
              DATA[i][6], " "*(24-len(str(DATA[i][6]))), "|",
              DATA[i][7], " "*(15-len(str(DATA[i][7]))), "|",
              DATA[i][8], " "*(17-len(str(DATA[i][8]))), "|",
              DATA[i][9], " "*(18-len(str(DATA[i][9]))), "|",
              DATA[i][10], " "*(13-len(str(DATA[i][10]))), "|",
              DATA[i][11], " "*(9-len(str(DATA[i][11]))), "|",
              DATA[i][12], " "*(11-len(str(DATA[i][12]))), "|",
              DATA[i][13], " "*(29-len(str(DATA[i][13]))), "|",
              DATA[i][14], " "*(23-len(str(DATA[i][14]))), "|",
              DATA[i][15], " "*(30-len(str(DATA[i][15]))), "|",
              DATA[i][16], " "*(23-len(str(DATA[i][16]))), "|",
              DATA[i][17], " "*(29-len(str(DATA[i][17]))), "|",
              DATA[i][18], " "*(14-len(str(DATA[i][18]))), "|")




if __name__ == "__main__":


    MY_LIST = []

    LIST = getData(ELK_ISLAND_RAW_DATA)

    if FIRST_RUN:

        LIST = getData(ELK_ISLAND_RAW_DATA)
        Database(LIST)  # Creates the database

    while True:

        CHOICE = menu()

        if CHOICE == 1:
            "Enter the start year, the end year, and the animal name to determine the growth rate of the animal."
            START_YEAR = input("Start year: ")
            END_YEAR = input("End year: ")

            USER_ANIMAL = userAnimal()
            if USER_ANIMAL < 5:
                populationGrowth(START_YEAR, END_YEAR, USER_ANIMAL)
            else:
                allPopulationGrowth(START_YEAR, END_YEAR)

        if CHOICE == 2:
            USER_DATA = userData()
            insertData(USER_DATA)

        if CHOICE == 3:
            print("View all data of an animal from a specific year.")
            YEAR = input("What year: ")
            USER_INPUT = int(input("Bison (1), Moose (2), Elk (3), Deer (4): "))
            viewData(YEAR, USER_INPUT)

        if CHOICE == 4:
            print("Thanks for using the program!")
            exit()

