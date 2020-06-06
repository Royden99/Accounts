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
    plus final balance info, etc from the previous Fiscal Month."""

    if MoYr != "current":   # We must first gather data from the csvfile before placing
                            #   'var.linecount' at the top of it
        with open("/home/royden99/Pyproj/Accounts/account_records.csv", 'r') as csvfile:

            def read_info():
                csvfile.seek(0,0)   # reset pointer to the beginning of the file
                var.raw = []
                read = False
                look = False
                for line in csvfile:                # use the titles to find the info we want; read it 
                    if look == False:
                        if line[0:3] in var.months:
                            if build_cell(0, line) == f_m[1]:
                                look = True
                    else:
                        if read == False:
                            if line[0:14] == "Final balance:":
                                read = True
                                var.raw.append(line)
                        else:
                            var.raw.append(line)

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
                if trans != '':
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
        trans = deci(item[0])
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


# MORE FUNCTIONS
#=========================================================================================

# Save:  rewrite CFM with current data
def save_changes():
    set_linecount(var.MonthYear)    # navigate to CFM title
    

# display accounts in readable format
def display(account):
    """Display the information in the specified 'account' that the user wants to see:
    1) Account name, 2) Previous balance, 3) Transactions & tags, and 4) Final balance."""
    
    print("\n\n\n\t{}\n\t{}\n\n prev. balance:\t{}\n".format(account[0],
        ''.ljust(len(account[0]),'='), account[5]))
    for item in account[1]:
        print(item[0].rjust(13), '\t', item[1].ljust(True))
    print("\n final balance:\t", account[4])
    print("\n=============================================================")


def show_accounts():

        # Display names of accounts from CFM
        print(" Current Fiscal Month == ", var.MonthYear)
        print("\nAssets:")
        for account in var.Assets:
            print("\t", account[0])
        print("\nLiabilities:")
        for account in var.Liabilities:
            print("\t", account[0])
