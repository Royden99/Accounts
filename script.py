# MAIN GOAL:
# input debits and credits to the python command line.
# save account records to a csvfile 'CIBC_account_records'

# Housekeeping
#-------------------------------------------------------------------------------------------

# Transactions are handled using the decimal module to avoid the error associated with floats
import decimal

decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN, Emin=None, Emax=None, capitals=None, 
        clamp=None, flags=None, traps=None)

def deci(string):
    """ Return arg 'string' converted to a 'decimal.Decimal()' object. """
    
    # format transaction strings
    if ' ' in string:    
        string = string.replace(' ', '', 1)
    
    return decimal.Decimal(string)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
delimiter = ','

# Import entire csvfile
with open("/home/royden99/Documents/account_records.csv") as csvfile:
    raw = csvfile.readlines()

def reset_linecount(): 
    """ Var 'linecount' holds the value of some line in the raw file data.
    This function positions 'linecount' at the top of the most recent monthly dataset. """
    
    global linecount 

    # Go to the last line of the file and work back toward the beginning, looking for the
    #   title
    linecount = len(raw) - 1
    while True:
        if raw[linecount][0:3] in months:
            break
        else:
            linecount -= 1
    

def build_cell(n):
    """ This function builds and returns a string out of chars found in cell "n", on line
    'linecount'.  A 'cell' being an area separated by delimiters. """

    cellcount = 0
    charbuff = []
    line = raw[linecount]

    for char in line:
        # find desired cell
        if cellcount != n:
            if char == delimiter:
                cellcount += 1
        # build a string from chars in cell
        else:
            # collect one char at a time in 'charbuff', until a delimiter is found
            #   or the end of the line is reached (denoted by '\n')
            # then turn list 'charbuff' into a string
            if char == delimiter:
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

#-------------------------------------------------------------------------------------------

# read title of current fiscal month
reset_linecount()
MonthYear = build_cell(0)

# find boundaries of assets & liabilities
linecount += 1
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
#       [name, [transactions & tags], transaction column, tag column, final balance]

Assets = []
Liabilities = []

# read names of existing accounts, find what column they are in
linecount += 1
cellcount = 0
while True:
    nam = build_cell(cellcount)
    if nam == None:
        break
   
    if nam != '':
        if cellcount >= account_type['liabilities']:
            Liabilities.append([nam, [], cellcount, (cellcount + 1), 0])
        elif cellcount >= account_type['assets']:
            Assets.append([nam, [], cellcount, (cellcount + 1), 0])

    cellcount += 1

# fill in 'transactions & tags' as follows: [[transaction1, tag1], [transaction2, tag2], ...]
def read_transactions(n):
    """ Read transaction info into the second entry ([1]) of all accounts listed under arg
    'n' """
    
    global linecount

    for acnt in n:
        reset_linecount()
        linecount += 3
        while True:
            try:
                trans = build_cell(acnt[2])
                tag   = build_cell(acnt[3])
                linecount += 1
                next_tag = build_cell(acnt[3])
            except IndexError:
                break

            # read transactions until two consecutive empty cells in the 'tag' column are found
            if tag != '' or next_tag != '':
                if trans != '':
                    entry = [] 
                    entry.append(deci(trans))
                    entry.append(tag)
                    acnt[1].append(entry)

            else:
                break

read_transactions(Assets)
read_transactions(Liabilities)

# calculate 'final balance'
def calc_bal(account):
    """ This function, for the 'account' specified, looks at last month's final balance
    and all of this month's transactions, and returns the new balance. 
    Arg 'account' must be an item in list 'Assets' or 'Liabilities.' """
    
    global linecount

    # find previous balance
    reset_linecount()
    while True:
        linecount -= 1
        if build_cell(0) == 'Final balance:':
            bal = deci(build_cell(account[2]))
            break

    # add all (+ve and -ve) transactions to 'bal'
    for item in account[1]:
        trans = item[0]
        bal += trans

    account[4] = bal


calc_bal(Assets[1])
print(Assets[1][4])

# display accounts in readable format

quit()
