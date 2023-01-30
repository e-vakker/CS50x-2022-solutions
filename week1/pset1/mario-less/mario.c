#include <cs50.h>
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height = 0;
    // Request the pyramid height from the user
    while (height < 1 || height > 8)
    {
        height = get_int("Height: ");
    }
    // Making a pyramid
    for (int width = 1; width <= height; width++)
    {
        // Making a empty symbols
        for (int n = 0; n < height - width; n++)
        {
            printf(" ");
        }
        // Making a # symbols
        for (int j = 0; j < width; j++)
        {
            printf("#");
        }
        // New string and - 1
        printf("\n");
    }
}