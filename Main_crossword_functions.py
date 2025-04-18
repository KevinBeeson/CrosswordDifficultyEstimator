#This file will contain the main function for the program
import pandas as pd
import os 
import logging
def empty_spaces(answers_square: list)->int:
    #This function will return the number of empty spaces in the crossword
    empty = 0
    for row in answers_square:
        for letter in row:
            if letter == '#':
                empty += 1
    return empty

def filled_spaces(answers_square: list)->int:
    #This function will return the number of filled spaces in the crossword
    filled = 0
    for row in answers_square:
        for letter in row:
            if letter != '#':
                filled += 1
    return filled

def split_sections(raw_crossword: str,date: str):
    #This function will split the raw xd file into the three sections, metadata, answers, and clues
    metadata = {}
    answers_square = []
    location = []
    clues = []
    answers = []

    # Get the meta data from the header of the string and sees where the metadata ends
    metadata_wanted=['title','author','copyright','date']
    for end_of_metadata,line in enumerate(raw_crossword):
        if line == '\n':
            break
        line_split = line.split(":")
        #check if the line contains the metadata we want
        if line_split[0].lower() in metadata_wanted:
            metadata[line_split[0]] = line_split[1].strip()
    if not 'Date' in metadata:
        metadata['Date'] = date
    if not 'Copyright' in metadata:
        metadata['Copyright'] = 'No copyright'
    if not 'Author' in metadata:
        metadata['Author'] = 'No author'
    if not 'Title' in metadata:
        metadata['Title'] = 'No title'

    # Get the answers from the string

    for i in range(end_of_metadata+2,len(raw_crossword)):
        if raw_crossword[i] == '\n':
            break
        else:
            answers_square.append(raw_crossword[i].strip())
    # Get the clues from the string
    accross_clues = []
    accross_answers= []
    down_clues = []
    down_answers = []
    accross_location = []
    down_location = []
    for j in range(i+2,len(raw_crossword)):
        if raw_crossword[j] == '\n':
            break
        else:
            line=raw_crossword[j].strip()
            clue_line=line.split("~")[0].strip()
            accross_location.append(clue_line.split(".")[0].strip())
            accross_clues.append(clue_line.split(".")[1].strip())
            accross_answers.append(line.split("~")[1].strip())
    for k in range(j+1,len(raw_crossword)):
        if raw_crossword[k] == '\n':
            break
        line=raw_crossword[k].strip()
        clue_line=line.split("~")[0].strip()
        down_location.append(clue_line.split(".")[0].strip())
        down_clues.append(clue_line.split(".")[1].strip())
        down_answers.append(line.split("~")[1].strip())

    clues.append(accross_clues)
    clues.append(down_clues)
    answers.append(accross_answers)
    answers.append(down_answers)
    location.append(accross_location)
    location.append(down_location)
    return metadata,answers_square,location,clues,answers
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
        logging.warning("The file for the date "+date+" does not exist")
        return None
    elif len(masked) > 1:
        logging.warning("There are multiple files for the date "+date+" please specify the file")
        return None
    else:
        directory=base+"/"+year+"/"+masked[0]
    #We will now open the file and read it into a list
    try:
        with open(directory) as f:
            crossword = f.readlines()
    except:
        logging.warning("The file for the date "+date+" does not exist")
        return None
    return crossword
def __main__():
    date='2021-01-01'
    crossword=opening_file(date)
    metadata,answers,clues=split_sections(crossword,date)
    logging.info(metadata)
    logging.info(answers)
    logging.info(clues)
    logging.info(empty_spaces(answers))


