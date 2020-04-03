
	Program purpose:

INPUT	* Debits  (-ve amounts),  what it was spent on
	* Credits (+ve amounts),  who from

OUTPUT	* Gross profit
	* How much spent
	* Net profit
	* New final balances

SAVE information to csvfile in monthly sections


	Program operation:

enter:
  Load previous information from csvfile

mainloop commands (custom command line):
  Enter transactions
  Calculate outputs
  Display updated info for current month
  Navigate, create, or delete individual accounts
  Navigate, create, or delete fiscal months

at end:
  Append all new information to csvfile
