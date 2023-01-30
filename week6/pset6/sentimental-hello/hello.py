# Import library cs50
from cs50 import get_string

# Requesting a user name
answer = get_string("What's your name? ")
# Displaying the welcome message and user name in the console
print("Hello, " + answer)