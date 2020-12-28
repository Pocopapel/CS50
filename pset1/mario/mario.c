#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    // ask user for input on how high (s)he wants the pyramid to be
    do
    {
        height = get_int("height is:");
    }
    while (height < 1 || height > 8);

    // for the entire height print spaces first and then hashes so that the pyramid looks reversed
    for (int i = 0; i < height; i++)
    {
        for (int space = 0; space > i - height + 1; space--)
        {
            printf(" ");
        }
        for (int hash = 0; hash < i + 1; hash++)
        {
            printf("#");
        }
        printf("  ");

        // now print the same but without spaces so that the pyramid mirrors itself
        for (int hash = 0; hash < i + 1; hash++)
        {
            printf("#");
        }
        printf("\n");

    }

}