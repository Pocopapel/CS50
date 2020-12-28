from sys import exit

cc = (input("enter creditcard number: "))
cclen = len(cc)
sumcheck = 0
doubledigit = 0

# get every second number starting at the 2nd rightmost nr, add and multiply by 2
for num in range(cclen - 2, -1, -2):
    if (int(cc[num]) * 2) < 10:
        sumcheck += int(cc[num]) * 2
    else:
        # if > 10 the first digit is a 1, add this and the decimal
        doubledigit = (int(cc[num]) * 2) % 10
        doubledigit += 1
        sumcheck += doubledigit
# get all other numbers and add them
for num in range(cclen - 1, -1, -2):
    sumcheck += int(cc[num])
succes = False
# check if Luhns algorithm is true, as in the last number is a 0, else print invalid and exit

if (sumcheck % 10 == 0):
    if int(cc[1]) == 4 or int(cc[1]) == 7:
        print("AMEX")
        succes = True
    if cclen == 16 and int(cc[0]) == 5:
        if int(cc[1]) in (1, 2, 3, 4, 5):
            print("MASTERCARD")
            succes = True
    if cclen == 13 or cclen == 16:
        if int(cc[0]) == 4:
            print("VISA")
            succes = True
if succes == False:
    print("INVALID")