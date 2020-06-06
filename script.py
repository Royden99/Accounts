# MODULE 'SCRIPT':
#   Handle user input, responding with data and functions loaded from 'INIT.py'

import decimal
import var
import func as f

decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN, Emin=None, Emax=None, capitals=None, 
        clamp=None, flags=None, traps=None)

print("\n\n\t\t\tACCOUNTS\n============================================================")
print("\t   Financial bookkeeping for the nerd\n\n")

f.load_fiscal_month()
f.show_accounts()

# At this point we have accumulated the following data:
#   * MonthYear == the Current Fiscal Month i.e. CFM
#       e.g. "January 2020"
# 
#   * Lists "var.Assets[]" and "var.Liabilities[]" each containing a number of accounts
#       and info about them
#
#       - syntax:
#           var.Assets == [[account0], [account1], ... [account'n']]
#
#           [account0] == [name(str), [transactions & tags](str), transaction column(int),
#               tag column(int), final balance(decimal), previous balance(decimal)]
#
#           [transactions & tags] == [[trans0, tag0], [trans1, tag1], ... [trans'n', tag'n']]

exit_words = ["quit", "q", "exit"]

while True:
    # Command Line
    cmd = input("\nacnts>> ")
    
    # navigate Fiscal Months
    # Syntax: "[month]_[year]"
    if cmd[0:3] in var.months:
        f.load_fiscal_month(cmd)
        f.show_accounts()

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
