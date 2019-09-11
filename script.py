# MAIN GOAL:
# input debits and credits to the python command line.
# save account records to a csvfile 'CIBC_account_records'

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
delimiter = ','

# Import most recent month's data from csvfile
with open("/home/royden99/Documents/CIBC_account_records.csv") as csvfile:
    raw = csvfile.readlines()

# find last line
linecount = len(raw) - 1
# work backward to find most recent month heading
while True:
    if raw[linecount][0:3] in months:
        break
    else:
        linecount -= 1

# INITIAL DATA:
# month
MonthYear = raw[linecount].replace(delimiter , '')

# dict Accounts: details accounts found on the line directly after MonthYear
#   - syntax[ 'account name':(square no. that the account name is in) ]
Accounts = {'cash':1 , 'chequing':5 , 'visa credit':9 , 'mastercard credit':13 , 'TOTAL':17}

# each account has a list of transactions & a list of corresponding notes
Cash_t = []
Cash_n = []
Chequing_t = []
Chequing_n = []
Visa_credit_t = []
Visa_credit_n = []
Mastercard_credit_t = []
Mastercard_credit_n = []
TOTAL_t = []
TOTAL_n = []

# populate account dicts with data in transaction columns
linecount += 2
A = Accounts['cash']
B = Accounts['chequing']
C = Accounts['visa credit']
D = Accounts['mastercard credit']
E = Accounts['TOTAL']
while True:
    linecount += 1
    line = raw[linecount]
    squarecount = 0
    charbuff = []
    # rows in transaction columns will begin with a delimiter
    if line[0] == delimiter:
        # keep track of our horizontal location in the spreadsheet, leftmost square is '1'
        for char in line:
            # collect data one char at a time in charbuff
            if char != delimiter:
               charbuff.append(char)
            else:
                # build transaction & note content from chars collected in charbuff,
                #   add them to account lists in 'squarecount' columns
                content = ''.join(charbuff)
                if content != '':
                    if squarecount == A:
                        Cash_t.append(content)
                    elif squarecount == A + 1:
                        Cash_n.append(content)
                    elif squarecount == B:
                        Chequing_t.append(content)
                    elif squarecount == B + 1:
                        Chequing_n.append(content)
                    elif squarecount == C:
                        Visa_credit_t.append(content)
                    elif squarecount == C + 1:
                        Visa_credit_n.append(content)
                    elif squarecount == D:
                        Mastercard_credit_t.append(content)
                    elif squarecount == D + 1:
                        Mastercard_credit_n.append(content)
                    elif squarecount == E:
                        TOTAL_t.append(content)
                    elif squarecount == E + 1:
                        TOTAL_n.append(content)
                    # reset charbuff
                charbuff = []
                # count squares
                squarecount += 1

    # end of transaction columns have been reached;
    # gather conclusion data
    else:
        break

print("Cash_t = ", Cash_t)
print("Cash_n = ", Cash_n)
print("Chequing_t = ", Chequing_t)
print("Chequing_n = ", Chequing_n)
print("Visa_credit_t = ", Visa_credit_t)
print("Visa_credit_n = ", Visa_credit_n)
print("Mastercard_credit_t = ", Mastercard_credit_t)
print("Mastercard_credit_n = ", Mastercard_credit_n)
print("TOTAL_t = ", TOTAL_t)
print("TOTAL_n = ", TOTAL_n)

# MAINLOOP:

# Display data

# Gather user input

# React to input:
   
    # Default (input starts with '-' or '+'):        

        # Add new credit or debit & message to Wlist
        
        # Calculate & add to Wlist:
        #   * Total profits
        #   * Total spent
        #   * Actual amount gained or lost
        #   * New balance

    # Input 'new month': 
    #    * save
    #    * write headings in csvfile for new month
    #    * start a new Wlist for new current month
 
    # Input 'save': write Wlist to csvfile (save most recent month's data in complete format)

    # Input 'exit': quit

quit()
