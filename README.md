# uva_submit
A CLI tool that enables submission and status checking of UVa problems from terminal

## Setup
### Dependencies
1. `pip install bs4`
2. `pip install getpass`

### Environment variables
Put the following in your `.bashrc` or `.zshrc` file:
1. `export UVA_USERNAME="YOUR_USERNAME_HERE"`
2. `export UVA_PASSWD="YOUR_PASSWORD_HERE"`

Finally, remove the `.py` extension and put the file in your PATH

## What this script does
#### To submit a problem (only C++ submission is supported now)
```
uva submit PROBLEM_ID filename.cc
```
#### To check submission status
```
uva tail (NUMBER_OF_SUBMISSION, default to 5)
```
