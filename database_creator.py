#This file will create a database of all the crosswords and also calculate some statistics

import sqlite3
import pandas as pd
import Main_crossword_functions as mcf
import os
import json

con = sqlite3.connect("crossword.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS crosswords")
cur.execute("""
CREATE TABLE crosswords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    copyright TEXT,
    date TEXT,
    company TEXT,
    answers_square TEXT, -- list of strings
    location TEXT, -- list of strings  
    clues TEXT, -- list of strings
    answers TEXT -- list of strings
)
""")
cur.execute("DROP TABLE IF EXISTS clues")
cur.execute("""
            CREATE TABLE clues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crossword_id INTEGER,
    clue TEXT,
    answer TEXT,
    direction TEXT, -- 'across' or 'down'
    number INTEGER, -- clue number
    FOREIGN KEY (crossword_id) REFERENCES crosswords(id)
)"""
)

names_of_companies = os.listdir('xd-puzzles/gxd/')
for company in names_of_companies:
    years=os.listdir('xd-puzzles/gxd/'+company)
    for year in years:
        dates=os.listdir('xd-puzzles/gxd/'+company+'/'+year)
        for date in dates:
                        # get prefix
            prefix=""
            for letter in date:
                if letter.isdigit():
                    break
                else:
                    prefix+=letter
            # get the date
            date=date[len(prefix):-3]
            crossword=mcf.opening_file(date,company)
            metadata,answers_square,location,clues,answer=mcf.split_sections(crossword)

            #title,author,copyright,date, company, answers_square,location,clues,answer
            metadata_strings=[str(metadata[x]) for x in metadata]
            metadata_strings+=[company,json.dumps(answers_square),json.dumps(location),json.dumps(clues),json.dumps(answer)]
            # Insert metadata into the crosswords table
            table_name = 'crosswords'
            cur.execute(f"PRAGMA table_info({table_name})")

            try:
                cur.execute("""INSERT INTO crosswords (title, author, copyright, date, company, answers_square, location, clues, answers)
                            VALUES (?,?,?,?,?,?,?,?,?)"""
                            ,metadata_strings)
            except sqlite3.ProgrammingError:
                print("Error: ",metadata_strings)
                print("Error: ",cur.execute(f"PRAGMA table_info({table_name})").fetchall())
                raise
            con.commit()

            crossword_id = cur.lastrowid

            # Insert clues into the clues table
            for i, clue in enumerate(clues[0]):
                cur.execute("INSERT INTO clues (crossword_id, clue, answer, direction, number) VALUES (?, ?, ?, ?, ?)",
                            (crossword_id, clue, answer[0][i], 'across', int(location[0][i][1:])))
            for i, clue in enumerate(clues[1]):
                cur.execute("INSERT INTO clues (crossword_id, clue, answer, direction, number) VALUES (?, ?, ?, ?, ?)",
                            (crossword_id, clue, answer[1][i], 'down', int(location[1][i][1:])))
            con.commit()
            # Insert grid locations into the grid_locations table

