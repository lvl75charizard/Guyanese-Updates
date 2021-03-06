from firebase_db import database_read_simplewords

sentence1 = "inpu of in "
sentence2 = "input('sentence2 > ') of in"

match_percentage = 0
percent_of_words_matched = 0


def remove_simple_words(words):
    for simple_word in str(database_read_simplewords().val()).split():
        for word in words:
            # print(simple_word)
            if word.lower() == simple_word.lower():
                words.remove(word)

    return words


def check_match_percent(s1, s2):
    global match_percentage
    # first we find the longest of the two strings
    if len(s1) > len(s2):
        main_string = s1
        other_string = s2
    else:
        main_string = s2
        other_string = s1
    # split into words
    # remove simple words that don't add to story (slightly complicated operation all in one)

    list_of_main_string = remove_simple_words(main_string.split())
    list_of_other_string = remove_simple_words(other_string.split())

    # find the worth of one word
    main_word_worth = round(100 / len(list_of_main_string), 3)
    for main_word in list_of_main_string:

        for other_word in list_of_other_string:
            if other_word.lower() == main_word.lower():
                match_percentage = match_percentage + main_word_worth
                print(f'{other_word} {match_percentage}')

    print(f'Percentage match {match_percentage}%')
    if match_percentage > 30:
        print('This must be a match')
        match_percentage = 0
        return True
    else:
        match_percentage = 0
        # print('Most likely not a match')
        return False


if __name__ == '__main__':
    check_match_percent(sentence1, sentence2)  # This runs the script and takes 2 sentences when its called.
