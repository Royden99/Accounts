# Global variables here

CFM_saved = True       # flag for whether CFM was modified without saving

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

delimiter = ','         # separator in csvfile

linecount = 0           # i.e. "cursor"; tracks position in 'raw'

MonthYear = "0"         # Current Fiscal Month (CFM)

most_recent_month = ""  # the last fiscal month stored in the csvfile

raw = []                # raw data (lines of text) loaded from csvfile

Assets = []             # Accounts data in CFM
Liabilities = []
#   * Lists "var.Assets[]" and "var.Liabilities[]" each contain a number of accounts
#       and info about them
#
#       - syntax:
#           var.Assets == [[account0], [account1], ... [account'n']]
#
#           [account0] == [name(str), [transactions & tags](str), transaction column(int),
#               tag column(int), final balance(decimal), previous balance(decimal)]
#
#           [transactions & tags] == [[trans0, tag0], [trans1, tag1], ... [trans'n', tag'n']]

CA = {'name':"", 'type':"", 'location':0}               # Current Account in CFM

account_names = []      # names of accounts in CFM

statement = {}          # final statement data in CFM
                        # {revenue, expenses, net income, net worth}
