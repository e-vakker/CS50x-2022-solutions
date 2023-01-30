#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// Functions
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get input user text for grade
    string userText = get_string("Text: ");
    int letters = count_letters(userText);
    int words = count_words(userText);
    int sentences = count_sentences(userText);
    // Average number of letters per 100 words in the text
    float L = (float)letters / (float)words * 100.0;
    // Average number of sentences per 100 words in the text
    float S = (float)sentences / (float)words * 100.0;
    // Coleman-Liau index for grades
    int grade = round(0.0588 * L - 0.296 * S - 15.8);
    // Output grade level
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

// Counting letters with ASCII code in the text
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int letter = toupper(text[i]);
        if (letter >= 65 && letter <= 90)
        {
            letters++;
        }
    }
    return letters;
}

// Counting words with spaces in the text
int count_words(string text)
{
    int words = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }
    return words;
}

// Counting the number of sentences with symbols ! . ?
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}