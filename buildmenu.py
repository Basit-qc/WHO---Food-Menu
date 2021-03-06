from pandas.core.frame import DataFrame
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter


__author__ = 'zahidirfan'

import pandas as pd


class BuildMenu():
    """
        This Class Builds the Menu as per CSV file
    """

    def __init__(self):
        self.menu = list()
        self.cols = list()
        self.file_menu = 'Menu.csv'
        # self.file_database = 'WHFoods CSV For Zahid.csv'
        self.file_database = 'converted_values.csv'
        self.file_recommended_values = 'WHO Daily Recommended Values.rtf'
        self.tmp_file = 'tmp.csv'
        self.file_converted_values = 'converted_values.csv'
        self.indexes = [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                        30, 31, 33, 40, 41, 43, 47]
        self.target_values = dict()
        # clears the Menu First
        df = DataFrame(data=None, columns=None)
        df.to_csv(self.file_menu, index=False)
        df.to_csv(self.tmp_file, index=False)

    def get_user_input(self):
        """
        Input to the main menu is entered here
        :return:
        """
        user_input = raw_input("Please enter the food to search: ")
        return user_input

    def read_csv(self, file_name):
        """
        This function reads the csv file using pandas
        :param file_name:
        :return:
        """
        food_data = pd.read_csv(file_name)
        return food_data

    def main_menu(self):
        """
        This is the Main Menu Shown to the user at start
        :return:
        """
        input_option = raw_input(
            "Press - 1 - to input a food name\n"
            "Press - 2 - to run function\n"
            "Press - 3 - to abort\n"
            "Please enter your choice>> ")
        while input_option:
            if input_option not in ['', ' ', '\n']:
                return input_option
            else:
                print 'Not Valid input'
                input_option = raw_input("Please choose from\n"
                                         "Press - 1 - to input a food name\n"
                                         "Press - 2 - to run function\n"
                                         "Press - 3 - to abort\n"
                                         "Please enter your choice>> ")
            return input_option

    def start_up(self, user_object):
        """
        Application starts from here
        It Takes input fro User and process it accordingly
        :param user_object:
        :return:
        """
        try_again = ''
        exit_code = False
        main_input = self.main_menu()
        while main_input != '':
            while try_again != '':
                if try_again.lower() == 'yes':
                    main_input = self.main_menu()
                    break
                elif try_again.lower() == 'no':
                    print 'Good Bye From Main Menu'
                    exit_code = True
                    break
                elif try_again != '':
                    print 'This is NOT a valid option'
                    try_again = raw_input("Do you want to try/start again? (yes/no) ")
            if exit_code:
                break
            if main_input == '1':
                user_object.build_menu_from_input()
            elif main_input == '2':
                user_object.build_menu_from_function()
            elif main_input == '3':
                print 'Good Bye From Main Menu'
                break
            else:
                print 'This is NOT a valid option'
            try_again = raw_input("Do you want to try/start again? (yes/no) ")

    def build_menu_from_input(self):
        """
        This function builds the menu by asking the user what should be added
        :return:
        """
        index = 1
        filtered_foods = list()
        data_in = self.get_user_input()
        # Searches for valid input
        if data_in not in ['', ' ', '\n']:
            data_food = self.read_csv(self.file_database)
            # Searches valid input inside Database
            for food_name in data_food['Food_Name']:
                if data_in.lower() in str(food_name).lower():
                    filtered_foods.append(food_name)
            # If item found, builds the Menu
            if filtered_foods:
                # gets confirmation for item to be added
                item_for_menu = self.selected_item(index, filtered_foods)
                if item_for_menu != '':
                    # finds columns of Menu and item to be added in Menu
                    item = self.build_col_item(data_food, item_for_menu)
                    if len(item) != 0:
                        print self.update_menu(item)
                        self.calculate_last_row()
                        print 'Selected Item has been added and Menu has been exported to CSV'
                        want_menu = raw_input('Do you want to see the Menu? (yes/no) ')
                        if want_menu == 'yes':
                            print 'Menu is:'
                            self.print_menu(self.file_menu)
                        else:
                            print 'Menu will not be shown'
                    else:
                        print 'NO item to be added'
                else:
                    pass
            else:
                print 'No Result Found'
        else:
            print 'Not a valid input'

    def calculate_last_row(self):
        """
        This calculates the last row which shows Ratio of Sum of col to Target value
        :return:
        """
        main_index = self.indexes
        row = list()
        updated_row = [''] * 50
        file_to_process = self.file_menu
        target, filtered_col = self.read_recommendations(self.file_recommended_values)
        nutrient_list = self.nutrients_list(file_to_process, filtered_col, main_index)
        updated_row[0] = 'Ratio'
        updated_row[1] = '(Sum of column(s)/Target value)x 100'
        for column in filtered_col:
            ratios = 0
            formula = ''
            for dest in nutrient_list:
                if column == dest['nutrient']:
                    ratios += float(dest['value'])
                formula = ratios / float(target[column]) * 100
                formula = round(formula, 2)
            row.append(str(formula)+'%')
        sub_index = 0
        for index in main_index:
            updated_row[index] = row[sub_index]
            sub_index += 1
        data = self.read_csv(file_to_process)
        after_last_row = self.build_col_item(data, updated_row)
        self.update_menu(after_last_row)

    def build_col_item(self, data, item_for_menu):
        """
        This function generates the columns name and Items for the Menu
        :param data:
        :param item_for_menu:
        :return:
        """
        menu = self.menu
        for foods in menu:
            if 'Ratio' in foods:
                menu.pop()
                self.menu = menu
        if len(self.cols) == 0:
            for col_name in list(data._info_axis._data):
                self.cols.append(col_name)
        for item in data.values:
            if item_for_menu in item:
                menu.append(list(item))
                break
            elif 'Ratio' in item_for_menu:
                menu.append(item_for_menu)
                break
        return menu

    def print_menu(self, file_name):
        """
        Shows the menu
        :param file_name:
        :return:
        """
        from_csv = self.read_csv(file_name)
        print from_csv.head()

    def build_menu_from_function(self):
        """
        This function Updates the Menu on the basis of Foods already present in the item
        :return:
        """
        if len(self.menu) != 0:
            file_menu = self.file_menu
            file_database = self.file_converted_values
            file_recommended_values = self.file_recommended_values
            results = self.read_recommendations(file_recommended_values)
            target = results[0]
            filtered_col = results[1]
            largest = self.largest_in_menu(file_menu, target, filtered_col, self.indexes)
            print 'Item with largest value of Quantity:Target ratio in MENU is\n' + str(largest)
            raw_input("Press 'Enter key' to continue >> ")
            lowest = self.lowest_in_database(file_database, target, filtered_col, self.indexes, largest)
            self.validate_multiple_foods(file_database, target, filtered_col, largest, lowest)
        else:
            print 'Menu is Empty, Please provide an initial starting point'

    def validate_multiple_foods(self, file_database, target, filtered_col, largest, lowest):
        not_added = list()
        if lowest:
            # finding suitable foods from database:
            success, current_food_element, index = self.to_remove_food_items(file_database, filtered_col, target,
                                                                             lowest)
            while index != '':
                if success:
                    print 'Results:    Tolerance Rule Satisfied for: ' + str(current_food_element)
                    self.calculate_last_row()
                    print '            New Food has been added to the Menu'
                    print '            You can see the Updated Menu in Menu.csv file'
                elif not success:
                    not_added.append(current_food_element)
                lowest.pop(index)
                success, current_food_element, index = self.to_remove_food_items(file_database, filtered_col,
                                                                                 target, lowest)
            user_choice = raw_input('Do you want to see Food Items that failed the Tolerance rule?(yes/no) ')
            if user_choice == 'yes':
                for food in not_added:
                    print 'Results: Tolerance Rule Violated for: ' + str(food)

    def to_remove_food_items(self, file_database, filtered_col, target, lowest):
        """
        Picks an item randomly from searched results and check for validity
        :param file_database:
        :param filtered_col:
        :param target:
        :param lowest:
        :return:
        """
        import random

        if len(lowest) == 1:
            random_index = 0
        elif len(lowest) == 0:
            success = False
            return success, '', ''
        else:
            random_index = random.randint(0, len(lowest) - 1)
        required_food = lowest[random_index]
        # print 'Item with lowest value of Quantity:Target ratio in Database is\n' + str(required_food)
        # print 'Checking for Tolerance Rule'
        new_data_for_menu = self.item_to_add_in_menu(file_database, required_food['food_name'])
        success = self.check_tolerance(new_data_for_menu, filtered_col, target)
        if not success:
            new_data_for_menu.pop()
        return success, required_food['food_name'], random_index

    def check_tolerance(self, new_data_for_menu, filtered_col, target):
        """
        This function makes a temporary file tmp.csv to check for the valid Menu
        :param new_data_for_menu:
        :param filtered_col:
        :param target:
        :return:
        """
        success = False
        df = DataFrame(data=new_data_for_menu, columns=self.cols)
        df.to_csv(self.tmp_file, index=False)
        intermediate_data = self.nutrients_list(self.tmp_file, filtered_col, self.indexes)
        indicator = self.calc_tolerance(intermediate_data, target, filtered_col)
        if not indicator:
            tmp_data = self.read_csv(self.tmp_file)
            df = DataFrame(data=tmp_data, columns=self.cols)
            df.to_csv(self.file_menu, index=False)
            success = True
        else:
            tmp_data = self.read_csv(self.file_menu)
            df = DataFrame(data=tmp_data, columns=self.cols)
            df.to_csv(self.tmp_file, index=False)
            # print 'New Item does not satisfy the Tolerance Rule'
        return success

    def calc_tolerance(self, nutrient_list, target, filtered_col):
        """
        This function validates the new food according to 110% rule.
        Which says if adding new food does not make any nutrient sum to over 110%
            add the food
            otherwise remove it and try another
        :param nutrient_list:
        :param target:
        :param filtered_col:
        :return:
        """
        formula = ''
        error = False
        for column in filtered_col:
            ratios = 0
            for dest in nutrient_list:
                if column == dest['nutrient']:
                    ratios += float(dest['value'])
                    formula = ratios / float(target[column]) * 100
                    if formula > 110:
                        error = True
                        break
            if error:
                break
        return error

    def update_menu(self, food):
        """
        Updates the Menu using Pandas
        :param file_name:
        :param food:
        :param cols:
        :return:
        """
        df = DataFrame(data=food, columns=self.cols)
        df.to_csv(self.file_menu, index=False)
        return 'New Food has been added to the MENU'

    def item_to_add_in_menu(self, file_database, name):
        menu = list()
        database = self.read_csv(file_database)
        for food_item in database.values:
            if name.lower() in str(food_item).lower():
                menu = self.build_col_item(database, food_item[1])
                break
        return menu

    def largest_in_menu(self, file_menu, target, filtered_col, indexes):
        """
        Assuming Menu is filled,
        This returns the nutrient having highest quantity:target ratio
        :param file_menu:
        :param target:
        :param filtered_col:
        :param indexes:
        :return:
        """
        nutrients_menu = self.nutrients_list(file_menu, filtered_col, indexes)
        ratios_menu = self.calc_ratio(nutrients_menu, target)
        largest = self.pick_largest_lowest(ratios_menu, flag='high')
        return largest

    def lowest_in_database(self, file_database, target, filtered_col, indexes, largest):
        """
        This returns the nutrient having lowest quantity:target ratio in whole database
        :param file_database:
        :param target:
        :param filtered_col:
        :param indexes:
        :param largest:
        :return:
        """
        filtered_foods = list()
        nutrients_all = self.nutrients_list(file_database, filtered_col, indexes)
        if len(nutrients_all) != 0:
            ratios_all = self.calc_ratio(nutrients_all, target)
            for filtered_ratio in ratios_all:
                if largest['nutrient'] == filtered_ratio['nutrient']:
                    filtered_foods.append(filtered_ratio)
            lowest = self.pick_largest_lowest(filtered_foods, flag='low', largest=largest['ratio'])
        else:
            return 'Menu is Empty'
        return lowest

    def read_recommendations(self, file_name):
        """
        Function reads the targeted values from the file "WHO Daily Recommended Values.rtf"
        It process the entries and creates a dictionary with
        Nutrient name as Key and Nutrient Value as value
        :param file_name:
        :return:
        """
        target = dict()
        filtered_col = list()
        doc = Rtf15Reader.read(open(file_name))
        entities = PlaintextWriter.write(doc).getvalue().split('\n\n')
        for item in entities:
            splited = item.split(',')
            name = splited[0].split('(')[0]
            value = splited[1]
            try:
                unit = splited[0].split('(')[1].split(')')[0]
            except:
                unit = ''
            # target.append({'nutrient': name,
            # 'unit': unit,
            # 'value': value})
            target.update({name: value})
            filtered_col.append(name)
        self.target_values = target
        return target, filtered_col

    def calc_ratio(self, nutrient_list, target):
        """
        For all the nutrients present in the Menu, this function perform the division of
        individual nutrient's converted value with targeted value
        :param nutrient_list:
        :param target:
        :return:
        """
        ratios = list()
        for dest in nutrient_list:
            ratio = float(dest['value']) / float(target[dest['nutrient']])
            ratios.append({'food_name': dest['name'],
                           'nutrient': dest['nutrient'],
                           'ratio': ratio})
        return ratios

    def pick_largest_lowest(self, ratios_data, flag='', largest=''):
        """
        This Function calculates the largest/lowest value from input value depending on flag value
        if flag is high - Gives largest value
        if flag is low - Gives lowest value
        :param ratios_data:
        :param flag:
        :return:
        """
        val = list()
        same_results = list()
        for item in ratios_data:
            val.append(item['ratio'])
        if flag == 'high':
            for item in ratios_data:
                if item['ratio'] == sorted(val)[-1]:
                    return item
        elif flag == 'low':
            # for item in ratios_data:
            # if item['ratio'] == sorted(val)[0]:
            # same_results.append(item)
            for item in ratios_data:
                if item['ratio'] / largest < 0.1:
                    same_results.append(item)
            return same_results

    def nutrients_list(self, file_name, filtered_col, indexes):
        """
        Here is the formula implemented for actual values of the nutrients
        i.e. Value multiply by Grams per serving and divided by 100
        :param file_name:
        :param filtered_col:
        :param indexes:
        :return:
        """
        nutrients = list()
        from_csv = self.read_csv(file_name)
        menu = from_csv.values
        # for foods in menu:
        #     if 'Ratio' in foods:
        #         menu.pop()
        #         self.menu = menu
        for item in menu:
            index = 0
            for column in filtered_col:
                if 'Ratio' not in item:
                    item_index = indexes[index]
                    nutrients.append({'name': item[1],
                                      'nutrient': column,
                                      'value': item[item_index]
                    })
                    index += 1
        return nutrients

    def selected_item(self, index, filtered_foods):
        """
        Gets confirmation form the User for item to be added in the Menu
        :param index:
        :param filtered_foods:
        :return:
        """
        selected_item = ''
        print 'Available Choices are:'
        for item in filtered_foods:
            print str(index) + '-' + ' ' + str(item)
            index += 1
        item_num = raw_input("Please Choose item number from the list to add in Menu: ")
        while item_num:
            try:
                if int(item_num) > 0:
                    selected_item = filtered_foods[int(item_num) - 1]
                else:
                    selected_item = filtered_foods[item_num]
                print 'Selected item is ' + str(selected_item)
                confirm = self.get_confirmation()
                if confirm != 'confirm':
                    selected_item = ''
                break
            except:
                print 'You did not choose a valid item.\nPlease Choose item number from the list:'
                item_num = raw_input("Do you want to see the list again? (yes/no): ")
                if item_num == 'yes':
                    print 'Available Choices are:'
                    index = 1
                    for item in filtered_foods:
                        print str(index) + '-' + ' ' + str(item)
                        index += 1
                    item_num = raw_input("Please Choose item number from the list to add in Menu: ")
                elif selected_item == ' no':
                    break
                else:
                    print "Invalid option"
                    item_num = raw_input("Do you want to see the list again? (yes/no): ")
        return selected_item

    def get_confirmation(self):
        """
        This function asks from the user whether the selection of food is correct or not
        :return:
        """
        confirmation = raw_input("Please confirm to add in Menu!\n"
                                 "1- Confirmed   2- Not Confirmed ")
        while confirmation:
            if confirmation == '1':
                print 'Selected Item will be added to the menu'
                confirmation = 'confirm'
                break
            elif confirmation == '2':
                print 'Selected Item will not be added'
                confirmation = 'not_confirm'
                break
            else:
                print "Invalid option"
                confirmation = raw_input("Please choose from\n"
                                         "1-Confirmed   2-Not Confirmed ")
        return confirmation

    def export_converted_values(self):
        """
        This function is called initially to convert per-100g values to per serving values
        Once this function is invoked, new file is generated which serves as Database
        This function will need to be called only one time
        :return:
        """
        file_converted = self.file_converted_values
        data_file = self.file_database
        data = self.read_csv(data_file)
        converted_data = list()
        for item in data.values:
            converted_list = list(item[0:2])
            sub_item = item[2:50]
            for nutrient in sub_item:
                import math

                if math.isnan(nutrient):
                    nutrient = 0
                converted_list.append(nutrient * sub_item[47] / 100)
            converted_list.append(item[50])
            converted_data.append(converted_list)
        if len(self.cols) == 0:
            for col_name in list(data._info_axis._data):
                self.cols.append(col_name)
        df = DataFrame(data=converted_data, columns=self.cols)
        df.to_csv(file_converted, index=False)
        print 'File has been exported'

user = BuildMenu()
user.start_up(user)

# uncomment the following if need to convert values first. In this case, file has already been generated
# user.export_converted_values()



