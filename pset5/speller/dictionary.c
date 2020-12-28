// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <math.h>


#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65536;
// Hash table
node *table[N];

//set counter for the amount of words loaded
int wordcount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //create a copy of the word
    int length = strlen(word);
    char copy[LENGTH + 1];
    for (int i = 0; i < length; i++)
    {
        copy[i] = tolower(word[i]);
    }
    // create the end of the string
    copy[length] = '\0';
    // hash the word
    int h = hash(copy);
    // set pointer to the beginning of the hashtable
    node *cursor = table[h];

    //search the dictionary untill the word is found or the pointer points to null (end of the table) in which case the word isnt in the dict
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, copy) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hash provided by https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/ user delipity
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char word [LENGTH + 1];
    // scan until the end of the file
    while (fscanf(file, "%s", word) != EOF)
    {
        // give memory
        node *n = malloc(sizeof(node));
        // included to not give valgrind memory error
        memset(n, 0, sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);

        // hash the word
        int h = hash(n->word);

        node *head = table[h];
        if (head == NULL)
        {
            table[h] = n;
            wordcount ++;

        }
        else
        {
            n->next = table[h];
            table[h] = n;
            wordcount ++;
        }

    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *tmp;
    node *cursor;
    // repeats for every index in the table
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            continue;
        }
        cursor = table[i];
        tmp = cursor;

        // until the end of the list keeps freeing the memory allocated in load
        while (cursor->next != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
        free(cursor);
    }
    return true;
}

