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
f.show_statement()

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
    month = var.MonthYear[:3] + var.MonthYear[-4:]
    cmd = input("\n{}\{}\>> ".format(month, var.CA))
    
    # navigate Fiscal Months 
    if cmd[0:3] in var.months:      # syntax '[month] [year]'
        var.CA = ""
        f.load_fiscal_month(cmd)
        f.show_statement()

    #debug
    elif cmd == ' ':
        f.rewrite_csv()

    # create new Fiscal Month
    # delete CFM (Current Fiscal Month)
    #   IN CURRENT FISCAL MONTH:
    
    # navigate accounts
    elif cmd in var.account_names:  # syntax '[account name]'
        var.CA = cmd
        # display account info
        for acnt in var.Assets:
            if acnt[0] == cmd:
                f.display(acnt)
                break
        for acnt in var.Liabilities:
            if acnt[0] == cmd:
                f.display(acnt)
                break

    # create new account
    # delete CA (Current Account)
    
    # display statement
    elif cmd == 'ls':
        f.show_statement()

    #   IN CURRENT ACCOUNT:

    # add transaction
#    elif cmd[0] == '+' or cmd[0] == '-':


    # delete an existing transaction
    
    # save changes
    elif cmd == 'save':
        f.rewrite_raw()
        f.rewrite_csv()

    # exit program
    elif cmd in exit_words:
        break
    # unknown command
    else:
        print(" unknown command: ", cmd)    

quit()
