""" This code is used to show PurpleAir quality information."""

import csv
from enum import Enum
filename = 'purple_air.csv'

class Stats(Enum):
    MIN = 0
    AVG = 1
    MAX = 2


class EmptyDataSetError(Exception):
    pass


class NoMatchingItems(Exception):
    pass


class DataSet:
    """This objected oriented class defines the method used for input of the
    header, which is displayed for the menu."""

    def __init__(self, header=""):
        self._data = None
        self.header = header
        self._zips = {}
        self._times = []

    def is_there_data(self):
        if self._data is None:
            return False
        else:
            return True

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, my_header: str):
        if len(my_header) <= 30:
            self._header = my_header
        else:
            raise ValueError

    def get_zips(self):
        copy_zips = self._zips.copy()
        return copy_zips

    def display_cross_table(self, stat: Stats):
        if not self._data:
            print('Please load some data.')
            return
        print('          ', end="")
        for time_of_day in self._times:
            print(f'{time_of_day:>10}', end="")
        print()
        for zip_code in self._zips.keys():
            # if zip_code == True in self._zips:
            if self._zips[zip_code]:
                print(f'{zip_code:10}', end="")
                for time_of_day in self._times:
                    try:
                        my_stat = self._cross_table_statistics (zip_code, time_of_day)[stat.value]
                        # I don't know why it keeps getting mad at me for this
                        # indentation, I keep reverting it, and then it forces
                        # me to revert it.
                        print(f'{my_stat:>10.2f}', end="")
                    except NoMatchingItems:
                        print(f"{'N/A':>10}", end="")
            else:
                continue
            print()

    def _cross_table_statistics(self, zip_code: str,
                                time_of_day: str):
        if not self._data:
            raise EmptyDataSetError
        concentration_list = [float(item[2]) for item in self._data if item[0]
                              == zip_code and
                              item[1] == time_of_day]
        if len(concentration_list) == 0:
            raise NoMatchingItems
        return (min(concentration_list), sum(concentration_list) /
                len(concentration_list), max(concentration_list))

    def _initialize_labels(self):
        temp_zip_code = set()
        temp_time_of_day = set()
        for item in self._data:
            temp_zip_code.add(item[0])
            temp_time_of_day.add(item[1])
        self._zips = {}
        for item in self._data:
            self._zips[item[0]] = True
        self._times = list(temp_time_of_day)
        self._times.sort(reverse=True)

    def load_default_data(self):
        self._data = [('12345', 'Morning', 1.1),
                      ('94022', 'Morning', 2.2),
                      ('94040', 'Morning', 3.0),
                      ('94022', 'Midday', 1.0),
                      ('94040', 'Morning', 1.0),
                      ('94022', 'Evening', 3.2)]
        self._initialize_labels()

    def toggle_zip(self, target_zip=str):
        if target_zip not in self._zips:
            raise LookupError
        else:
            if self._zips[target_zip]:
                self._zips[target_zip] = False
            else:
                self._zips[target_zip] = True

    def load_file(self):
        with open(filename, newline = '') as file:
            csv.reader(file)
            data = [(data[1],data[4],data[5])for data in csv.reader(file)][1:]
            print(f"{len(data)} lines of data were downloaded")
            self._data = list(set(data))
            self._initialize_labels()


def manage_filters(my_dataset: DataSet):
    if my_dataset.is_there_data() is False:
        print('Please enter some data.')
        return
    my_zips = my_dataset.get_zips()
    print()
    print('The following labels are in the dataset:')
    my_zips_list = []
    for num, zip_code in enumerate(my_zips, 1):
        my_zips_list.append(zip_code)
        print(f"{num}: {zip_code}      ", end='')
        print(f"{'Active' if my_zips[zip_code] else 'Inactive'}")
    user_input = input('Please select an item to toggle or press '
                       'enter/return when you are finished. ')
    my_len = len(user_input)
    if my_len == 0:
        return
    try:
        i_user = int(user_input)
        my_dataset.toggle_zip(my_zips_list[i_user - 1])
        manage_filters(my_dataset)
    except ValueError:
        print(f'Please enter a valid number between 1 and '
              f'{len(my_zips_list)}.')
        manage_filters(my_dataset)


def print_menu():
    """ Prints the main menu. """
    print('Main Menu')
    print('1 - Print Average Particulate Concentration by Zip Code and '
          'Time')
    print('2 - Print Minimum Particulate Concentration by Zip Code and '
          'Time')
    print('3 - Print Maximum Particulate Concentration by Zip Code and '
          'Time')
    print('4 - Adjust Zip Code Filters')
    print('5 - Load Data')
    print('9 - Quit')


def menu(my_dataset: DataSet):
    """ Enters a loop until 9 is inputted while also displaying the
    main menu each time. A numeric number within 1-5 will not be allowed for
    now, and a non-numeric option will ask for a numeric one. It also prints
    the dataset, or the header.
    """
    while True:
        print()
        print(my_dataset.header)
        print_menu()
        choice = input('What is your choice? ')
        try:
            int(choice)
        except ValueError:
            print('Please enter a number.')
            continue
        if choice == '9':
            break
        elif choice == '1':
            my_dataset.display_cross_table(Stats.AVG)
        elif choice == '2':
            my_dataset.display_cross_table(Stats.MIN)
        elif choice == '3':
            my_dataset.display_cross_table(Stats.MAX)
        elif choice == '4':
            manage_filters(my_dataset)
        elif choice == '5':
            my_dataset.load_file()
        else:
            print('Please enter a valid number.')
    print('Thank you for using the database! Goodbye.')


def main():
    """ Asks for the user's name and displays it. This function also goes
    through dataset class, which displays the header for the menu, along with
    the recurring loop for the menu. """
    user_name = input('Please enter your name: ')
    print(f"Hello {user_name}, welcome to the Air Quality Database.",
          sep='')
    purple_air = DataSet()
    while True:
        try:
            user_header = input('Enter a header for the menu: ')
            purple_air.header = user_header
            break
        except ValueError:
            print('The header is too long; it has to be 30 characters'
                  ' or less.')
    menu(purple_air)


if __name__ == '__main__':
    main()
