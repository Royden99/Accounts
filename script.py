# MODULE 'SCRIPT':
#   Handle user input, responding with data and functions provided by 'func' and 'var'

import decimal
import var
import func as f

decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN, Emin=None, Emax=None, capitals=None, 
        clamp=None, flags=None, traps=None)

def check_for_unsaved_changes():
    if var.CFM_saved == False:
        confirm = input(' You have unsaved changes. Save automatically before continuing?\
\n [y/n] >>')
        if confirm == 'y' or confirm == 'yes':
            f.rewrite_raw()
            f.rewrite_csv()
        var.CFM_saved = True

print("\n\n\t\t\tACCOUNTS\n============================================================")
print("\t   Financial bookkeeping for the nerd\n\n")

f.load_fiscal_month()
var.most_recent_month = var.MonthYear

f.display_statement()

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
    cmd = input("\n{}\{}\>> ".format(month, var.CA['name']))

    # The following conditionals interperet the commands of the user.
     
    #debug
    if cmd == ' ':
        if var.CA['type'] == 'asset':
            accounts = var.Assets
        else:
            accounts = var.Liabilities
        for line in accounts[var.CA['location']][1]:
            print(line)
        
    # navigate Fiscal Months 
    elif cmd[0:3] in var.months:      # syntax '[month] [year]'
        var.CA = {'name':"", 'type':"", 'location':0}
        check_for_unsaved_changes()
        f.load_fiscal_month(cmd)
        f.display_statement()

    # create new Fiscal Month
    elif cmd == "new month":
        # ensure that CFM is the most recent one
        check_for_unsaved_changes()
        if var.MonthYear != var.most_recent_month:
            f.load_fiscal_month()

        # replace 'var.MonthYear' with the next month
        var.MonthYear = f.find_month('next')

        # zero account transaction data in Assets and Liabilities, replace prev_balance with final_balance
        #   (final_balance stays the same)
        for account in [(chain) for list_ in (var.Assets, var.Liabilities) for chain in list_]:
            account[1] = [['', '']]
            account[5] = account[4]

        # calculate statement
        f.calc_statement()

        # save current data to a new month, empty of transactions, at the end of csvfile
        f.rewrite_raw(new_month = True)
        f.rewrite_csv(new_month = True)

        var.most_recent_month = var.MonthYear
        f.display_statement()

    # delete CFM (only the most recent one)
    elif cmd == 'del month':
        if var.MonthYear != var.most_recent_month:
            print(" Sorry, you can only delete the latest Month in the file.")
            continue
        else:
            # double-check with the user
            confirm = input(" Delete this fiscal month?\n Any existing transactions will be lost. [y/n]\n\n>>")
            if confirm == 'yes' or confirm == 'y':
                check_for_unsaved_changes()

                # load the second most recent fiscal month
                f.load_fiscal_month(f.find_month('prev'))
                
                # rewrite csvfile, simply leaving out any data that used to follow
                f.rewrite_csv(del_month = True)
                
                var.most_recent_month = var.MonthYear
                f.display_statement()

    # search database for specific transactions
    elif cmd == 'search_transactions':
        pass

    #   IN CURRENT FISCAL MONTH:
    
    # navigate accounts
    # (Currently the only method for navigation is to type the name of the account into the command line.
    #   Account names are apparent to the user via the initial 'f.display_statement()' or the 'ls' command.)
    elif cmd in var.account_names:  # syntax '[account name]'
        var.CA['name'] = cmd
        for i, acnt in enumerate(var.Assets):
            if acnt[0] == cmd:
                var.CA['type'] = "asset"
                var.CA['location'] = i
                f.display(acnt)         # display account info
                break
        for i, acnt in enumerate(var.Liabilities):
            if acnt[0] == cmd:
                var.CA['type'] = "liability"
                var.CA['location'] = i
                f.display(acnt)         # display account info
                break
        
    # create new account (only in most recent month)
    elif cmd == 'new account':
        # ascertain that CFM is most recent month
        # user decide whether account is an asset or liability
        # user provide account name
        # populate new account information -- name, trans&tags, trans_col, tag_col,
        #   final_bal, and prev_bal
        # if new account is an asset, then all liabilities accounts are going to be 
        #   'shoved over' and their lateral (column) placement needs to be re-figured
        # append new account into respective list of accounts; update 'var.account_names'
        # update 'var.CA' to reflect the new account; display it
        var.CFM_saved = False
        pass
    # delete current account
    elif cmd[:3] == 'del' and var.CA['name'] != "":
        # double-check with user
        # ascertain that CFM is most recent month
        # change column data for any accounts to the right of the one being deleted,
        #   to bring them in and fill the gap
        # delete account info from its respective list
        # reset var.CA to nothing; display statement 
        var.CFM_saved = False
        pass
    
    # display CFM statement
    elif cmd == 'ls':
        f.display_statement()

    #   IN CURRENT ACCOUNT:

    # add a new transaction
    elif len(cmd) > 0 and (cmd[0] == '+' or cmd[0] == '-'):
        if var.CA['name'] != "":        # ensure that an account is selected
            prefix = cmd[0]

            try:    # check that the transaction is valid
                trans = str(decimal.Decimal(cmd))
                tag = input(" Tag: ")   # prompt the user for a 'tag' - description of the transaction
                
                # Add the transaction to the Current Account
                def insert(transaction, account):
                    """ Insert 'transaction' into the appropriate list of transactions & tags.
                    Then, recalculate the final balance. """
                    if prefix == '-':
                        # insert transaction just before the second blank entry 
                        for i in range(0, len(account[1]), 1):
                            if account[1][i] == ['', '']:
                                account[1].insert(i, [transaction, tag])
                                break
                    elif prefix == '+':
                        # insert transaction at the very end of the list
                        account[1].append(['+'+transaction, tag])

                    # add transaction to final balance
                    account[4] += f.deci(transaction)
                
                if var.CA['type'] == 'asset':
                    insert(trans, var.Assets[var.CA['location']])
                elif var.CA['type'] == 'liability':
                    insert(trans, var.Liabilities[var.CA['location']])
            
                # recalculate CFM statement
                f.calc_statement()

                # re-display the account
                if var.CA['type'] == 'asset':
                    f.display(var.Assets[var.CA['location']])
                else:
                    f.display(var.Liabilities[var.CA['location']])

            except decimal.InvalidOperation:
                print("\n Invalid transaction format")
        else:
            print(" Please select an account before adding a transaction. ")
        var.CFM_saved = False

    # delete an existing transaction
    
    # save changes
    elif cmd == 'save' or cmd == 'write':
        f.rewrite_raw()
        f.rewrite_csv()
        var.CFM_saved = True

    # exit program
    elif cmd in exit_words:
        check_for_unsaved_changes()
        break 
    # unknown command
    else:
        print(" unknown command: ", cmd)    

quit()
