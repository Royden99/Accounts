# MAIN GOAL:
# input debits and credits to the python command line.
# save account records to a csvfile 'CIBC_account_records'

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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
MonthYear = raw[linecount].replace(',' , '')

# dict Accounts: details accounts found on the line directly after MonthYear
#   - syntax[ 'account name':(square no. that the account name is in) ]
Accounts = {'cash':1 , 'chequing':7 , 'visa credit':12 , 'mastercard credit':17 , 'TOTAL':22}

# each account has a dict with a list of transactions & messages 
#   - syntax[ 'transaction':'message' ]
Cash = {}
Chequing = {}
Visa_credit = {}
Mastercard_credit = {}
TOTAL = {}

# populate account dicts with data found in the next few rows
linecount += 2
while True:
    linecount += 1
                

# gather conclusion data

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
