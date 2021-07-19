import re

def remove(plaintext):

    # replace line breaks with <p>
    plaintext = re.sub(r'\n+','<p>', plaintext)
    # # if <p> is followed by a lower case character
    # # replace <p> with space, keep the lower case character
    plaintext = re.sub(r'<p>([a-z])',r' \g<1>', plaintext)
    # # any <p> left is an actual line break
    plaintext = re.sub(r'<p>',r'\n', plaintext)

    # (\s) Find a space character
    # (?:\n+|\r\n+) Directly followed by any number of linebreaks
    # ** note that ?: indicates "Non-capturing group"
    # ([a-z]|\t[a-z]) Directly followed by a lowercase letter
    # or a tab character + lowercase letter.
    # Remove the linebreaks.
    subst = "\\1\\2"
    plaintext = re.sub(r'(\s)(?:\n+|\r\n+)([a-z]|\t[a-z])', subst, plaintext)

    # (\s) Find a non-space character
    # (?:\n+|\r\n+) Directly followed by any number of linebreaks
    # ([a-z]|\t[a-z]) Directly followed by a lowercase letter
    # or a tab character + lowercase letter.
    # Replace the linebreaks with a single space.
    subst = "\\1 \\2"
    plaintext = re.sub(r'(\S)(?:\n+|\r\n+)([a-z]|\t[a-z])', subst, plaintext)
    return plaintext
