# CrosswordDifficultyEstimator
The endgame for this tool is to create a tool that you can input a set of clues and answers and then the python tool will then estimate how long it will take for an average crossword user to finish the crossword.

# Data sources

The New York Time runs a long running daily crosswords. These crosswords differ in dificulty based on the day of the week. With Monday's being considered the easiest and Saturday the hardest. As there is a large variety of hardness and with a large amount of data I have choosen to focus on this crossword.


https://xwstats.com/ Will be the main source of data for average completion time for a crossword. The website allows users to track their average time to complete the New York Times Crossword. The website provides the average amount of time (Global Median Solver) for a user to finish the NYT crossword.

To get the crosswords it self I have been using two websites https://xd.saul.pw/ and https://www.xwordinfo.com/. 


Throught this excersice I will minimize the amount of data that isnt generated inhouse and will try to replicate metrics on these websites.


1. 

# tools
- Crossword_dificulty_fetcher.py can get the average time to complete a crosswords from https://xwstats.com/ and then stores it in crosswords_hardness.csv

- Graph_creator.ipynb Creates the graphs used in the pelimenary data analysis 

- Main_crossword_functions.py stores the functions that will be used multiple times accross different programs

# Preliminary data analysis from the https://xwstats.com/

Xwstats provides data for the average time to solve a crossword from 1995, although the data is provided from then some of the older crosswords will be a retroactive solve (i.e. The user was solving a crossword that was not freshly printed that week). 

Looking at The image below we can crealy see that any data before 2018 diverges into three main sections. Not sure why this happens maybe some users dominate these crosswords. not sure. so for the rest of the anaylsis we will only be using data afer 2018.

![image](Images/Average%20time%20to%20complete%20the%20crossword%20on%20Wednesdays.png)

Lets then see the avergae time it takes to solve a crossword divided into the crosswords release day.

![image](Images/average_time_by_day.png)

We can clearly see that the Monday crossword takes the least amount of time and Sundays takes the most. However this data can be skewed as some crosswords require more letters to solve than others.

![image](Images/crossword_time_per_letter_by_day.png)

When we Normalise this by the amount of letters needed to solve the crossword we can see that Saturday and Sunday swap places. Friday overtakes Saturday. This shows that Sunday's longer solving time is partly down to the crossword size rather than the clues hardness.