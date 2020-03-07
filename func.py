# MODULE 'INIT':
#   Load data from 'account_records.csv' into the program
#   
#   also define functions for use later

# LOAD DATA
#============================================================================================

# Transactions are handled using the decimal module to avoid the error associated with floats
import var
import decimal

decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN, Emin=None, Emax=None, capitals=None, 
        clamp=None, flags=None, traps=None)

# Import entire csvfile
with open("account_records.csv") as csvfile:
    raw = csvfile.readlines()
 
def deci(string):
    """ Return arg 'string' converted to a 'decimal.Decimal()' object. """
    
    # format transaction strings
    if ' ' in string:    
        string = string.replace(' ', '', 1)
    
    return decimal.Decimal(string)

def set_linecount(MoYr="current"): 
    """ Var 'linecount' holds the number of some line in the raw file data.
    This function positions 'linecount' at the top of the Fiscal Month specified by
    arg 'MoYr', or the current one if none is specified. """
    
    global var.linecount 

    if MoYr == "current":
        while True:
            if raw[var.linecount][0:3] in var.months:
                break
            else:
                var.linecount -= 1
    else:
        # Go to the last line of the file and work back toward the beginning, looking for the
        #   title in the first cell of each line
        var.linecount = len(raw) - 1
        if MoYr == "recent":    # this value allows for 'load_fiscal_month()'
            while True:
                if raw[var.linecount][0:3] in var.months:
                    break
                else:
                    var.linecount -= 1
        else:
            try:
                while True:
                    title = build_cell(0)
                    if title == MoYr:
                        break
                    else:
                        var.linecount -= 1
            except IndexError:
                print(" Could not find fiscal month titled '", MoYr, "'")
                return 0

def build_cell(n):
    """ This function builds and returns a string out of chars found in cell "n", on line
    'linecount'.  A 'cell' being an area separated by delimiters. """

    cellcount = 0
    charbuff = []
    line = raw[var.linecount]

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
    
    global var.linecount

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
    Arg 'account' must be an item in list 'Assets' or 'Liabilities.' """
    
    global var.linecount

    # find previous balance
    set_linecount()
    while True:
        var.linecount -= 1
        if build_cell(0) == 'Final balance:':
            bal = deci(build_cell(account[2]))
            account[5] = bal
            break

   # add all (+ve and -ve) transactions to 'bal'
    for item in account[1]:
        trans = deci(item[0])
        bal += trans

    account[4] = bal

# MAIN FUNCTION
def load_fiscal_month(MoYr="recent"):
    """This function loads raw data from the csvfile into two large lists
    'Assets' and 'Liabilities.' This data is from the Fiscal Month titled 'MoYr'
    in the csvfile. """

    global var.linecount
    global var.MonthYear
    
    # read title of fiscal month
    if set_linecount(MoYr) == 0:
        return 0

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

    # ACCOUNTS: two lists--'Assets' & 'Liabilities'--each containing individual accounts
    #    - each account consists of the following info:
    #       [name, [transactions & tags], transaction column, tag column, final balance, previous balance]

    Assets = []
    Liabilities = []

    # find existing accounts and register them, including name and column info
    var.linecount += 1
    cellcount = 0
    while True:
        nam = build_cell(cellcount)
        if nam == None:
            break
       
        if nam != '':
            if cellcount >= account_type['liabilities']:
                Liabilities.append([nam, [], cellcount, (cellcount + 1), 0, 0])
            elif cellcount >= account_type['assets']:
                Assets.append([nam, [], cellcount, (cellcount + 1), 0, 0])

        cellcount += 1

    # fill in 'transactions & tags' as follows: [[transaction1, tag1], [transaction2, tag2], ...]
    read_transactions(Assets)
    read_transactions(Liabilities)

    # calculate 'final balance'
    for acnt in Assets:
        calc_bal(acnt)
    for acnt in Liabilities:
        calc_bal(acnt)


# MORE FUNCTIONS
#=========================================================================================

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


