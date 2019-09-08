# MAIN GOAL:
# input debits and credits to the python command line.
# save account records to a csvfile 'CIBC_account_records'

# Import most recent month's data from csvfile as a list 'Wlist'
#   (Wlist is now modified by MAINLOOP and saved back to csvfile)

with open("/home/royden99/Documents/CIBC_account_records.csv") as csvfile:
    File = csvfile.read()

print(File)

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
