# MODULE 'INIT':
#   Load data from 'account_records.csv' into the program
#   
#   also define functions for use later

# LOAD DATA
#============================================================================================

# Transactions are handled using the decimal module to avoid the error associated with floats
import var
import decimal

def deci(string):
    """ Return arg 'string' converted to a 'decimal.Decimal()' object. """
    
    # format transaction strings
    if ' ' in string:    
        string = string.replace(' ', '', 1)
    
    return decimal.Decimal(string)

def set_linecount(MoYr="current"): 
    """ This function reads lines of text from the csvfile into list 'var.raw[]', 
    and/or positions 'var.linecount' at the top of the data.
    The text is all the information inside the Fiscal Month specified by
    arg 'MoYr', or the last Fiscal Month in the file if 'MoYr' == 'recent';
    plus final balance info from the previous Fiscal Month."""

    if MoYr != "current":   # We must first gather data from the csvfile before placing
                            #   'var.linecount' at the top of it
        with open("/home/royden99/Pyproj/Accounts/account_records.csv", 'r') as csvfile:

            def read_info():
                csvfile.seek(0,0)   # reset pointer to the beginning of the file
                var.raw = []
                read = False
                look = False
                end = False
                i = 0
                for line in csvfile:                # use the titles to find the f_m we want; start reading lines 
                    if look == False:
                        if line[0:3] in var.months:
                            if build_cell(0, line) == f_m[1]:
                                look = True
                    elif read == False:
                        if line[0:14] == "Final balance:":
                            read = True
                            var.raw.append(line)
                    elif end == False:
                        if line[0:3] in var.months:
                            if i == 1:
                                end = True              # stop reading lines when we come to the next f_m
                            else:
                                i += 1
                                var.raw.append(line)
                        else:
                            var.raw.append(line)
                    else:
                        break

            if MoYr == "recent":    # this value allows for 'load_fiscal_month()'
                # Loop through csvfile twice, the first time finding out the titles of the last two
                #   fiscal months, the second time reading all information from the 'Final balance'
                #   of the second last month to the end of the file.
                f_m = [0,0]
                for line in csvfile:                # find titles of last two months in file
                    if line[0:3] in var.months:
                        f_m[1] = f_m[0]
                        f_m[0] = build_cell(0, line)
                read_info()

            else:   # Same as above, except look for month titled ['MoYr'] instead of the last month
                f_m = [0,0]
                for line in csvfile:        # find titles of desired month & the one before it
                    if line[0:3] in var.months:
                        f_m[1] = f_m[0]
                        f_m[0] = build_cell(0, line)
                        if f_m[0] == MoYr:
                            break
                    if line == "":  # EOF -- ['MoYr'] could not be found
                        print(" Could not find fiscal month titled '", MoYr, "'")
                        csvfile.close()
                        return 0
                read_info()

    # Place 'var.linecount' at the top of 'var.raw' data for this fiscal month
    var.linecount = 0
    while True:
        if var.raw[var.linecount][0:3] in var.months:
            break
        else:
            var.linecount += 1

def build_cell(n, line="default"):
    """ This function builds and returns a string out of chars found in cell "n", on the line
    specified ('var.raw[var.linecount]' is default; otherwise, 'line' could be any string).
    A 'cell' being an area separated by delimiters. """

    cellcount = 0
    charbuff = []
    if line == "default":
        line = var.raw[var.linecount]

    for char in line:
        # find desired cell
        if cellcount != n:
            if char == var.delimiter:
                cellcount += 1
        # build a string from chars in cell
        else:
            # collect one char at a time in 'charbuff', until a delimiter is found
            #   or the end of the line is reached (denoted by '\n')
            # then turn list 'charbuff' into a string
            if char == var.delimiter:
                content = ''.join(charbuff)
                return str(content)
            elif char == '\n':
                if charbuff != '':
                    content = ''.join(charbuff)
                    return str(content)
                else:
                    return None
            else:
                charbuff.append(char)

    return None

def read_transactions(n):
    """ Read transaction info into the second entry ([1]) of all accounts listed under arg
    'n' """

    for acnt in n:
        set_linecount()
        var.linecount += 3
        while True:
            try:
                trans = build_cell(acnt[2])
                tag   = build_cell(acnt[3])
                var.linecount += 1
                next_tag = build_cell(acnt[3])
            except IndexError:
                break

            # read transactions until two consecutive empty cells in the 'tag' column are found
            if tag != '' or next_tag != '':
                entry = [] 
                entry.append(trans)
                entry.append(tag)
                acnt[1].append(entry)

            else:
                break

def calc_bal(account):
    """ This function, for the 'account' specified, looks at last month's final balance
    and all of this month's transactions, and updates the account with the new balance. 
    Arg 'account' must be an item in list 'var.Assets' or 'var.Liabilities.' """

    # find previous balance
    set_linecount()
    while True:
        var.linecount -= 1
        if build_cell(0) == 'Final balance:':
            bal = deci(build_cell(account[2]))
            account[5] = bal
            break

   # find new balance: add all (+ve and -ve) transactions to 'bal'
    for item in account[1]:
        if item[0] != '':
            trans = deci(item[0])
        else:
            trans = deci('0')
        bal += trans

    account[4] = bal

# MAIN FUNCTION
def load_fiscal_month(MoYr="recent"):
    """This function loads raw data (account names, transactions, tags, and balances)
    from the csvfile into two large lists 'var.Assets' and 'var.Liabilities.' This data is from
    the Fiscal Month titled 'MoYr' in the csvfile. """

    # read title of fiscal month
    if set_linecount(MoYr) == 0:
        return 0                    # This happens if the operation failed for some reason

    var.MonthYear = build_cell(0)

    # find boundaries of assets & liabilities
    var.linecount += 1
    account_type = {'assets' : 0, 'liabilities' : 0}
    cellcount = 0
    while True:
        typ = build_cell(cellcount)
        if typ == 'ASSETS':
            account_type['assets'] = cellcount
        elif typ == 'LIABILITIES':
            account_type['liabilities'] = cellcount
        elif typ == None:
            print('Error:\n\tFailed to find "ASSETS" and "LIABILITIES" headings.')
            quit()
        if account_type['assets'] != 0 and account_type['liabilities'] != 0:
            break
        cellcount += 1

    # ACCOUNTS: two lists--'var.Assets' & 'var.Liabilities'--each containing individual accounts
    #    - each account consists of the following info:
    #       [name, [transactions & tags], transaction column, tag column, final balance, previous balance]

    var.Assets = []
    var.Liabilities = []

    # find existing accounts and register them, including name and column info
    var.linecount += 1
    cellcount = 0
    while True:
        nam = build_cell(cellcount)
        if nam == None:
            break
       
        if nam != '':
            if cellcount >= account_type['liabilities']:
                var.Liabilities.append([nam, [], cellcount, (cellcount + 1), 0, 0])
            elif cellcount >= account_type['assets']:
                var.Assets.append([nam, [], cellcount, (cellcount + 1), 0, 0])

        cellcount += 1

    # fill in 'transactions & tags' as follows: [[transaction1, tag1], [transaction2, tag2], ...]
    read_transactions(var.Assets)
    read_transactions(var.Liabilities)

    # calculate 'final balance'
    for acnt in var.Assets:
        calc_bal(acnt)
    for acnt in var.Liabilities:
        calc_bal(acnt)

    # Load account names
    var.account_names = []

    for account in var.Assets:
        var.account_names.append(account[0]) 
    for account in var.Liabilities:
        var.account_names.append(account[0])

    # Load final statement
    var.statement = {}

    set_linecount()
    while build_cell(0) != "Final balance:":
        var.linecount += 1
    var.linecount += 2
    while True:
        try:
            key = build_cell(1)
            if key != "":
                var.statement[key] = build_cell(2)
            var.linecount += 1
        except IndexError:
            break


# MORE FUNCTIONS
#=========================================================================================

# Save changes: 1)rewrite 'var.raw' with all data in 'Assets', 'Liabilities', & 'statement'
#               2)rewrite CFM data in csvfile with contents of 'var.raw'
def save_to_raw():

    for line in var.raw:
        print(line)

    # keep 'final balance' info from previous month, but delete everything from CFM
    i = 0
    for line in var.raw:
        if line[:3] in var.months:
            break
        i += 1
    var.raw = var.raw[0:i]

    # CFM title
    var.raw.append('{},\n'.format(var.MonthYear))

    # place 'ASSETS' & 'LIABILITIES' headings
    line = []
    assets = var.Assets[0][2]           # transaction column of the first account in 'Assets'
    liabilities = var.Liabilities[0][2]
    i = 0
    while True:
        if i == assets:
            line.append('ASSETS,')
        elif i == liabilities:
            line.append('LIABILITIES,')
            break
        else:
            line.append(',')
        i += 1
    line.append('\n')
    var.raw.append(''.join(line))

    def add_info(info, to_what, iterator, match):
        """ A small csv writer

        Append 'info' to list 'to_what' when 'match' is the same value as 'iterator'.
        The rest of the time, append ',' to the list instead."""
        while True:
            if match == iterator:
                to_what.append(info)
                break
            else:
                to_what.append(',')
                iterator += 1
        return iterator, to_what

    # place account names
    line = []
    cellcount = 0
    for account in var.Assets:
        cellcount, line = add_info(account[0], line, cellcount, account[2])
    for account in var.Liabilities:
        cellcount, line = add_info(account[0], line, cellcount, account[2])

    line.append('\n')
    var.raw.append(''.join(line))
    var.raw.append(',\n')  # (also a blank line)

    # place transactions & tags
    length = 0  # find the length of the longest list of transactions
    for account in var.Assets:
        if len(account[1]) > length:
            length = len(account[1])
    for account in var.Liabilities:
        if len(account[1]) > length:
            length = len(account[1])
    i = 0
    while i <= length:
        line = []
        cellcount = 0
        for account in var.Assets:
            try:
                info = "{},{}".format(account[1][i][0], account[1][i][1])
            except IndexError:
                info = ","
            cellcount, line = add_info(info, line, cellcount, account[2])
            cellcount += 1  # necessary because two values are appended to 'list' simultaneously
        for account in var.Liabilities:
            try:
                info = "{},{}".format(account[1][i][0], account[1][i][1])
            except IndexError:
                info = ","
            cellcount, line = add_info(info, line, cellcount, account[2])
            cellcount += 1  # necessary because two values are appended to 'list' simultaneously

        line.append('\n')
        var.raw.append(''.join(line))
        i += 1

    # place final balance
    line = []
    line.append('Final balance:,')
    cellcount = 1
    for account in var.Assets:
        cellcount, line = add_info(str(account[4]), line, cellcount, account[2])
    for account in var.Liabilities:
        cellcount, line = add_info(str(account[4]), line, cellcount, account[2])
    line.append('\n')
    var.raw.append(''.join(line))
    var.raw.append(',\n')
    
    # place statement
    for key, value in var.statement.items():
        line = []
        if "Net worth" in key:
            var.raw.append(',\n')
        line.append(",{},{}\n".format(key, value))
        var.raw.append(''.join(line))
    
    with open("/home/royden99/Pyproj/Accounts/debugfile.csv", 'w') as csvfile:
        for line in var.raw:
            csvfile.write(line)


# display accounts in readable format
def display(account):
    """Display the information in the specified 'account' that the user wants to see:
    1) Account name, 2) Previous balance, 3) Transactions & tags, and 4) Final balance."""
    
    print("\n\n\n\t{}\n\t{}\n\n prev. balance:\t{}\n".format(account[0],
        ''.ljust(len(account[0]),'='), account[5]))
    for item in account[1]:
        print(item[0].rjust(13), '\t', item[1].ljust(True))
    print("\n final balance:\t", account[4])
    print("\n =============================================================")


def show_statement():

        # Display names of accounts from CFM
        print("\n Assets:")
        for account in var.Assets:
            print("{}  -  {}".format(account[0].rjust(25), account[4]))
        print("\n Liabilities:")
        for account in var.Liabilities:
            print("{}  -  {}".format(account[0].rjust(25), account[4]))

        # Display final statement info from CFM
        print("\n")
        for key, value in var.statement.items():
            print(" {}\t{}".format(key, value))
