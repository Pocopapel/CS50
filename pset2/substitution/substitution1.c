#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    // make sure the user gives a cypher
    if (argc != 2)
    {
        printf("usage ./substitution cyper\n");
        return 1;
    }
    // make sure there are 26 letters, as in the entire alphabet
    if (strlen(argv[1]) != 26)
    {
        printf("key needs to be 26 letters\n");
        return 1;
    }
    // make sure no characters get repeated
    char temp;
    for (int i = 0; i < 27; i++)
    {
        temp = argv[1][i];
        for (int j = i+1; j < 27; j++)
        {
            if (temp == argv[1][j] || temp == argv[1][j] + 32 || temp == argv[1][j] - 32)
            {
                printf("no repeated characters please \n");
                return 1;
            }
        }
    }
    //save the cypher
    char cypher[27];
    for (int i = 0; i < 27; i++)
    {
        cypher[i] = toupper(argv[1][i]);
    }

    printf("%s\n", cypher);
    // get the plaintext as input and save the length
    string plaintext = get_string("enter plaintext here:");
    int length = strlen(plaintext);

    //declare normal alphabet
    char normalph[27];
    for (int i = 0; i < 27; i++)
    {
        normalph[i] = (65 + i);
    }

    // get difference between cypher and alphabet
    char diff[27];
    for(int i = 0; i < 27; i++)
    {
        diff[i] = cypher[i] - normalph[i];
    }
    printf("%s\n", diff);

    char newmessage[length];
    for(int i = 0; i < length; i++)
    {
        if (isupper(plaintext[i]))
        {
            newmessage[i] = plaintext[i] + diff[i];
        }
        if (islower(plaintext[i]))
        {
            newmessage[i] = plaintext[i] + diff[i] + 32;
        }
        else
        {
            newmessage[i] = plaintext[i];
        }
    }
    printf("%s\n", newmessage);
}