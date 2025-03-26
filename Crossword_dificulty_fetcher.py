#This code will fetch data from https://xwstats.com/ and get all crosswords data 
import requests  
import pandas as pd  
from bs4 import BeautifulSoup  

#see if there is a 

html_crossword_page = requests.get('https://xwstats.com/puzzles/2025-02-04')
soup = BeautifulSoup(html_crossword_page.content, 'html.parser')