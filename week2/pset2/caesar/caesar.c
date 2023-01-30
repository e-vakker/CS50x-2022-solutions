#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Check the number of arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Check the argument are digit
    else if (only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Get input from user for encryption
    string plaintext = get_string("plaintext: ");
    // Output cipher text
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        printf("%c", rotate(plaintext[i], atoi(argv[1])));
    }
    printf("\n");
    return 0;
}

// Function to check the argument contains only digits
bool only_digits(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isdigit(s[i]))
        {
            // Continued loop
        }
        else
        {
            return false;
        }
    }
    return true;
}

// Encryption every char from plain text
char rotate(char c, int n)
{
    if (isalpha(c) && isupper(c))
    {
        c = ((c - 65 + n) % 26) + 65;
        return c;
    }
    else if (isalpha(c) && islower(c))
    {
        c = ((c - 97 + n) % 26) + 97;
        return c;
    }
    else
    {
        return c;
    }
}