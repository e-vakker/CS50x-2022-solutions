// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100;

// Numbers of words

int number_of_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int id_hash = hash(word);
    node *cursor = table[id_hash];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Improve this hash function
    return ((int)toupper(word[0]) + (int)toupper(word[1]) + (int)toupper(word[2])) % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dictionary_file = fopen(dictionary, "r");
    if (dictionary_file == NULL)
    {
        printf("Error 1\n");
        return false;
    }
    // Buffer for word
    char buffer[LENGTH + 1];
    // Read string from file
    while (fscanf(dictionary_file, "%s", buffer) != EOF)
    {
        // New node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Error 2");
            return false;
        }
        strcpy(n->word, buffer);
        n->next = NULL;
        int id_hash = hash(n->word);
        n->next = table[id_hash];
        table[id_hash] = n;
        number_of_words++;
    }
    fclose(dictionary_file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return number_of_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = NULL;
        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
