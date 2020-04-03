# MODULE 'SCRIPT':
#   Handle user input, responding with data and functions loaded from 'INIT.py' (currently also func.py)

import decimal
import var
from INIT import *
   
load_fiscal_month()

# At this point we have accumulated the following data:
#   * MonthYear == the Current Fiscal Month i.e. CFM
#       e.g. "January 2020"
# 
#   * Lists "Assets[]" and "Liabilities[]" each containing a number of accounts
#       and info about them
#
#       - syntax:
#           Assets == [[account0], [account1], ... [account'n']]
#
#           [account0] == [name(str), [transactions & tags](str), transaction column(int),
#               tag column(int), final balance(decimal), previous balance(decimal)]
#
#           [transactions & tags] == [[trans0, tag0], [trans1, tag1], ... [trans'n', tag'n']]

print("\n\n Current Fiscal Month == ", var.MonthYear)

exit_words = ["quit", "q", "exit"]

while True:
    # Command Line
    cmd = input(">>> ")
    
    # navigate Fiscal Months
    # Syntax: "[month]_[year]"
    if cmd[0:3] in var.months:
        load_fiscal_month(cmd)
        print(" Current Fiscal Month == ", var.MonthYear)

    # create new Fiscal Month
    # delete CFM (Current Fiscal Month)
    #   IN CURRENT FISCAL MONTH:
    # navigate accounts
    # create new account
    # delete CA (Current Account)
    # display statement
    #   IN CURRENT ACCOUNT:
    # add transaction
    # delete an existing transaction
    # exit program
    elif cmd in exit_words:
        break
    else:
        print("unknown command: ", cmd)

quit()
