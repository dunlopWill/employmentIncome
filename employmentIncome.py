import math
#ASSESSABLE EMPLOYMENT INCOME
#Is general earnings received during tax year (6th April to 5th April).
#Treat earnings received as the earlier of the time when payment is made and when a person becomes entitled to payment.
generalEarnings = 0

#TAXABLE BENEFITS:
#Vouchers
exchangeableValue = 0
creditVoucherEmployerPaid = 0
creditVoucherEmployeePaid = 0
goodsVoucherEmployerPaid = 0
goodsVoucherEmployeePaid = 0
    #Cash vouchers = taxed at amount can exchange for voucher
cashVouchers = exchangeableValue
    #Credit tokens = taxed at cost to employer less any amount paid by employee
creditTokens = creditVoucherEmployerPaid - creditVoucherEmployeePaid
    #Vouchers for goods/services = taxed at cost to employer less any amount paid by employee
goodsVouchers = goodsVoucherEmployerPaid - goodsVoucherEmployeePaid

#Living accomodation (is taxable unless its job related)
accomodationCost = 150000
capitalImprovements = 15000
annualAccomodationValue = 7500
employeeRentPerMonth = 700
officialRateOfInterest = 0.025
monthsOccupied = 12 #Time apportion for when available in tax year
excess = 0
    #Basic rental benefit:
        #If owned by employer, benefit = rent would have been paid if had been let at its annual value
        #If rented by employer, benefit = higher of the annual value and the rent actually paid by employer
basicRentalBenefit = annualAccomodationValue - employeeRentPerMonth * monthsOccupied
if basicRentalBenefit < 0: #Restrict basic rental benefit to zero (excess is used to reduce additional)
    excess = basicRentalBenefit * -1
    basicRentalBenefit = 0
print(f"Basic rental benefit is: £{basicRentalBenefit}")
    #Additional yearly benefit (only applies to accomodation that costed the employer more than £75k to provide):
        # = (cost of providing accomodation - 75000) * official rate of interest at start of tax year
        # cost of providing accomodation = original cost + any capital improvements made before start of tax year
    #Any employee payment to the employer for property occupation reduces the taxable benefit
additionalYearlyBenefit = 0
if accomodationCost + capitalImprovements > 75000:
    additionalYearlyBenefit = (accomodationCost + capitalImprovements - 75000) * officialRateOfInterest - excess
print(f"Additional yearly rental benefit is: £{additionalYearlyBenefit}")

accomodationBenefit = basicRentalBenefit + additionalYearlyBenefit
print(f"Taxable accomodation benefit is: £{accomodationBenefit}")

#Private use cars and fuel including home to work travel
carMonths = 3
carListPrice = 0
carAccessories = 0
if carAccessories < 100:
    carAccessories = 0
carTotal = carListPrice + carAccessories
carEmployeePaidMonthly = 0
employeeFuelPaidMonthly = 30
diesel = True #Assume petrol if diesel not true
dieselSupplement = 0.04
rDE2 = False #If diesl car meets RDE2 (aka Euro 6d), exempt from diesel supplement
carEmissions = 192
emissions = carEmissions - carEmissions % 5 #CO2 emissions of car in grams per kilometer (g/km) rounded down to nearest 5g/km
emissionsPercentage = 0
    #Calculate emmission percentage based on emission thresholds and if petrol or diesel
if emissions < 0 and emissions <= 50:
    emissionsPercentage = 0.13
elif emissions >= 51 and emissions <= 75:
    emissionsPercentage = 0.16
elif emissions >= 76 and emissions <= 94:
    emissionsPercentage = 0.19
elif emissions == 95:
    emissionsPercentage = 0.2
else:
    emissionsPercentage = 0.2 + math.floor((emissions - 95)/5) * 0.01 #For every extra 5g/km (rounded down) add 1% up to 37%
#Add diesel supplement unless RDE2 is true
if diesel == True and rDE2 == False:
    emissionsPercentage = emissionsPercentage + dieselSupplement
if emissionsPercentage > 0.37: #Overall max of 37% (even for diesel)
    emissionsPercentage = 0.37
#Calculate taxable car benefit
carBenefit = carTotal * emissionsPercentage * carMonths/12 - carEmployeePaidMonthly * carMonths
# print(emissionsPercentage)
print(f"Taxable car benefit is: £{round(carBenefit)}")
#Calculate taxable fuel benefit
fuelBenefit = 23400 * emissionsPercentage
if fuelBenefit > employeeFuelPaidMonthly * carMonths:
    fuelBenefit = fuelBenefit
else:
    fuelBenefit = 0
print(f"Taxable fuel benefit is: £{round(fuelBenefit)}")

#Vans for private use (doesn't include home to work travel)
van = False
vanMonths = 0
vanEmissions = 0
vanBenefit = 0
if van == True:
    if vanEmissions > 0:
        vanBenefit = 3350 * vanMonths/12
    else:
        vanBenefit = 1340 * vanMonths/12
vanFuelBenefit = 633 * vanMonths/12

#ASSETS AVAILABLE FOR PRIVATE USE
privateAssetMonths = 12
privateAssetEmployeeContribution = 0
privateAssetBenefit = 0
privateAssetMarketValue = 0
privateAssetAnnualValue = privateAssetMarketValue * 0.2
if privateAssetMarketValue >= privateAssetAnnualValue: #Benefit is higher of market value and annual value
    privateAssetBenefit = privateAssetMarketValue * privateAssetMonths/12 - privateAssetEmployeeContribution
else: #Benefit is higher of market value and annual value
    privateAssetBenefit = privateAssetAnnualValue * privateAssetMonths/12 - privateAssetEmployeeContribution



taxableBenefits = cashVouchers + creditTokens + goodsVouchers + accomodationBenefit + carBenefit + fuelBenefit + vanBenefit + vanFuelBenefit + privateAssetBenefit
print(f"Total taxable benefits is: £{taxableBenefits}")

employmentIncome = generalEarnings + taxableBenefits
print(f"Employment income is: £{employmentIncome}")