import func
import var

# decide which months we want to include
months = ["August 2019", "September 2019", "October 2019", "November 2019", "December 2019", "January 2020", "February 2020", "March 2020", "April 2020", "May 2020", "June 2020", "July 2020", "August 2020", "September 2020", "October 2020", "November 2020", "December 2020"]

# load each month in turn and add all revenue together
Revenue = func.deci('0')
for MoYr in months:
    func.load_fiscal_month(MoYr)
    Revenue += func.deci(var.statement["Revenue --------"])
    print("{}\t-\t+{}".format(MoYr, var.statement["Revenue --------"]))

print("\t--------------------\nTOTAL\t\t-\t", Revenue)
    
# take 10% of the revenue
tithe = Revenue/func.deci('10')
print('\nTithe\t-\t', tithe)
