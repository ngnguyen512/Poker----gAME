from project1Aashish import *
from contextlib import redirect_stdout
import io, string

def main():
    getProverbTest()
    printGameTest()
    getChListTest()  
    editHiddenTest()
    checkAndChangeTest()

def checkIfExists(x, output):
    result = falseResult = True
    for element in x:
        if element not in output:
            print(f"\"{element}\" is not present in print output")
            falseResult = False
    return (result and falseResult)

def getTestResult(result, functionName):
    if result == True:
        return f'\u2713 All tests for {functionName}() are passing\n'
    else:
        return f'\u0078 One or more tests for {functionName}() have failed\n'

def getProverbTest():
    print('Starting test for getProverb() function\n')
    f = io.StringIO()
    with redirect_stdout(f):
        print('- Test case 1: standard input')
        print('Expect: retrieve a proverb from list')
        proverb = getProverb()
        print(f'Retrieved \"{proverb}\" from proverb file')
        print('- Test case 2: empty proverbs file')
        print('Expect: console log empty proverb file message')
        proverbEmptyFile = getProverb("proverbsEmpty.txt")
        print('- Test case 3: invalid proverbs file name')
        print('Expect: console log no proverb file found message')
        proverbNoFile = getProverb("invalid_file.txt")
    out = f.getvalue()
    print(out)
    printResult = checkIfExists(["Proverbs file is empty.", "Proverbs file not found."], out)
    with open('proverbs.txt') as f:
        if proverb in f.read() and proverbEmptyFile == proverbNoFile == None and printResult == True:
            testStatus = True
        else:
            testStatus = False
    print(getTestResult(testStatus, 'getProverb'))


def printGameTest():
    print('Starting test for printGame() function\n')
    f = io.StringIO()
    hidden = "hidden"
    wrong = "wrong"
    maxReveals = "maxReveals"
    misses = "misses"
    with redirect_stdout(f):
        print('- Test case 1: standard input')
        print('Expect: console log all provided arguments in correct formatting')
        print('Result:')
        printGame(hidden, wrong, maxReveals, misses)
        print('- Test case 2: empty input for misses parameter')
        print('Expect: console log all provided arguments in correct formatting')
        print('Result:')
        printGame(hidden, wrong, maxReveals, "")
    out = f.getvalue()
    print(out)
    testStatus = checkIfExists([hidden, f"Letter reveals:  {wrong} / {maxReveals}", f"Misses:  m, i, s, s, e, s", "None"], out)
    print(getTestResult(testStatus, 'printGame'))

def getChListTest():
    print('Starting test for getChListTest() function\n')
    result = []
    proverb = [
        "Actions speak louder than words.",
        ""
    ]
    hidden = [
        "~~~~~~~ ~~~~~ ~~~~~~ ~~~~ ~~~~~.", 
        ""
    ]
    expectedResult = [
        ['c', 'i', 'p', 'k', 'l', 'u', 'h', 'w', 't', 'n', 'e', 'd', 'r', 'a', 'o', 's'],
        [],
        [],
        ['c', 'i', 'p', 'k', 'l', 'u', 'h', 'w', 't', 'n', 'e', 'd', 'r', 'a', 'o', 's']
    ]
    print('- Test case 1: standard inputs')
    print('Expect: return character list')
    result.append(getChList(proverb[0], hidden[0]))
    print(f'Result: {result[0]}')
    print('- Test case 2: empty inputs')
    print('Expect: return empty array')
    result.append(getChList(proverb[1], hidden[1]))
    print(f'Result: {result[1]}')
    print('- Test case 3: empty hidden argument')
    print('Expect: return empty array')
    result.append(getChList(proverb[1], hidden[0]))
    print(f'Result: {result[2]}')
    print('- Test case 3: empty proverb argument')
    result.append(getChList(proverb[0], hidden[1]))
    print('Expect: return character list')
    print(f'Result: {result[3]}')
    print(getTestResult(result == expectedResult, 'getChList'))

def editHiddenTest():
    print('Starting test for editHidden() function\n')
    result = []
    print()
    proverb = [
        "Actions speak louder than words.",
        ""
    ]
    hidden = [
        "~~~~~~~ ~~~~~ ~~~~~~ ~~~~ ~~~~~.", 
        ""
    ]
    correct = [
        "s",
        "b"
    ]
    expectedResult = [
        hidden[0],
        "~~~~~~s s~~~~ ~~~~~~ ~~~~ ~~~~s.",
        hidden[0]
    ]
    print('- Test case 1: standard inputs - default letterReveal')
    print('Expect: return hidden proverb with no character reveal')
    result.append(editHidden(proverb[0], hidden[0], correct[0]))
    print(f'Result: {result[0]}')
    print('- Test case 2: standard inputs - letterReveal=True')
    print('Expect: return hidden proverb with character \'s\' reveal')
    result.append(editHidden(proverb[0], hidden[0], correct[0], True))
    print(f'Result: {result[1]}')
    print('- Test case 3: standard inputs - letterReveal=true, correct = character not in proverb')
    result.append(editHidden(proverb[0], hidden[0], correct[1], True))
    print('Expect: return hidden proverb with no character reveal')
    print(f'Result: {result[2]}')
    print(getTestResult(result == expectedResult, 'editHidden'))      

def checkAndChangeTest():
    print('Starting test for checkAndChange() function')
    print('Note: each subsequent test uses outputs obtained from previous test to simulate real-life workflow')
    result = []
    user_input = [
        "s",
        "b",
        "f",
        "p",
        "k"
    ]
    proverb = "Actions speak louder than words."
    hidden = "~~~~~~~ ~~~~~ ~~~~~~ ~~~~ ~~~~~."
    wrong = 0
    misses = []
    expectedResult = [

    ]
    print('- Test case 1: standard input - user_input = character in proverb')
    print(f'Expect: wrong count remains at 0, reveal character \'s\' in hidden proverb (\'{user_input[0]}\')')
    wrong, hidden, misses = checkAndChange(user_input[0], proverb, hidden, wrong, misses)
    print(f"Result: {wrong, hidden, misses}")
    # print('- Test case 2: standard input - user_input = character not in proverb (\'{user_input[1]}\')')
    # print('Expect: wrong count increments by 1, reveal character \'c\' in hidden proverb, append character \'b\' to misses array')
    # wrong, hidden, misses = checkAndChange(user_input[1], proverb, hidden, wrong, misses)
    # print(f"Result: {wrong, hidden, misses}")    
    # print('- Test case 3: standard input - user_input = character not in proverb (\'{user_input[2]}\')')
    # print('Expect: wrong count increments by 1, reveal character \'i\' in hidden proverb, append character \'f\' to misses array')
    # wrong, hidden, misses = checkAndChange(user_input[2], proverb, hidden, wrong, misses)
    # print(f"Result: {wrong, hidden, misses}")    
    # print('- Test case 4: standard input - user_input = character in proverb (\'{user_input[3]}\')')
    # print('Expect: wrong count remains, reveal character \'p\' in hidden proverb')
    # wrong, hidden, misses = checkAndChange(user_input[3], proverb, hidden, wrong, misses)
    # print(f"Result: {wrong, hidden, misses}")  
    # print('- Test case 5: standard input - user_input = character in proverb (\'{user_input[4]}\')')
    # print('Expect: wrong count remains, reveal character \'k\' in hidden proverb')
    # wrong, hidden, misses = checkAndChange(user_input[4], proverb, hidden, wrong, misses)
    # print(f"Result: {wrong, hidden, misses}") 
    print(getTestResult(False, 'checkAndChange'))

if __name__ == "__main__":
    main() 