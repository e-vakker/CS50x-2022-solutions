# Import library cs50
from cs50 import get_int


# Request the pyramid height from the user
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break
# Loop for mario blocks
width = height - 1
for i in range(1, height + 1):
    print(" " * width, end="")
    print("#" * i, end="")
    width -= 1
    print("")