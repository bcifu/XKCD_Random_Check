from selenium.webdriver import Chrome
import re
import pickle
import os
import argparse
import random
from progress.bar import Bar

parser = argparse.ArgumentParser(description= "get information on XKCD random for all comics a specefied number of times")
parser.add_argument('--repeat_times', '-r', default=2)
repeat = parser.parse_args().repeat_times

#Load any past data
if os.path.isfile('data.pickle'):
    data = pickle.load(open('data.pickle', 'rb'))
else:
    data = {}

#Data is structured with the keys as the starting comment and each value in its dict as a redirect instance

#Expects the driver to be in the current folder
driver = Chrome(executable_path="chromedriver.exe")

#extract the number of comics
driver.get('https://xkcd.com')
permalink = re.search(r'Permanent link.*<br>', driver.find_element_by_id(
    'middleContainer').get_attribute('innerHTML')).group(0)
numberOfComics = int(re.search(r'\d+', permalink).group(0))

#randomize the order to make this more fair...
#Due to some limitations of random this is not truly random but who cares
#This isn't a scientific study, I'm just bored and programming
comicList = []
for repeatCount in range(repeat):
    comicList.extend(range(1, numberOfComics + 1))
random.shuffle(comicList)

for comicNum in Bar('Checking').iter(comicList):
    driver.get('https://xkcd.com/{}/'.format(comicNum))
    driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li[3]/a').click()
    newNumber = int(re.search(r'\d+', driver.current_url).group(0))
    #because this is a list, treat as such
    if comicNum in data:
        data[comicNum].append(newNumber)
    else:
        data[comicNum] = [newNumber]

pickle.dump(data, open('newsave.pickle', 'wb'))
if os.path.isfile('data.pickle'):
    os.remove('data.pickle')

os.rename('newsave.pickle', 'data.pickle')

driver.close()
