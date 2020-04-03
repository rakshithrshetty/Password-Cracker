import hashlib
import time


def hash_md5(inp):
    hash_value = hashlib.md5(inp.encode())
    return hash_value.hexdigest()


def dictionary(dictionary_file, input_hash):
    with open(dictionary_file, 'r+') as f:  # opening the wordlist
        attempts = 0
        start = time.time()
        for line in f:
            attempts += 1
            line = line.rstrip('\n')    # removing the newline character
            print('trying password', line)
            line1 = hash_md5(line)  # hashing the password from the wordlist
            if line1 == input_hash:
                print('\n\nThe password is {}. Found in {} guesses.'.format(line, attempts))
                end = time.time()   # calculating the time required for execution
                print('Time required in secs for cracking the password is', end - start)
                exit(0)
        print('\n\nNo matches found')
        end = time.time()
        print('time required in secs is', end - start)
        exit(0)


def combine(*args, **kwds):
    def generate(values, uppper):
        for init in uppper:       # move though all the first levels
            for present in values:   # again iterate through current level
                yield init + (present,)
    iter_list = iter(((),))
    for level in tuple(map(tuple, args)) * kwds.get('repeat', 1):   # generate tuples out of string of characters which are again converted back to tuples
        iter_list = generate(level, iter_list)  # build a list of base iterators over which other characters will iterate through
    return iter_list


def bruteforce_simple(input_hash):
    attempts = 0
    chars = 'abcdefghijklmnopqrstuvwxyz' #string of all the characters that we are iterating over
    start = time.time()
    for i in range(1, 9):
        for test in combine(chars, repeat=i):
            test = ''.join(test) #combining two of more tuples to form a string
            attempts += 1
            test1 = hash_md5(test)
            if test1 == input_hash: #trying to match the hash of the generated password with the input hash
                end = time.time()
                print('Time required in secs for cracking the password is', end - start)
                return 'The password is {}. Found in {} guesses.'.format(test, attempts)


def bruteforce_complex(input_hash):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&' + '()*+,-./:;<=>?@[\]^_`{|}~' #string of all the characters that we are iterating over
    attempts = 0
    start = time.time()
    for i in range(1, 9):
        for test in combine(chars, repeat=i):
            test = ''.join(test)  #combining two of more tuples to form a string
            attempts += 1
            test1 = hash_md5(test)
            if test1 == input_hash: #trying to match the hash of the generated password with the input hash
                end = time.time()
                print('Time required in secs for cracking the password is', end - start)
                return 'The password is {}. Found in {} guesses.'.format(test, attempts)
#            print(guess, attempts)


if __name__ == '__main__':
    default_dictionary = 'dict.txt'
    input_hash = input('Enter the MD5 hash of the password to be cracked\n')
    print('The Password Cracker has two options for Attack\n'
          '1.   Dictionary Attack\n'
          '2.   Brute Force Attack\n')
    user_options = ['1', '2']
    user_input1 = input("Select one by entering 1 or 2\n")
    while user_input1 not in user_options:
        print("Please try again")
        user_input1 = input("Select one by entering 1 or 2\n"
                            "1 is for Dictionary Attack\n"
                            "2 is for Brute Force Attack\n")
    if user_input1 == '1':
        user_input2 = input('Please enter 1 for using your Wordlist, or 2 for using the default wordlist\n')
        while user_input2 not in user_options:
            print("Please try again")
            user_input2 = input("Select one by entering 1 or 2\n"
                                "1 is for using custom wordlist\n"
                                "2 is for using the default wordlist\n")
        if user_input2 == '1':
            filename = input('Enter the wordlist file name\n')
            dictionary(filename, input_hash)
        else:
            dictionary(default_dictionary, input_hash)
    else:
        print('Select the type of the password that is to be cracked\n'
              '1.   Simple Password (only lower case alphabets)\n'
              '2.   Complex Password(all possible combinations)\n')
        user_input3 = input("Select one by entering 1 or 2\n")
        while user_input3 not in user_options:
            print("Please try again")
            user_input3 = input("Select one by entering 1 or 2\n"
                                "1 is for Simple Password (only lower case alphabets)\n"
                                "2 is for Complex Password(all possible combinations)\n")
        if user_input3 == '1':
            print('Trying to crack the password...')
            print(bruteforce_simple(input_hash))
            exit(0)
        else:
            print('Trying to crack the password...')
            print(bruteforce_complex(input_hash))
            exit(0)
