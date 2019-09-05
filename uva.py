#!/usr/local/bin/python3

import requests
import getpass
import sys
import os
from bs4 import BeautifulSoup

class UVA:
    def __init__(self):
        self.FORMAT = ['{:^15}','{:^12}','{:^40}','{:^20}','{:^15}','{:^15}','{:^25}']
        self.TITLE = ['#', 'ID', 'Problem', 'Verdict', 'Language', 'Runtime', 'Date']

        # Prepare session
        session = requests.session()
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        session.headers = headers
        self.session = session


    def login(self, username, passwd):
        url = 'https://onlinejudge.org/index.php?option=com_comprofiler&task=login'

        # Post first to get cbsecuritym3 token
        res = self.session.post(url, {})
        s = BeautifulSoup(res.content, 'lxml')
        e = s.select_one('input[name=cbsecuritym3]')

        data = {
            'username': username,
            'passwd': passwd,
            'op2': 'login',
            'force_session': '1',
            'loginfrom': 'loginmodule',
            'remember': 'yes',
            'submit': 'Login',
            e['name']: e['value']
        }

        self.session.post(url, data)


    def view_submission(self, count):
        url = 'https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=9&limit={}'.format(count)
        res = self.session.get(url)
        s = BeautifulSoup(res.content, 'lxml')

        row = s.select_one('tr.sectiontableentry1')
        for idx, (form, title) in enumerate(zip(self.FORMAT, self.TITLE)):
            print(form.format(title), end='\n' if idx == len(self.FORMAT) - 1 else '|')
        # Tail the last count submissions
        for i in range(count):
            for idx, (form, string) in enumerate(zip(self.FORMAT, row.stripped_strings)):
                print(form.format(string), end='\n' if idx == len(self.FORMAT) - 1 else '|')
            # Goto next <tr>
            row = row.next_sibling.next_sibling


    def submit(self, problem_id, file_name):
        url = 'https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=25&page=save_submission'
        path = '{}/{}'.format(os.getcwd(), file_name)

        # Read code file we need to submit
        with open(path, 'r') as f:
            data = {
                'localid': problem_id,
                'language': '5',
                'code': f.read()
            }

        res = self.session.post(url, data)
        print('Submission with status {}'.format(res.status_code))


if __name__ == '__main__':
    uva = UVA()
    username = os.environ['UVA_USERNAME']
    passwd = os.environ['UVA_PASSWD']
    uva.login(username, passwd)

    # Parse command line arguments
    try:
        if sys.argv[1] == 'submit':
            uva.submit(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'tail':
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            uva.view_submission(count)
    except e:
        print("{} operation cancelled".format(sys.argv[1]))

