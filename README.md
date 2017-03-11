[![Codacy Badge](https://api.codacy.com/project/badge/Grade/74308b89ad164e79a6d9ffbf4a14394a)](https://www.codacy.com/app/andela-hms/CP1?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-hms/CP1&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/andela-hms/CP1/badge.svg?branch=master)](https://coveralls.io/github/andela-hms/CP1?branch=master)
[![Humphrey Musonye](https://img.shields.io/badge/humphrey%20musonye-CP1%20Amity-brightgreen.svg)]()

# AMITY ROOM ALLOCATION SYSTEM.
>A project done in fulfillment of the first checkpoint of the Andela training program.

#1. Problem definition

The main objective of this project is to model a room allocation system for one of Andela’s facilities called Amity.

**Who? Fellows and staff at one of Andela's facilities alias Amity.**

Fellows and staff at Andela's Amity facility are the immediate consumers of the system.

**What? A room allocation system**

The goal is to model and build a room allocation system that smoothens the problem of keeping track of office ad living spaces at Amity, providing a scalable and usable solution.

>An office can occupy a maximum of 6 people. A living space can inhabit a maximum of 4 people.

**Where? Office spaces and living spaces.**

The system manages office spaces as well as living spaces and ensures they are allocated effectively.

**When? On request to occupy a space.**

The spaces mentioned above need to be allocated when vacant or occupied and/or reallocated as well as give status on their status when required.
The system serves to also tell how many people are in a given space at any given time.

**Why? To ensure smooth and seamless allocation and transfer of rooms amongst fellow and staff.**

The criteria set to solve the problem is to ensure the rooms can and will be allocated on request to get a new space whether office space or living space.
There is also the need to have a way of determing how many people are at a particular space from time to time.


#2. Commands

Command | Argument | Example
--- | --- | ---
create_room | L or O | create_room O Emirates
add_person | (first_name) (last_name) (person_type) [wants_accomodation] |add_person Alexis Sanchez Fellow Y
reallocate_person | (identifier) (new_room_name) | reallocate_person 4758696 emirates
load_people | (filename) | load_people
print_allocations| [--o=filename] | print_allocations --o=allocations
print_unallocated| [--o=filename] | print_unallocated --o=allocations
print_room | (room_name) | print_room emirates
save_state | [--db=sqlite_database]| save_state --db=amity
load_state |(sqlite_database)|load_state amity

#3. Installation and setup

1. First clone this repository to your local machine using `https://github.com/andela-hms/CP1.git`

2. Checkout into the **master** branch using `git checkout master`

3. Create a **virtualenv** on your machine and install the dependencies via `pip install -r requirements.txt` and activate it.

4. cd into the **app** folder and run `python run-app.py --interactive`

#4. Usage
The following screencast shows how to run the app. Check it out:

[![asciicast](https://asciinema.org/a/90nbku8jisl9u3fk1jocj08yx.png)](https://asciinema.org/a/90nbku8jisl9u3fk1jocj08yx)


#5. Tests

To run nosetests ensure that you are within the *virtual environment* and have the following installed:

1. *nose*
2. *coverage*

After ensuring the above, within the **amity folder** run :

`nosetests --with-coverage` and

`coverage report`

## Credits

1. [Humphrey Musonye](https://github.com/andela-hms)

2. The [Andela](https://www.andela.com) community.
