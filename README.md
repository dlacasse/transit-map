# Transit Map

## Overview
CLI program to interact with the MBTA subway map (and theoretically others). Running the program (see below) will output information for the first two questions then start a prompt where you can enter origin/destination stops to get a possible list of routes to travel between them.

## How To Run
* I used python3 + pipenv for this project
* You can install the dependencies prior to running by running `pipenv install`

### Running the tests:
`pipenv run pytest`

### Running the cli app:
`pipenv run python3 main.py`

*Note:* You can exit the program by typing "exit" for the origin or issuing a SIGINT (control + c).


## Assumptions
* The API breaks out the different Green Line (and Red Line) branches into separate routes. There might be times when displaying this as one "line" would be more intuitive, but I think it is actually more realistic to keep them separate. It simplifies the reality that while they share some stops, they diverge -- you can never get to Riverside directly on a Green Line E train.
* The code is structured to be modular, but the `MBTADataProvider` is hard-coded in the CLI class. To support multiple, we'd need to revisit this and make it either selectable by the user or based on some sort of config / CLI arguments.


## What's next, given more time
* Additional test coverage -- I mostly focused on testing the TransitMap / Routes classes since that's where most of the complexity lies.
* Additional input sanitization / error handling
* Better error handling around API failures


## Questions 1
For this implementation, I chose to have the API server do the filtering (e.g. `filter[type]=0,1`). The key driving factors that facilitated this decision for me were:
1. The data set is fairly large when unfiltered -- seems like a bit of a waste if we're going to use any of it. If we need it in the future, it'll be easy enough to extend the solution to add it.
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
The output below attempts to answer the questions posed under Question 2. Note: For the most stops, there is a tie so I decided to allow the program to return multiple routes


### Output
```
The subway route(s) with the most stops are:
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
The solution uses an algorithm in the style of depth-first search to find a feasible route between two stops. If we wanted to actually make this optimized for fewest stops (for example) we'd need to do a bit of work to enhance the algorithm.

### Output
```
Route Finder
==============================
Enter origin: Davis
Enter destination: Kendall/MIT

Davis to Kendall/MIT -> Red Line

Route Finder
==============================
Enter origin: Ashmont
Enter destination: Riverside

Ashmont to Riverside -> Red Line, Green Line D

Route Finder
==============================
Enter origin: Ashmont
Enter destination: Copley

Ashmont to Copley -> Red Line, Green Line B

Route Finder
==============================
Enter origin: Ashmont
Enter destination: Hynes Convention Center

Ashmont to Hynes Convention Center -> Red Line, Green Line B

Route Finder
==============================
Enter origin: Broadway
Enter destination: Airport

Broadway to Airport -> Red Line, Green Line B, Blue Line

Route Finder
==============================
Enter origin: Mattapan
Enter destination: Wood Island

Mattapan to Wood Island -> Mattapan Trolley, Red Line, Green Line B, Blue Line
```