#!/usr/bin/python3
"""
Example of task for the golf server.
This module has two functions,
first function generates arguments for submited program
second function generates a string to compare STDOUT from submited code

If you're still stuck, maybe pseudocode would be better for you:

>>> arguments = make_arguments()
>>> for argv in arguments:
>>>     result = do_it(argv)
>>>     stdout = execute_submited_code(argv)
>>>     assert result == stdout

This code is a standalone script too 
you can put in golf server or execute in the terminal

for more rules please read the howto.html file
"""


def make_arguments():
    """
        this function generate arguments (argv) to submited program 
        each record is a list with strings
        and will be executed by do_it function and submited code

        :return: List of arguments for argv
        :rtype: List[List[str]]
    """
    return [
        ['Join our team <3'],
        ['The cake is a lie'],
        ['I like trains'],
    ]


def do_it(*argv):
    """
        this function execute arguments (from make_arguments)
        and returns string who will be compared with 
        stdout from submited code

        :param argv: list of stringed arguments (argv)
        :type argv: List[str]
        :return: result to compare with 
        :rtype: str
    """
    first_line = 'Clearcode @ SpreadIT 2019: ' + argv[0]
    return first_line + '\n' + '=' * len(first_line) + '\n'


def validate_code(code):
    """
        this function validate and transform code
        from textarea input (a player's code).
        This function must returns code (modified or not)
        or raise ValueError exception

        :param code: executable code
        :type code: str
        :return: executable code
        :rtype: str
    """
    if any(char.isdigit() for char in code):
        raise ValueError('the code cannot contain digits')
    return code


if __name__ == "__main__":
    from sys import argv, stdout
    if len(argv) != 4:
        print('usage:', __file__, 'COUNT', 'CHAR')
        exit(-1)
    result = do_it(*argv[1:])
    stdout.write(result)
