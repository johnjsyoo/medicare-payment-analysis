#Loading datasets
rawdata  = read.csv("PaymentsDataset.csv")
mydata  = read.csv("PaymentsDataset.csv")

#Removing outlier
mydata <- rawdata[rawdata$NPI!=1568413417,]

#Creating variables for Pharma and Medicare payments
pharma_pmts <- mydata$Avg_Payment_USDollars
medicare_pmts <- mydata$AVERAGE_MEDICARE_PAYMENT_AMT

#Running summary statistics
summary(pharma_pmts)
mean(pharma_pmts)
sd(pharma_pmts)

summary(medicare_pmts)
mean(medicare_pmts)
sd(medicare_pmts)

#Running correlation test
cor.test(medicare_pmts, pharma_pmts)