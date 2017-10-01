#!/usr/bin/env python3
import urllib.request
import bs4

import enum

url = "http://apps.cs.utexas.edu/unixlabstatus/"


class LabStatus(enum.Enum):
    """An enum for the status after running a test"""
    UP = 0
    """Implementation has passed the test"""
    DOWN = 1

    def __bool__(self):
        return self.value == LabStatus.UP.value

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
        self.load = 10000 if load == "" else float(load)

    def __str__(self):
        return "Host: {},\tStatus: {},\tUptime: {},\tNumber of users: {},\tLoad: {}".format(
            self.host, self.status, self.uptime, self.num_users, self.load)


def grab_all():
    global url
    with urllib.request.urlopen(url) as response:
        html = response.read()
    sitetree = bs4.BeautifulSoup(html, "html.parser")
    data = sitetree.table.find_all("tr")[3:]
    comp_status = [
        LabMachine(
            host=tr.select('td')[0].get_text(),
            status=tr.select('td')[1].get_text(),
            uptime=tr.select('td')[2].get_text(),
            num_users=tr.select('td')[3].get_text(),
            load=tr.select('td')[4].get_text()
        )
        for tr in data
    ]
    return comp_status


if __name__ == "__main__":
    print(*sorted(grab_all(), key=lambda x: x.load), sep="\n")
