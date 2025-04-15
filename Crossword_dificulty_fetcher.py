#This code will fetch data from https://xwstats.com/ and get all crosswords data 
import requests  
import pandas as pd  
from bs4 import BeautifulSoup  
import time
import logging

#see if there is a 

# Load pandas dataframe
try:
    df = pd.read_csv('crosswords_hardness.csv')
except:
    df = pd.DataFrame(columns = ['title', 'date','difficulty','average_time','average_increase', 'faster', 'much_faster', 'slower', 'much_slower'])


for pages in range(1,458):
    # load the main puzzle page
    main_page = requests.get('https://xwstats.com/puzzles?p='+str(pages))
    soup = BeautifulSoup(main_page.content, 'html.parser')
    links=soup.find_all("a",class_="puzzle")
    dates=[]
    links=[]
    for link in soup.find_all("a",class_="puzzle"):
        date_time=link.get_text()
        date=pd.to_datetime(date_time.split("-")[1].strip())
        dates.append(date)
        links.append(link.get("href"))

    example_date=dates[0]
    example_link="https://xwstats.com"+links[0]
    for date,link in zip(dates,links):
        if date not in pd.to_datetime(df['date']).values:
            logging.info("Fetching data for the first time")
            logging.info("Fetching "+date.strftime("%Y-%m-%d"))
            # load the first crossword page
            html_crossword_page = requests.get("https://xwstats.com"+link)
            soup = BeautifulSoup(html_crossword_page.content, 'html.parser')

            title=soup.find("h1").get_text()
            date=title.split("-")[1].strip()
            date=pd.to_datetime(date)
            title=title.split("-")[0].strip()

            main_values=soup.find_all("div",class_="stat-value")
            difficulty=main_values[0].get_text()
            average_time=main_values[1].get_text()
            average_increase=main_values[2].get_text()
            adjective=average_increase.split(" ")[1]
            if adjective=="faster":
                average_increase=float(average_increase.split(" ")[0][:-1])
            else:
                average_increase=average_increase.split(" ")[0][:-1]
                average_increase=-1*float(average_increase)


            small_text_facts =soup.find("ul", class_="achievements")
            small_text_facts=small_text_facts.get_text()
            small_text_facts=small_text_facts.split("\n")
            small_text_facts=[x for x in small_text_facts if x]
            faster=small_text_facts[0]
            faster_number=faster.split(" ")[0]
            faster_number = float(''.join(filter(str.isdigit, faster_number)))
            much_faster=small_text_facts[1].strip()
            much_faster_number=much_faster.split(" ")[0]
            much_faster_number = float(''.join(filter(str.isdigit, much_faster_number)))
            slower=small_text_facts[2]
            slower_number=slower.split(" ")[0]
            slower_number = float(''.join(filter(str.isdigit, slower_number)))
            much_slower=small_text_facts[3].strip()
            much_slower_number=much_slower.split(" ")[0]
            much_slower_number = float(''.join(filter(str.isdigit, much_slower_number)))
            df.loc[len(df)]={'title': title, 'date': str(date.date()),'difficulty':difficulty,'average_time':average_time,'average_increase':average_increase, 'faster':faster_number, 'much_faster':much_faster_number, 'slower':slower_number, 'much_slower':much_slower_number}
            df.to_csv('crosswords_hardness.csv', index=False)
            logging.info("Data fetched")
            #wait for 1 second
            time.sleep(1)
        else:
            logging.info("Data already fetched")
