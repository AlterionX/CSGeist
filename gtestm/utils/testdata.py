import enum


class TestData:
    """
    A class for storing and updating the testing data
    """
    def __init__(self):
        self.tests = {}
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.timed_out = 0
        self.comp_failed = 0

    def update(self, file_hash: str, data: list):
        """
        Given the stdout of a make command, update the testing data.
        :param file_hash: A string representing the file name
        :param data: A list of all the lines that were sent to stdout
        :return: None
        """
        self.total += 1
        if "... pass ---" == data[0][-len("... pass ---"):len(data[0])]:
            self.tests[file_hash] = Status.PASS, data, fetch_flags(file_hash)
            self.passed += 1
        elif "----> timeout <----" == data[-1][-len("----> timeout <----"):len(data[-1])]:
            self.tests[file_hash] = Status.TOUT, data, fetch_flags(file_hash)
            self.timed_out += 1
        elif "... fail ---" == data[0][-len("... pass ---"):len(data[0])]:
            self.tests[file_hash] = Status.FAIL, data, fetch_flags(file_hash)
            self.failed += 1
        elif "failed" == data[-1][-len("failed"):len(data[-1])] and "Makefile:32: recipe for target " == data[-1][:len(
                "Makefile:32: recipe for target ")]:
            self.tests[file_hash] = Status.CERR, data, fetch_flags(file_hash)
            self.comp_failed += 1

    def __str__(self):
        print(
            "Total: {} Passed: {} Failed: {} Timed Out: {} Compilation with makefile failed: {}".format(
                self.total,
                self.passed,
                self.failed,
                self.timed_out,
                self.comp_failed
            )
        )


class Status(enum.Enum):
    """An enum for the status after running a test"""
    PASS = 0
    """Implementation has passed the test"""
    FAIL = 1
    """Implementation has failed the test"""
    TOUT = 2
    """Implementation has timed out the test"""
    CERR = 3
    """The test has failed to compile with your implementation"""


class Flags:
    """Flags set by users: potentially have networking here"""
    def __init__(self, invalid: bool = False):
        self.invalid = invalid


def fetch_flags(file_hash):
    """
    Retrieve remote or local flags or combine the two somehow.
    :param file_hash: The file name we are looking at
    :return: A Flags object
    """
    return Flags(False)
