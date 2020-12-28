from cs50 import get_float

while True:
    totalowed = get_float("how much is owed: ##.##?:")
    if (totalowed >= 0):
        break
totalcents = int(totalowed * 100)

owedtmp = totalcents
quarters = 0
dimes = 0
nickels = 0
pennies = 0
i = 0
while owedtmp >= 25:
    quarters += 1
    owedtmp -= 25
while owedtmp >= 10:
    dimes += 1
    owedtmp -= 10
while owedtmp >= 5:
    nickels += 1
    owedtmp -= 5
while owedtmp >= 1:
    pennies += 1
    owedtmp -=1
coinsneeded = quarters + dimes + nickels + pennies
print("coins needed:", coinsneeded)
print("quarters:", quarters)
print("dimes:", dimes)
print("nickels:", nickels)
print("pennies:", pennies)

