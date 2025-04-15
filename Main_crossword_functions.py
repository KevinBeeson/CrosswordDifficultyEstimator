#This file will contain the main function for the program
import pandas as pd
import os 

def empty_spaces(answers: list)->int:
    #This function will return the number of empty spaces in the crossword
    empty = 0
    for row in answers:
        for letter in row:
            if letter == '#':
                empty += 1
    return empty

def filled_spaces(answers: list)->int:
    #This function will return the number of filled spaces in the crossword
    filled = 0
    for row in answers:
        for letter in row:
            if letter != '#':
                filled += 1
    return filled

def split_sections(raw_crossword: str):
    #This function will split the raw xd file into the three sections, metadata, answers, and clues
    metadata = {}
    answers = []
    clues = []

    # Get the meta data from the header of the string and sees where the metadata ends
    metadata_wanted=['title','author','copyright','date']
    for end_of_metadata,line in enumerate(raw_crossword):
        if line == '\n':
            break
        line_split = line.split(":")
        #check if the line contains the metadata we want
        if line_split[0].lower() in metadata_wanted:
            metadata[line_split[0]] = line_split[1].strip()


    # Get the answers from the string

    for i in range(end_of_metadata+2,len(raw_crossword)):
        if raw_crossword[i] == '\n':
            break
        else:
            answers.append(raw_crossword[i].strip())
    # Get the clues from the string
    accross_clues = []
    down_clues = []
    for j in range(i+2,len(raw_crossword)):
        if raw_crossword[j] == '\n':
            break
        else:
            accross_clues.append(raw_crossword[j].strip())
    for k in range(j+1,len(raw_crossword)):
        down_clues.append(raw_crossword[k].strip())
    clues.append(accross_clues)
    clues.append(down_clues)
    return metadata,answers,clues
def opening_file(date: str, base: str = 'nytimes') -> list[str]:
    #This function will open the right new york times crossword file given the date
    base='xd-puzzles/gxd/'+base

    year=date.split("-")[0]
    month=date.split("-")[1]
    day=date.split("-")[2]
    #The prefix for the company names are all different and kinda random so we will find the prefix first

    all_files=os.listdir(base+"/"+year)
    masked = [s for s in all_files if date in s]
    if len(masked) == 0:
        print("The file for the date "+date+" does not exist")
        return None
    elif len(masked) > 1:
        print("There are multiple files for the date "+date+" please specify the file")
        return None
    else:
        directory=base+"/"+year+"/"+masked[0]
    #We will now open the file and read it into a list
    try:
        with open(directory) as f:
            crossword = f.readlines()
    except:
        print("The file for the date "+date+" does not exist")
        return None
    return crossword
def __main__():
    date='2021-01-01'
    crossword=opening_file(date)
    metadata,answers,clues=split_sections(crossword)
    print(metadata)
    print(answers)
    print(clues)
    print(empty_spaces(answers))


