#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    // argc needs to be 2  //
    if (argc != 2)
    {
        printf("use: ./Caesar key\n");
        exit(1);
    }
    // string argv needs to be a positive int //
    for (int i = 0; i < strlen(argv[1]); i++)
        if (!isdigit(argv[1][i]))
        {
            printf("use: ./Caesar key\n");
            exit(1);
        }
    int key = atoi(argv[1]);
    if (key < 0)
    {
        printf("use: ./Caesar key\n");
        exit(1);
    }
    //get the message which has to be encoded//
    else
    {
        string message = get_string("Enter text to encrypt:");
        // encrypt it & return encrypted message //
        int length = strlen(message);
        printf("ciphertext: ");
        for (int i = 0; i < length; i++)
        {
            if (isupper(message[i]))
            {
                printf("%c", (message[i] + key - 65) % 26 + 65);
            }
            else if (islower(message[i]))
            {
                printf("%c", (message[i] + key - 97) % 26 + 97);
            }
            else
            {
                printf("%c", message[i]);
            }
        }
    }
    printf("\n");
}

