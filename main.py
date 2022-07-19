import requests
from bs4 import BeautifulSoup
import transliterator
# import datetime

url = 'https://multiplex.ua/cinema/khmelnytskyi/oazis'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
city_list = soup.find_all('p', class_='cityname')
city_list = [city.text for city in city_list]

cinema_href_list = soup.find_all(class_='cname_s cname')
cinema_name_list = [cinema_href.find('span').text for cinema_href in cinema_href_list]
cinema_href_list = [cinema.get('href') for cinema in cinema_href_list]
cinema_href_dict = {}
for i in range(len(cinema_href_list)):
    cinema_href_dict[cinema_href_list[i]] = cinema_name_list[i]
counter = 1
print('Оберіть місто: ')
for city in city_list:
    print(f'\t{counter}) {city}')
    counter += 1
index = int(input())
city = city_list[index-1]
if city != 'Запоріжжя':
    transliterate_city = transliterator.transliterate(city)
else:
    transliterate_city = 'zaporizhia'
city_cinema_name_list = [cinema_href_dict[cinema] for cinema in cinema_href_dict if transliterate_city in cinema]
city_cinema_href_list = [cinema for cinema in cinema_href_dict if transliterate_city in cinema]
counter = 1
if len(city_cinema_name_list) != 0:
    print('Оберіть кінотеатр: ')
    for cinema in city_cinema_name_list:
        print(f'\t{counter}) {cinema}')
        counter += 1
    index = int(input())
    cinema_href = city_cinema_href_list[index-1]
else:
    print('У цьому місті немає кінотеатрів Multiplex')
    exit(0)


def correct_num(num):
    if num < 10:
        return '0' + str(num)
    return num


def getFilmTrailer(film_url):
    url = 'https://multiplex.ua' + film_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    film_trailer = soup.find(class_="trailerbut playtrailer").get('data-fullyturl')
    return film_trailer


def getFilmPoster(film_url):
    url = 'https://multiplex.ua' + film_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    film_poster = soup.find('img', class_="poster").get('src')
    return 'https://multiplex.ua' + film_poster


def getFilmData(film_url):
    url = 'https://multiplex.ua' + film_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    age = soup.find('div', class_="val")
    film_keys = [s.text for s in soup.find_all('p', class_="key")]
    film_vals = [s.text for s in soup.find_all('p', class_="val")]
    film_vals = [age.text.split()[0]] + film_vals
    film_data = dict(zip(film_keys, film_vals))
    return film_data


def getFilmDescription(film_url):
    url = 'https://multiplex.ua' + film_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    description = soup.find('div', class_='movie_description').text
    return description


print('Оберіть дату: ')
for i in range(7):
    date = datetime.datetime.now() + datetime.timedelta(days=i)
    print(f'{i+1}) {correct_num(date.day)}.{correct_num(date.month)}.{date.year}')

delta = int(input()) - 1
chosen_date = datetime.datetime.now() + datetime.timedelta(days=delta)
href_date = f'{correct_num(chosen_date.day)}{correct_num(chosen_date.month)}{chosen_date.year}'

new_url = 'https://multiplex.ua' + cinema_href + '#' + href_date
r = requests.get(new_url)
soup = BeautifulSoup(r.text, 'html.parser')
if int(href_date[:2]) != datetime.datetime.now().day:
    film_soup = soup.find_all(class_='cinema_inside sch_date hidden')
    film_soup = [s for s in film_soup if s.get('data-date') == href_date]
    film_soup_list = film_soup[0].find_all('div', class_='film')
    film_soups = film_soup[0].find_all('a', class_='title')
else:
    film_soup_list = soup.find(class_='cinema_inside sch_date').find_all('div', class_='film')
    film_soups = [s.find('a', class_='title') for s in film_soup_list]

titles = [t.get('title').strip() for t in film_soups]
hrefs = [t.get('href') for t in film_soups]

print('Оберіть фільм: ')
for i in range(len(titles)):
    film_data = getFilmData(hrefs[i])
    genres = film_data['Жанр:'].split()
    print(f"{i+1}) {titles[i].strip()} ({film_data['Рейтинг Imdb:']})")
    g = ''
    for genre in genres:
        g += genre + ' '
    print(g, '\n')

index = int(input())

print(getFilmDescription(hrefs[index-1]))
print(f'Poster: {getFilmPoster(hrefs[index-1])}')
print(f'Trailer: {getFilmTrailer(hrefs[index-1])}')
film_times_list = film_soup_list[index-1].find_all('div', class_='ns')
film_times_list = [s.find('span').text for s in film_times_list]

print('Доступні часи:')
for time in film_times_list:
    print(time)
