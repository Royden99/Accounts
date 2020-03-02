# MODULE 'SCRIPT':
#   Handle user input, responding with data and functions loaded from 'INIT.py'

import decimal
from INIT import * 

# At this point we have accumulated the following data:
#   * MonthYear == the current fiscal month i.e. 'working directory'
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


display(Assets[1])
display(Liabilities[0])

#while True:
#    # Commands: select account, add transaction, display statement, start new month
#    cmd = raw_input()
#    if cmd == 
#

quit()
