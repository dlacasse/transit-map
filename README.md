# Transit Map

## Overview


## How to run
### Running the program
`pipenv run python3 main.py`

### Running the tests
`pipenv run pytest`


## Assumptions
* The API breaks out the different Green Line (and Red Line) branches into separate routes. There might be times when displaying this as one "line" would be more intuitive, but I think it is actually more realistic to keep them separate. It simplifies the reality that while they share some stops, they diverge -- you can never get to Riverside directly on a Green Line E train.


## Questions 1
For this implementation, I chose to have the API server do the filtering (e.g. `filter[type]=0,1`). The key driving factors that facilitated this decision for me were:
1. The data set is fairly large unfiltered -- seems like a bit of a waste if we're going to use any of it. If we need it in the future, it'll be easy enough to extend the solution to add it.
2. The filter functionality is a well-documented documented parameter in the documentation for the API and therefore it seems reasonable to depend on this feature.

Output:
```
All Subway routes:
==============================
Blue Line
Green Line B
Green Line C
Green Line D
Green Line E
Mattapan Trolley
Orange Line
Red Line
```

## Question 2

### Output
```
he subway route(s) with the most stops are:
==============================
Green Line E: 25
Green Line D: 25

The subway route(s) with the fewest stops are:
==============================
Mattapan Trolley: 8

Subway stops which connect two or more routes:
==============================
Arlington (Green Line B, Green Line C, Green Line D, Green Line E)
Ashmont (Mattapan Trolley, Red Line)
Boylston (Green Line B, Green Line C, Green Line D, Green Line E)
Copley (Green Line B, Green Line C, Green Line D, Green Line E)
Downtown Crossing (Orange Line, Red Line)
Government Center (Blue Line, Green Line B, Green Line C, Green Line D, Green Line E)
Haymarket (Green Line D, Green Line E, Orange Line)
Hynes Convention Center (Green Line B, Green Line C, Green Line D)
Kenmore (Green Line B, Green Line C, Green Line D)
Lechmere (Green Line D, Green Line E)
North Station (Green Line D, Green Line E, Orange Line)
Park Street (Green Line B, Green Line C, Green Line D, Green Line E, Red Line)
Science Park/West End (Green Line D, Green Line E)
State (Blue Line, Orange Line)
```

## Question 3


### Output

#### Examples
```python
#transit_cli.get_travel_info('Davis', 'Kendall/MIT')
#transit_cli.get_travel_info('Ashmont', 'Riverside')
#transit_cli.get_travel_info('Ashmont', 'Copley')
#transit_cli.get_travel_info('Ashmont', 'Hynes Convention Center')
#transit_cli.get_travel_info('Ashmont', 'Government Center') 
#transit_cli.get_travel_info('Broadway', 'Airport')
#transit_cli.get_travel_info('Riverside', 'Back Bay')
#transit_cli.get_travel_info('Mattapan', 'Wood Island')
```

