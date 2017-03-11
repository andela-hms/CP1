# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
AMITY room allocation system

Usage:
    amity add_person <first_name> <last_name> <role> [(y|n)]
    amity reallocate_person <first_name> <last_name> <room_name>
    amity save_state [--db=sqlite_database]
    amity load_state <database>
    amity print_allocations [--o=filename]
    amity print_unallocated [--o=filename]
    amity load_people
    amity print_room <room_name>

Help:
    For help using this app, please open an issue on the Github repository:
    https://github.com/andela-hms

Options:
    -h --help     Show this screen.
    -i --interactive  Interactive Mode
    -v --version
"""
import sys
import os
import time
import cmd
from pyfiglet import Figlet
from termcolor import colored
from docopt import docopt, DocoptExit
from amity import Amity

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command! Use this instead:')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

def delay_print(stuff):
    """Delays screen output"""
    for string in stuff:
        sys.stdout.write('%s' %string)
        sys.stdout.flush()
        time.sleep(0.001)

class ScreenOut(cmd.Cmd):
    """main class"""

    os.system('clear')
    fig_font = Figlet(font='poison', justify='left', width=200)
    print ("\n")
    print(colored(fig_font.renderText('( AMITY )'),\
         'green', attrs=['bold']))

    intro = colored('Version 1.0\t\t Enter "quit" to exit \n', 'green', attrs=['bold'])

    nice = colored('(amity) ~ ', 'cyan', attrs=['blink'])
    prompt = nice

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.amity = Amity()

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_name>..."""
        room_type = args['<room_type>']
        room_names = args['<room_name>']

        msg = self.amity.create_room(room_type, *room_names)
        if "!" in msg:
            msg += '  ✘'
            msg = colored(msg, 'red', attrs=['bold', 'dark'])
            print(msg)
        else:
            msg += '  ✔'
            msg = colored(msg, 'green', attrs=['bold', 'dark'])
            print(msg)

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <fname> <lname> <role> [<wants_accomodation>]"""
        fname = args['<fname>']
        lname = args['<lname>']
        role = args['<role>']
        wants_accomodation = args['<wants_accomodation>']

        try:
            if wants_accomodation.upper() not in ['Y', 'N']:
                msg = "Invalid accomodation parameter! Please use Y or N  ✘"
                msg = colored(msg, 'red', attrs=['bold', 'dark'])
                print(msg)

            if role.upper() not in ['FELLOW', 'STAFF']:
                msg = "Invalid role parameter! Please use FELLOW or STAFF  ✘"
                msg = colored(msg, 'red', attrs=['bold', 'dark'])
                print(msg)

            else:
                msg = self.amity.add_person(fname, lname, role, wants_accomodation)
                msg += '  ✔'
                msg = colored(msg, 'green', attrs=['bold', 'dark'])
                print(msg)

        except AttributeError:
            msg = "Please indicate if person wants accomodation!  ✘"
            msg = colored(msg, 'red', attrs=['bold', 'dark'])
            print(msg)

    @docopt_cmd
    def do_allocate_person(self, args):
        """Usage: allocate_person <person_id>"""
        person_id = args['<person_id>']
        msg = self.amity.allocate_person(person_id)
        if "!" not in msg:
            msg += '  ✔'
            msg = colored(msg, 'yellow', attrs=['bold', 'dark'])
            print(msg)
        else:
            msg = colored(msg, 'green', attrs=['bold', 'dark'])
            print(msg)

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_id> <new_room_name>"""
        person_id = args['<person_id>']
        room = args['<new_room_name>']
        msg = self.amity.reallocate_person(person_id, room)
        if "!" in msg:
            msg += '  ✘'
            msg = colored(msg, 'red', attrs=['bold', 'dark'])
            print(msg)
        else:
            msg += '  ✔'
            msg = colored(msg, 'green', attrs=['bold', 'dark'])
            print(msg)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        msg = self.amity.load_people('people')
        if "!" in msg:
            msg += '  ✘'
            msg = colored(msg, 'red', attrs=['bold', 'dark'])
            print(msg)
        else:
            msg += '  ✔'
            msg = colored(msg, 'green', attrs=['bold', 'dark'])
            print(msg)

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=filename.txt]"""
        if args['--o']:
            filename = args['--o']
            msg = self.amity.print_allocations(filename)
            if "!" in msg:
                msg += '  ✘'
                msg = colored(msg, 'red', attrs=['bold', 'dark'])
                print(msg)
            else:
                msg += '  ✔'
                msg = colored(msg, 'green', attrs=['bold', 'dark'])
                print(msg)
        else:
            msg = self.amity.print_allocations()
            if "!" in msg:
                msg += '  ✘'
                msg = colored(msg, 'red', attrs=['bold', 'dark'])
                print(msg)
            else:
                msg = colored(msg, 'yellow', attrs=['bold', 'dark'])
                print(msg)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=filename.txt]"""
        if args['--o']:
            filename = args['--o']
            msg = self.amity.print_unallocated(filename)
            if "!" in msg:
                msg += '  ✘'
                msg = colored(msg, 'red', attrs=['bold', 'dark'])
                print(msg)
            else:
                msg += '  ✔'
                msg = colored(msg, 'green', attrs=['bold', 'dark'])
                print(msg)
        else:
            msg = self.amity.print_unallocated()
            if "!" in msg:
                msg += '  ✘'
                msg = colored(msg, 'red', attrs=['bold', 'dark'])
                print(msg)
            else:
                msg = colored(msg, 'yellow', attrs=['bold', 'dark'])
                print(msg)

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        room_name = args['<room_name>']
        msg = self.amity.print_room(room_name)

        if "!" in msg:
            msg += '  ✘'
            msg = colored(msg, 'red', attrs=['bold', 'dark'])
            print(msg)
        else:
            msg += '  ✔'
            msg = colored(msg, 'yellow', attrs=['bold', 'dark'])
            print(msg)

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""
        db = args['--db']
        msg = self.amity.save_state(db)
        if "!" in msg:
            msg += '  ✘'
            msg = colored(msg, 'red', attrs=['bold', 'dark'])
            print(msg)
        else:
            msg += '  ✔'
            msg = colored(msg, 'green', attrs=['bold', 'dark'])
            print(msg)

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state [<sqlite_database>]"""
        db = args['<sqlite_database>']
        msg = self.amity.load_state(db)
        if "!" in msg:
            msg += '  ✘'
            msg = colored(msg, 'red', attrs=['bold', 'dark'])
            print(msg)
        else:
            msg = colored(msg, 'green', attrs=['bold', 'dark'])
            print(msg)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        os.system('clear')
        bye = Figlet(font='jazmine')
        delay_print('\n\n' + \
                colored(bye.renderText('Bye ...'), 'yellow', attrs=['bold']))
        exit()

if __name__ == '__main__':

    try:
        print(__doc__)
        ScreenOut().cmdloop()
    except KeyboardInterrupt:
        os.system('clear')
        font = Figlet(font='jazmine')
        delay_print('\n\n' + \
        colored(font.renderText('Bye ...'), 'yellow', attrs=['bold']))
