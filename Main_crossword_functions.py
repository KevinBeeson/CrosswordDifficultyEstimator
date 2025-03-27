#This file will contain the main function for the program
import pandas as pd

def empty_spaces(answers: list)->int:
    #This function will return the number of empty spaces in the crossword
    empty = 0
    for row in answers:
        for letter in row:
            if letter == '#':
                empty += 1
    return empty

def split_sections(raw_crossword: str):
    #This function will split the raw xd file into the three sections, metadata, answers, and clues
    metadata = {}
    answers = []
    clues = []

    # Get the meta data from the header of the string
    title=raw_crossword[0].split(":")[1].strip()

    author=raw_crossword[1].split(":")[1].strip()

    copyright=raw_crossword[2].split(":")[1].strip()

    date = raw_crossword[3].split(":")[1].strip()

    metadata['title'] = title
    metadata['author'] = author
    metadata['copyright'] = copyright
    metadata['date'] = date

    # Get the answers from the string

    for i in range(6,len(raw_crossword)):
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
def opening_file(date:str)->list[str]:
    #This function will open the right new york times crossword file given the date
    base='xd-puzzles/gxd/nytimes'
    year=date.split("-")[0]
    month=date.split("-")[1]
    day=date.split("-")[2]
    directory=base+"/"+year+"/nyt"+date+".xd"
    with open(directory) as f:
        crossword = f.readlines()
    return crossword
def __main__():
    date='2021-01-01'
    crossword=opening_file(date)
    metadata,answers,clues=split_sections(crossword)
    print(metadata)
    print(answers)
    print(clues)
    print(empty_spaces(answers))


