__author__ = 'John'

from os import listdir
from os.path import isfile, join
import csv
import pandas as pd

"""
Finding all files in path and creating a list
"""
mypath = '/Users/John/Dropbox/SUMMER 15/Big Data/MedicareOutput/'
onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath,f))]

"""
Taking all the files in our list and creating one complete Pandas data frame
"""
transactions = []
for file in onlyfiles:
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            transactions.append(row)
transDF = pd.DataFrame(transactions)
transDF.to_csv('MedicarePayments.csv')

"""
Loading our complete Medicare payment CSV file and filtering all providers in TX
"""
fileName = '/Users/John/Downloads/12192014_ALLDTL/OPPR_ALL_DTL_GNRL_12192014.csv'
payList = pd.read_csv(fileName)
payTX = payList[(payList.Recipient_State == 'TX')]

"""
Further redefining our dataset
"""
paySubset = payTX.loc[:,['Physician_Profile_ID',
                         'Physician_First_Name',
                         'Physician_Middle_Name',
                         'Physician_Last_Name',
                         'Recipient_Primary_Business_Street_Address_Line1',
                         'Recipient_City',
                         'Recipient_State',
                         'Recipient_Zip_Code',
                         'Product_Indicator',
                         'Total_Amount_of_Payment_USDollars']]

paymentsSorted = paySubset.sort(['Physician_Profile_ID'], ascending=True) # Sort the dataset ascending
paymentsUnique = paymentsSorted.drop_duplicates(cols = 'Physician_Profile_ID') # So we can remove the duplicates
paymentsUnique = paymentsUnique[pd.notnull(paymentsUnique['Physician_Profile_ID'])] # And create a table of unique IDs

"""
Grouping the payments by ID so can grab the mean of the payments
"""
groupedPayments = paySubset.groupby('Physician_Profile_ID')
paymentAvg = groupedPayments.mean()
payments = paymentAvg.reset_index()
payments.columns = ['Physician_Profile_ID', 'Avg_Payment_USDollars']

mergedTable = pd.merge(paymentsUnique,payments,on='Physician_Profile_ID', how='inner') # Merging the table on the PID

"""
Creating an Identifier for Physicians so we can join on it
"""
mergedTable['Recipient_Zip_Code'] = mergedTable['Recipient_Zip_Code'].astype(str)
mergedTable['Recipient_Zip_Code'] = mergedTable['Recipient_Zip_Code'].str[:5]
mergedTable['Identifier'] = mergedTable.Physician_First_Name + \
                            mergedTable.Physician_Last_Name + \
                            mergedTable.Recipient_Zip_Code
mergedTable['Identifier'] = mergedTable['Identifier'].str.upper()

########################################################################################################################

medicarePayments = pd.read_csv('/Users/John/Dropbox/SUMMER 15/Big Data/MedicarePayments.csv')

finalMerge = pd.merge(medicarePayments,mergedTable,on='Identifier',how='inner')

finalMerge.to_csv('PaymentsDataset.csv')