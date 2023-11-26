import unittest
import difflib


# assertEqualWithDiff adapted from https://stackoverflow.com/questions/25512531/assertequal-only-shows-differences

class MyTestCase(unittest.TestCase):

    def __assertEqualWithDiff(self, left, right, msg=None):
        diff = difflib.unified_diff(
            left.splitlines(True),
            right.splitlines(True),
            n=0
        )
        diff = ''.join(diff)
        if diff:
            raise self.failureException("\n" + diff)

    def __test_compare_expected_with_generated(self, file_prefix: str):
        hack_code = ""
        with open(file_prefix + ".hack", "r") as hack_file:
            for line in hack_file:
                hack_code += line

        comp_code = ""
        with open(file_prefix + ".comp.hack", "r") as comp_file:
            for line in comp_file:
                comp_code += line

        self.__assertEqualWithDiff(hack_code, comp_code)

    def test_add(self):
        self.__test_compare_expected_with_generated("projects/06/add/Add")

    def test_maxL(self):
        self.__test_compare_expected_with_generated("projects/06/max/MaxL")

    def test_rectL(self):
        self.__test_compare_expected_with_generated("projects/06/rect/RectL")

    def test_pongL(self):
        self.__test_compare_expected_with_generated("projects/06/pong/PongL")

    def test_max(self):
        self.__test_compare_expected_with_generated("projects/06/max/Max")

    def test_rect(self):
        self.__test_compare_expected_with_generated("projects/06/rect/Rect")

    def test_pong(self):
        self.__test_compare_expected_with_generated("projects/06/pong/Pong")


if __name__ == "__main__":
    unittest.main()
