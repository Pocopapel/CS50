//start commands that load programs
#include <cs50.h>
#include <stdio.h>
#include <math.h>
int main(void)
{
    // coins we are using and the counter
    int quarter;
    int dime;
    int fiver;
    int cent;
    int counter = 0;

    float change;
    //ask for the amount of change and make sure it repeats when number is negative
    do
    {
        change = get_float("amount of change owed in dollars:");
    }
    while (change < 0);
    // change dollars to pennies
    int pennies = round(change * 100);
    // check for coins
    for (quarter = 1; pennies >= 25 ; quarter++)
    {
        pennies -= 25;
        counter += 1;
    }
    for (dime = 1; pennies >= 10; dime++)
    {
        pennies -= 10;
        counter += 1;
    }
    for (fiver = 1; pennies >= 5; fiver++)
    {
        pennies -= 5;
        counter += 1;
    }
    for (cent = 1; pennies >= 1; cent++)
    {
        pennies -= 1;
        counter += 1;
    }
    // say number of change coins
    printf("You have to give back %i coins\n", counter);
}