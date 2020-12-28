#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, char *argv[])
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
    for (int i = 0; i < 26; i++)
    {
        temp = argv[1][i];
        for (int j = i + 1; j < 26; j++)
        {
            if (temp == argv[1][j] || temp == argv[1][j] + 32 || temp == argv[1][j] - 32)
            {
                printf("no repeated characters please \n");
                return 1;
            }
        }
    }
    //save the cypher
    char cypher[26];
    for (int i = 0; i < 26; i++)
    {
        cypher[i] = toupper(argv[1][i]);
    }

    printf("%s\n", cypher);
    // get the plaintext as input and save the length
    string plaintext = get_string("enter plaintext here:");
    int length = strlen(plaintext);

    //declare normal alphabet
    char normalph[26];
    for (int i = 0; i < 26; i++)
    {
        normalph[i] = (65 + i);
    }

    //free space for the encrypted message
    char *newmessage = malloc(length * sizeof(char));

    for (int i = 0; i < length; i++)
    {
        for (int j = 0; j < 26; j++)
        {
            // check which letter of the alphabet it is, take corresponding letter of the cypher and use it in new message
            if (isupper(plaintext[i]))
            {
                if (plaintext[i] == normalph[j])
                {
                    newmessage[i] = toupper(cypher[j]);
                }

            }
            else if (islower(plaintext[i]))
            {
                if (plaintext[i] == tolower(normalph[j]))
                {
                    newmessage[i] = tolower(cypher[j]);
                }
            }
            else
            {
                newmessage[i] = plaintext[i];
            }
        }
    }
    //print encrypted message and free the space
    printf("ciphertext: %s\n", newmessage);
    free(newmessage);
}