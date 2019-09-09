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

# list accounts
linecount += 1
charbuff = []
Accounts = []
chars = raw[linecount]

for i in range(len(chars)):
    if i >= 1:
        if chars[i] != ',' and chars[i] != '\n':
            charbuff.append(chars[i])
        elif chars[i] == ',':
            if chars[i-1] != ',':
                Accounts.append("".join(charbuff))
                charbuff = []

Accounts.append("".join(charbuff))

# dictionary for each account with a list of transactions & messages 
linecount += 1
while True:
    linecount += 1
                
# Clean up & format raw csv data for viewing

# MAINLOOP:

# Display Wlist

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
