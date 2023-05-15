import random

def getProverb():
    try:
        with open("proverbs.txt", "r") as f:
            lines = f.readlines()
        if lines:
            a = random.choice(lines).strip()
            return a
        else:
            print("Proverbs file is empty.")
            return None
    except FileNotFoundError:
        print("Proverbs file not found.")
        return None

def printGame(hidden, wrong, maxReveals, misses):
    print(hidden)
    print("Letter reveals: ", wrong, "/", maxReveals)
    print("Misses: ", ', '.join(misses) if misses else "None")
    print()

def getChList(proverb, hidden):
    chDict = {}
    for ch in proverb:
        if ch.isalpha() and ch.lower() not in hidden.lower():
            chDict[ch.lower()] = chDict.get(ch.lower(), 0) + 1
    chList = sorted(chDict, key=chDict.get)
    return chList

def checkAndChange(user_input, proverb, hidden, wrong, misses):
    proverbList = proverb.split()
    proverbList = [word.lower() for word in proverbList]
    user_input = user_input.lower().split()
    hit = False
    for i in user_input:
        if i in proverbList:
            hit = True
            hidden = editHidden(proverb, hidden, i)
        else:
            misses.append(i)
    if not hit:
        ch = getChList(proverb, hidden)[0]
        hidden = editHidden(proverb, hidden, ch, letterReveal = True)
        wrong += 1
    return wrong, hidden


def editHidden(proverb, hidden, correct, letterReveal = False):
    proverb = proverb.split()
    hidden = hidden.split()
    if not letterReveal:
        for i in range(len(proverb)):
            if correct == proverb[i].lower():
                hidden[i] = proverb[i]
        hidden = ' '.join(hidden)
    else:
        proverb = ' '.join(proverb)
        hidden = ' '.join(hidden)
        hidden = list(hidden)
        for i in range(len(proverb)):
            if correct == proverb[i].lower():
                hidden[i] = proverb[i]
        hidden = ''.join(hidden)
    return hidden

def main():
    while True:
        proverb = getProverb()
        if proverb is None:
            return
        if proverb[-1] == '.':
            proverb = proverb[:-1]
        hidden = ''.join(['~' if ch.isalpha() else ch for ch in proverb])
        wrong, maxReveals, misses = 0, len(proverb.split()), []
        while wrong < maxReveals and "~" in hidden:
            printGame(hidden, wrong, maxReveals, misses)
            misses = []
            user_input = input("Guess: ")
            wrong, hidden = checkAndChange(user_input, proverb, hidden, wrong, misses)
        if wrong >= maxReveals:
            print("You have lost this round.")
        else:
            print("Congratulations, you won this round!")
        print("The proverb is:", proverb)
        play_again = input("Play again? (Y/N) ")
        if play_again.lower() != 'y':
            print("ANOTHER TIME")
            break

if __name__ == "__main__":
    main()





