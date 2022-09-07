import unittest

class StringCalculationSpec(unittest.TestCase):

    def test_return_0_for_empty_string(self):
        calculation("").the_result_is(0)

    def test_return_single_numbers(self):
        calculation("1").the_result_is(1)
        calculation("2").the_result_is(2)

    def test_numbers_separated_by_comma(self):
        calculation("1,2").the_result_is(3)
        calculation("2,2").the_result_is(4)

    def test_numbers_separated_by_newline(self):
        calculation("1\n1").the_result_is(2)

    def test_numbers_separated_by_custom_delimiter(self):
        calculation("//a\n1a2").the_result_is(3)
        calculation("//##hi##\n1##hi##2").the_result_is(3)

    def test_numbers_separated_by_different_delimiters(self):
        calculation("1,2\n3").the_result_is(6)

    def test_rejects_negative_numbers(self):
        calculation("-1,1").value_error_raised()

class calculation(object):

    def __init__(self, string):
        self.string = string

    def the_result_is(self, expected_result):
        actual_result = StringCalculation().add(self.string)
        if actual_result != expected_result:
            raise AssertionError("Expected \"%s\" to result in %s, but was %s" % (
                self.string, expected_result, actual_result))

    def value_error_raised(self):
        try:
            StringCalculation().add(self.string)
            raise AssertionError("Expected \"%s\" to result in ValueError" %
                self.string)
        except ValueError:
            pass

class StringCalculation(object):

    DELIMITER = ","

    def add(self, string):
        if string == "":
            return 0
        else:
            return self._add_numbers(string)

    def _add_numbers(self, string):
        return sum(self._extract_numbers_from(string))

    def _extract_numbers_from(self, string):
        return [self._parse_number(number) for number in self._split_on_delimiters(string)]

    def _parse_number(self, number):
        if "-" in number:
            raise ValueError("Rejecting negative number")
        return int(number)

    def _split_on_delimiters(self, string):
        return self._normalize_delimiters(string).split(self.DELIMITER)

    def _normalize_delimiters(self, string):
        normalized = string
        normalized = self._normalize_custom_delimiter(normalized)
        normalized = normalized.replace("\n", self.DELIMITER)
        return normalized

    def _normalize_custom_delimiter(self, string):
        if string.startswith("//"):
            custom, rest = string.split("\n", 1)
            return rest.replace(custom[2:], self.DELIMITER)
        return string

if __name__ == '__main__':
    unittest.main()