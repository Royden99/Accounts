# MAIN GOAL:
# input debits and credits to the python command line.
# save account records to a csvfile 'CIBC_account_records'

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
delimiter = ','

# Import entire csvfile
with open("/home/royden99/Documents/CIBC_account_records.csv") as csvfile:
    raw = csvfile.readlines()

# from the end of 'raw', go back to most recent month's data
linecount = len(raw) - 1
while True:
    if raw[linecount][0:3] in months:
        break
    else:
        linecount -= 1

# STORE DATA FROM 'raw' AS LISTS & VARIABLES FOR EASE OF USE
# month
MonthYear = raw[linecount].replace(delimiter , '')

# dict Accounts: account details
#   - syntax[ 'account name' : square no. that the account name is in ]
Accounts = {'cash':1 , 'chequing':5 , 'visa credit':9 , 'mastercard credit':13 , 'TOTAL':17}

# each account exists as a list of transactions & a list of corresponding notes
#  Format of '_t' lists:  [t1, t2, ... tn, profit, loss, net, final_balance]
#  Format of '_n' lists:  [n1, n2, ... nn]
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

# Populate lists
linecount += 2
A = Accounts['cash']
B = Accounts['chequing']
C = Accounts['visa credit']
D = Accounts['mastercard credit']
E = Accounts['TOTAL']

while True:     # successive lines
    linecount += 1
    try:
        line = raw[linecount]
    except IndexError:
        break   # end of file

    squarecount = 0
    charbuff = []

    for char in line:       # successive chars
        # collect data (between delimiters) one char at a time in charbuff
        if char != delimiter:
           charbuff.append(char)
        else:
            # turn list 'charbuff' into a string
            content = ''.join(charbuff)
            # save the content, if any, to whatever list is indicated by 'squarecount'
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
