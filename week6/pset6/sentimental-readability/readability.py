from cs50 import get_string


def main():
    # Input text from user
    usertext = get_string("Text:")
    letters = count_letters(usertext)
    words = count_words(usertext)
    sentences = count_sentences(usertext)
    # Average number of letters per 100 words in the text
    L = letters / words * 100.0
    # Average number of sentences per 100 words in the text
    S = sentences / words * 100.0
    # Coleman-Liau index for grades
    grade = 0.0588 * L - 0.296 * S - 15.8
    # Output grade level
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(grade)}")


def count_letters(usertext):
    text = ""
    for character in usertext:
        if character.isalpha():
            text += character
    letters = len(text)
    return letters


def count_words(usertext):
    word_list = usertext.split()
    number_of_words = len(word_list)
    return number_of_words

    
def count_sentences(usertext):
    characters = ['!', '.', '?']
    sentences = 0
    for i in range(3):
        sentences += usertext.count(characters[i])
    return sentences


if __name__ == "__main__":
    main()