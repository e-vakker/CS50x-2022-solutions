import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")
    elif sys.argv[1].endswith('.csv') == False:
        sys.exit("Usage: python dna.py DATA.CSV sequence.txt")
    elif sys.argv[2].endswith('.txt') == False:
        sys.exit("Usage: python dna.py data.csv SEQUENCE.TXT")

    # TODO: Read database file into a variable
    people = []
    header = []

    with open(sys.argv[1], "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        header.remove("name")
        for row in reader:
            people.append(row)
        file.close()

    # TODO: Read DNA sequence file into a variable
    DNA = ""

    with open(sys.argv[2], "r") as file:
        DNA = file.read()
        file.close()

    # TODO: Find longest match of each STR in DNA sequence
    STR = []
    STR.append("Index")
    for i in range(len(header)):
        buffer = longest_match(DNA, header[i])
        STR.append(buffer)

    # TODO: Check database for matching profiles
    for person in range(len(people)):
        count = 0
        for indexSTR in range(1, len(header) + 1):
            a = people[person][indexSTR]
            b = STR[indexSTR]
            if int(a) == int(b):
                count += 1
            if count == len(header):
                sys.exit(people[person][0])
    sys.exit("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
