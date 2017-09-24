A simple to use interface for running tests on the lab machines in conjunction with Gheith's testing system.

See config file for details about how to change the configuration information.

Setup:

Navigate to the root of the project.

Ensure the python 3 version of paramiko is installed with the command "pip3 install paramiko"

Edit "config-sample" to match your own information and rename it as "config".

Run the CLI using "python3 -m gtestm.modes.run".
Run the GUI using "python3 -m gtestm.gui.gui_util".

Complete:
- Run all test cases
- Display test data
- GUI interface for test running
- CLI script for test running
- GUI/CLI dynamic login info request

In progress:
- Parallellized testing
- Sorting test cases by name and pass/fail state
- Selective testing & test data replacement
- Flagging tests (invalid)
- Batch running selected tests
- Better GUI
- Test result caching
- Duplicate test detection
- Possible related test detection
- ... and more
