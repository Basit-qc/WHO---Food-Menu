__author__ = 'zahidirfan'

import unittest
from unittest import TestCase
from buildmenu import BuildMenu
from contextlib import contextmanager


@contextmanager
def mock_raw_input(mock):
    original_raw_input = __builtins__.raw_input
    __builtins__.raw_input = lambda _: mock
    yield
    __builtins__.raw_input = original_raw_input


class TestBuildMenu(TestCase):
    """
        Build Menu Test Suite
    """

    menu = BuildMenu()

    def test_getting_input_main_menu(self):
        """
        Input to main Menu
        :return:
        """
        print "Getting input from the user"
        with mock_raw_input("1"):
            self.assertEqual(self.menu.main_menu(), "1")

        print "Main Menu Entered"

    def test_getting_input(self):
        """
        Takes the input from the user
        :return:
        """
        print "Getting input from the user"
        with mock_raw_input("berries"):
            self.assertEqual(self.menu.get_user_input(), "berries")

        print "Found Item"

    def test_find_food(self):
        """
        This finds the value that has been entered.

        :return:
        """

        self.menu.read_csv('WHFoods CSV For Zahid.csv')

        results = self.menu.build_menu_from_input("berries")
        # Ensuring that result is equal to one "BlackBerries" is a record found in the file

        self.assertEqual(results.len, 1, "The records are not found there must be some problem")

    def test_add_data(self):
        self.fail("If not written yet")


if __name__ == '__main__':
    unittest.main()