import sys
import mypy
import re
import pickle


class Person:
    def __init__(self, data_last, data_first, data_mi, data_id, data_phone):
        self.last = data_last
        self.first = data_first
        self.mi = data_mi
        self.id = data_id
        self.phone = data_phone

    def display(self):
        """
        Format is:
            Employee id: ID
            First Mid Last
            Phone Number
        """
        return 'Employee id: ' + self.id + '\n' + '\t' + self.first + ' ' + self.mi + ' ' + self.last + \
            '\n' + '\t' + self.phone + '\n'


def process_input(file_input: str) -> str:
    """
    The function firstly type checks if the parameter is a string.
    The function RETURNS a dict of person(s)
    Meets all the expected criteria:
    * Name Capitalization, ID modification
    !!!BUT!!!!
    For phone number reformatting, I thought it would be best to automatically change the old formatting to the
    required one instead of having to manually request input every time as the Sample Run suggests.
    """

    input_list = []
    person_dict = {}

    with open(file_input, 'r') as file:
        inputs = file.read().splitlines()
    for line in inputs[1:]:
        temp_list = line.split(',')

        if not temp_list[0]:  # Last Name, Capitalization
            continue
        else:
            temp_list[0] = temp_list[0][0].upper() + temp_list[0][1:]
            if len(temp_list[0]) > 1:
                temp_list[0] = temp_list[0][0] + temp_list[0][1:].lower()

        if not temp_list[1]:  # First Name, Capitalization
            continue
        else:
            temp_list[1] = temp_list[1][0].upper() + temp_list[1][1:]
            if len(temp_list[1]) > 1:
                temp_list[1] = temp_list[1][0] + temp_list[1][1:].lower()

        if not temp_list[2]:  # Middle Name, Checking
            temp_list[2] = 'X'
        elif not (len(temp_list[2]) == 1 and temp_list[2][0].isupper()):
            temp_list[2] = temp_list[2][0].upper()

        while not re.fullmatch('[A-Z]{2}\d{4}', temp_list[3]):  # Handles the IDs
            print('ID invalid:', temp_list[3])
            print('ID is 2 letters followed by 4 digits')
            print('Please enter a valid id: ', end='')
            temp_list[3] = input()

        if re.fullmatch('\d{3}.?\d{3}.?\d{4}',
                        temp_list[4]):  # Checks to see if the phone number has the digits formatted correct
            if re.fullmatch('\d{3}-\d{3}-\d{4}', temp_list[4]):
                continue
            else:
                stored = re.search('(\d{3}).?(\d{3}).?(\d{4})',
                                   temp_list[4])  # If it doesn't then forces it into that format
                temp_list[4] = stored.group(1) + '-' + stored.group(2) + '-' + stored.group(
                    3)  # NOTE: group(0) is something else entirely
        else:  # If it doesn't even match THAT, then we force the user to manually input it
            while not re.fullmatch('\d{3}-\d{3}-\d{3}',
                                   temp_list[4]):
                print('Phone', temp_list[4], 'is invalid')
                print('Enter phone number in form 123-456-7890')
                print('Enter phone number: ', end='')
                temp_list[4] = input()
        input_list.append(temp_list)

    for list_item in input_list:  # Goes through the dict and checks for duplicates
        temp = Person(list_item[0], list_item[1], list_item[2], list_item[3], list_item[4])
        if list_item[3] in person_dict:
            print('ERROR!!! ID value ' + list_item[3] + ' is a duplicate!', end='')
            exit()
        person_dict[list_item[3]] = temp

    return person_dict


def main():
    """
    Makes sure there's some input in the command arguments and ASSUMES that's the file input
    Calls process_input and then does the pickling and unpickling for verification
    """
    if len(sys.argv) > 1:
        file_input = sys.argv[1]
    else:
        print('ERROR')
        return

    input_dict = process_input(file_input)
    pickle.dump(input_dict, open('dict.p', 'wb'))  # Saved the dict as a pickled file
    pickled_dict = pickle.load(open('dict.p', 'rb'))  # Reading the pickled file

    print('\n\nEmployee List:\n')
    for key in pickled_dict:
        print(pickled_dict[key].display())


if __name__ == "__main__":
    main()
