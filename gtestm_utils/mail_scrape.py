#!/usr/bin/env python3


class EmailInfo:
    def __init__(self, tests, assignment):
        self.tests = []
        self.fails = []
        for test in tests:
            self.tests.append(test[0])
            if test[1] == "fail":
                self.fails.append(test[0])
        data = assignment
        print(len(data))
        data = data[0].strip().split('/')
        data = data[-1].split('_')
        self.assignment = data[2][1:]
        self.classname = data[0][2:]
        self.semester = data[1]


def scrape(email):
    print("Scraping:", email)
    return EmailInfo(
        map(
            lambda test_line: test_line[3: -3].strip().split(" "),
            filter(
                lambda email_line: email_line[0:3] == "---",
                email
            )
        ),
        list(filter(
            lambda email_line: email_line[0:3] == "***",
            email
        ))
    )


if __name__ == "__main__":
    hi = """********* tests in ~gheith/public/cs439h_f17_p2
--- 01fe179233bc7ebfa55002668f23eb3d60ed0940 pass ---
--- 06cab6755047830d48f632190204262c1c2ae2a9 pass ---
--- 0917cf7ae0c64276b4798c54a98d8d78ed37233a pass ---
--- 0aa457d877a4a1f8dc209f51914dbe4fb00c87ef pass ---
--- 151a722ed332cae1e28590cdc1cf6226cb0b8878 fail ---
--- 16d4ce34a9cf6708a900c15088d7502a65e9ff9f pass ---
--- 1cd077e9bb5da926f34739a7e508d360842c0d3d pass ---
--- 1d6014648feb7130c831faaee4a6845ba31c1536 pass ---
--- 29ddeb5baa0cf77cf0845a9071b3fd5b87bac8e6 pass ---
--- 35b5a78317fe8b78cde643c79ba943a05a74d77b pass ---
--- 3bb10e023107339d74835238ba2ee5203d63b221 pass ---
--- 3bcd3659de0a23e217b859854e4e9c49bc219292 pass ---
--- 3ffc9c846a8d49b9f57b7a8805928bffb725fa77 pass ---
--- 40670a2827418ae34ff335b48c0a1f7c19218f83 pass ---
--- 42dbd84ef19483aaaceafe9ecf8b57e1baf48a23 pass ---
--- 49f09ad76f3a4ec20a239f855686209efe2e7590 pass ---
--- 4ee7850d5ace54085167ee7018327c0faa8d2f82 fail ---
--- 58db7033792f94ca0f12223f50dd06f9a732aad3 fail ---
--- 5be9c649e83a0d2ba5ae1d5640ec76c60ae7d1fa pass ---
--- 68e4380fa993f40bf1ab350fc958c88835d54ca5 pass ---
--- 7361072ae903acd0eabdad93064dcb1e1bf1703d pass ---
--- 7b37c77c565256162f6c56fc7e71e1bfe5d86c1d fail ---
--- 7ecd205562057e3ccc1d36853db066b194222e45 pass ---
--- 7f3dc96876e06150462f89e58af538f1c09647cc fail ---
--- 84f2e72fa9622ef86135b2368cdcb732c0a1a6f9 fail ---
--- 859a734d8690174d32b8546b8d7d696173854d3b pass ---
--- 88206cd83b53b881d15f701e886536bb938ceef4 fail ---
--- 8dfa7500250025b18f0a62b8fbd907343b7d318a pass ---
--- 99bdd7aa13096bc256b96c1d6ceb459abe461b24 fail ---
--- a2fdb1d10ab06a23d063db42421d4b898f1db74c fail ---
../common.mak:17: recipe for target 'kernel.o' failed
--- a36a74f44dafdd81cd929ec3f3e5ff4e519509d4 fail ---
--- a5db1ea243c82c31e4a5edeae7ae330e1be9fbae pass ---
--- b1a0e2c318a891e04bbc62848812d1903b077195 pass ---
--- b52b1f690b7093154f2568954c33b37194c51fa2 fail ---
--- b914ae811294dd57630b15b3d56e81d0aa521695 fail ---
--- c3516fc131d8aa3636d491f1801aea8f150255a5 fail ---
--- c3fb4676e23f7aee1b93672b60c6bc6456522bed pass ---
--- d63fb7f23f7ccc24b87cb6b7551a813bcd4e45f4 pass ---
--- dec548ea12b83b56d3f830fef3e3250c1fd00929 pass ---
--- e19da6329b2ddfe61bf71b7758ee0a2c035b3824 pass ---
--- e4321b576d65426a3743ba82f8d67daf589ac20c fail ---
--- e7a269a1cd52ddfb1693c79da94f6f7b1d617819 pass ---
--- ee1af3c33c25103af23cdadc2ea392c5d8f36d63 fail ---
--- f5b12120a68d3426229e28fbd2fdcd9c02739082 pass ---
--- f75840b89a03899955bc757cc1b4654d12da7e4a pass ---
--- fada1ed5cafa9c752c0094b5c844e27dbe7c56a9 pass ---
--- fbf5612be8f2ccea3eedcf2b7e869b6f65d613b3 pass ---
--- fca03702910b578a430570b3c7b9a29eb6ad1f54 pass ---
--- fe6242b91089fb07922a2f57b043bde810ba90c5 fail ---
--- t0 pass ---
--- t1 pass ---
Describe your allocation strategy (first-fit, best-fit, worst-fit, ...)

Semi-best first fit.

Categorize blocks of memory by a range of sizes, allocating for each.

- Why did you pick this strategy?

effectively O(1) insertion

- Describe a scenario in which best-fit will do better than first-fit

When there are other blocks with exactly the right amount of memory, but first fit consistently finds the largest block.

- Describe a scenario in which worst-fit will do better than best-fit

If there are many consistently sized allocation along with several smaller blocks being allocated.

The consistently sized allocations will be in the same places, while the leftover space is used for the smaller blocks.

In best fit, the small sized allocations will start filling up the places where there used to be a consistently sized allocation, fragmenting the heap more and more
commit 06cab6755047830d48f632190204262c1c2ae2a9
Author: Benjamin Xu <benxu@cs.utexas.edu>
Date:   Thu Sep 14 23:13:34 2017 -0500

    Report and test. dinner was nice

commit 8d899af63a30506b53a4df4bba5019aa2a2c7882
Author: Benjamin Xu <benxu@cs.utexas.edu>
Date:   Thu Sep 14 18:49:03 2017 -0500

    possibly working

commit f24f9f269b4de7b40528a7b7a62aaebb38810746
Author: Benjamin Xu <benxu@cs.utexas.edu>
Date:   Sat Sep 9 14:23:36 2017 -0500

    test, first draft

commit ee022ddbc3bfbaa2c115228824555812f1553dce
Author: Benjamin Xu <benxu@cs.utexas.edu>
Date:   Sat Sep 9 13:09:40 2017 -0500

    Test in works

commit 135eb2f596dbfa997eb0b8e3f94931f2e3231db6
Author: Ahmed Gheith <gheith@cs.utexas.edu>
Date:   Thu Sep 7 19:02:29 2017 -0500

    removed some code

commit 670a826f0538168426df3b689a290c8800b92d3e
Author: Ahmed Gheith <gheith@cs.utexas.edu>
Date:   Thu Sep 7 19:00:35 2017 -0500

    empty commit""".splitlines()
    mail = scrape(hi)
    print(mail.assignment, mail.semester, mail.classname)
    print(mail.tests)
    print(mail.fails)
