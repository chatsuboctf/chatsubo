import string
import random


def randstr(length=8):
    """
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    """

    letters = string.ascii_letters
    numbers = string.digits
    punctuations = string.punctuation

    dico = list(f'{letters}{numbers}{punctuations}')
    random.shuffle(dico)

    blob = ''.join(random.choices(dico, k=length))
    return blob
