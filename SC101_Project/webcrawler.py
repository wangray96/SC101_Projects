"""
File: webcrawler.py
Name: Ray
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10900879
Female Number: 7946050
---------------------------
2000s
Male Number: 12977993
Female Number: 9209211
---------------------------
1990s
Male Number: 14146310
Female Number: 10644506
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names' + year + '.html'

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # ----- Write your code below this line ----- #
        tags = soup.find_all('td')
        data_list = []
        for tag in tags:
            text = tag.text.split()
            if len(text) == 1:
                data_list.append(text[0])
        text_count = 0
        rank_list = []  # a list of each rank
        sum_male = 0
        male = ''  # the number of male name of each rank
        sum_female = 0
        female = ''  # the number of female name of each rank
        for word in data_list:
            text_count += 1
            rank_list.append(word)
            # each rank_list has five elements
            if text_count % 5 == 0 and text_count <= 1000:
                for ch in rank_list[2]:  # the number of male
                    if ch.isdigit():
                        male += ch
                sum_male += int(male)
                male = ''
                for ch in rank_list[4]:  # the number of female
                    if ch.isdigit():
                        female += ch
                sum_female += int(female)
                female = ''
                rank_list = []
        print(f'Male Number: {sum_male}')
        print(f'Female Number: {sum_female}')


if __name__ == '__main__':
    main()
