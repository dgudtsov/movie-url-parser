# movie-url-parser

  

This tool is created to parse input text file as shown in [examples/input-example.txt](/examples/input-example.txt)

into CSV form of [examples/output-example.csv](/examples/output-example.csv)

using external movie db web service - api.kinopoisk.dev

## Usage

1) get token from one of serives:

kinopoisk.dev

kinopoiskapiunofficial.tech

2) set TOKEN variable in environment:

TOKEN=xxxyyyzzz...

  

3) prepare list of URLs as input file,e.g.:

% cat file-input

https://www.kinopoisk.ru/film/127063

https://www.kinopoisk.ru/series/1331649/

https://www.kinopoisk.ru/series/1199731/?ysclid=ltfslo2nm3760607930&utm_referrer=yandex.ru

  

4) run script, pointing in '-a' option kp-dev or kp-unoff value depenging on your choise in item 1 above:

% movie_url_parser.py -a kp-unoff -o result.csv file-input

using API: kp-unoff

parsing file1

...

done

  

5) check result in file result.csv
