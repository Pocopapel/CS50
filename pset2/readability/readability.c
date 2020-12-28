#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

//counters
int letters = 0;
int words = 1;
int sentences = 0;

int main(void)
{
    //get the text
    string text = get_string("Text:");

    //count letters
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            letters++;
        }
        //count words
        else if (text[i] == ' ')
        {
            words++;
        }
        //count sentences
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    //print words etc
    printf("letters: %i \ n", letters);
    printf("words: %i \ n", words);
    printf("sentences: %i \ n", sentences);

    // get the index
    float clindex = 0.0588 * (100 * (float) letters / (float) words) - 0.296 * (100 * (float) sentences / (float) words) - 15.8;

    // round the number
    int grade = round(clindex);

    // print the grades
    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}
