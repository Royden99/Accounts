
	Program purpose:

INPUT	* Debits  (-ve amounts),  what it was spent on
	* Credits (+ve amounts),  who from

OUTPUT	* Gross profit
	* How much spent
	* Net profit
	* New total

SAVE information to csvfile "Balance," in monthly sections


	Program operation:

enter:
  choose to edit existing month or start new

mainloop:
  Enter inputs on command line
  Calculate outputs
  Display updated info for current month after every input

at end:
  Write all new information to csvfile "Balance"
  Open "Balance" when program exit
