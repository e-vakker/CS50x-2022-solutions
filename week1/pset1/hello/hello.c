#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("What's your name?\n"); //Request a name
    printf("hello, %s\n", name); // Displaying the welcome message with the name
}