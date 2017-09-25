#!/usr/bin/env python3
import urllib
import bs4

import enum

url = "http://apps.cs.utexas.edu/unixlabstatus/"


class LabStatus(enum.Enum):
    """An enum for the status after running a test"""
    PASS = 0
    """Implementation has passed the test"""
    FAIL = 1
    """Implementation has failed the test"""
    TOUT = 2
    """Implementation has timed out the test"""
    CERR = 3
    """The test has failed to compile with your implementation"""

    def __bool__(self):
        return self.value == Status.PASS.value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
        

class LabMachine:
	def __init__(self, host, status, uptime, num_users, load):
		self.host = host
		self.status = status
		self.uptime = uptime
		self.num_users = num_users
		self.load = load
	
	
def grab_all():
	global url
	with urllib.request.urlopen(url) as response:
		html = response.read()
	sitetree = bs4.BeautifulSoup(html, "lxml")
	prettytree = sitetree.prettify()
	data = sitetree.table.find_all("tr")[3:]
	comp_status = [LabMachine(host=tr[0].get_text(), status=tr[1].get_text(), uptime=tr[2].get_text(), num_users=tr[3].get_text(), load=tr[4].get_text()) for tr in data]
	
	return comp_status
	
if __name__ == "__main__":
	grab_all()
