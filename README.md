A simple to use interface for running tests on the lab machines in conjunction with a public directory of tests.

See config file for details about how to change the configuration information.

Setup:

Ensure the python 3 version of paramiko is installed with the command "pip3 install paramiko"

Navigate to the root of the project.

Edit "config-sample" to match your own information and rename it "config".

Run the CLI using "./main.py -m cli".
Run the GUI using "./main.py -m gui".

Complete:
- Run/Display all test cases
- GUI/CLI interface for test running
- Sorting test cases by name and pass/fail state
- GUI/CLI dynamic login info request
- GUI/CLI parallellized testing
- Setup script
- Selective testing & batch running selected tests
- Test data replacement
- Run only latest tests
- Select all button

In progress:
- Settings dialog
- Improve select all button
- Flagging tests (invalid)
- Test result caching
- Better GUI
- ... and more
