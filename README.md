# Fuzzy Picker
This package is a thin wrapper providing interactive capability for the
excellent [FuzzyWuzzy Python Library](https://github.com/seatgeek/fuzzywuzzy).

## Installation
```
pip install fuzzypicker
```

## Usage

Fuzzy picker is intended to be used in your console scripts.  Let's say that you
had a script that needed to select from a variety of options.  As an example, 
let's say you want your users to choose from a selection of movies.

Simply place the following code in a file called `doit.py` and execute it.
You will see the interactive display shown below.

```python
from fuzzypicker import picker

movies = [
    'Rachel Getting Married',
    'Penelope',
    'P.S. I Love You',
    'Over Her Dead Body',
    'Our Family Wedding',
    'One Day',
    'Not Easily Broken',
    'No Reservations',
    'My Week with Marilyn',
    'Music and Lyrics',
    'Monte Carlo',
    'Miss Pettigrew Lives for a Day',
    'Midnight in Paris',
    'Marley and Me',
    'Mamma Mia!',
    'Made of Honor',
    'Love Happens',
    'Love & Other Drugs',
    'Life as We Know It',
]

print(f'selected_movie = {picker(movies)}')
```
![Alt Text](https://github.com/robdmc/fuzzypicker/blob/master/fuzzypicker.gif)

