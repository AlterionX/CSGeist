A simple to use interface for running tests on the lab machines in conjunction with a public directory of tests.

See config file for details about how to change the configuration information.

Setup:

Navigate to the root of the project.

Ensure the python 3 version of paramiko is installed with the command "pip3 install paramiko"

Edit "config-sample" to match your own information and rename it as "config".

Run the CLI using "./gtestm/main.py -m cli".
Run the GUI using "./gtestm/main.py -m gui".

If you have bash, there are three scripts in the root directory.

Complete:
- Run/Display all test cases
- GUI/CLI interface for test running
- Sorting test cases by name and pass/fail state
- GUI/CLI dynamic login info request
- GUI/CLI parallellized testing

In progress:
- Selective testing & test data replacement
- Flagging tests (invalid)
- Batch running selected tests
- Test result caching
- Duplicate test detection
- Possible related test detection
- Better GUI
- ... and more
