from decryptor import ALPHABET, LETTERFREQ, OPTIMAL, SubstitutionDecryptor
# import collections
from random import randint
import operator
import re
from collections import Counter

__author__ = "Abouzar Parvan <abzcoding@gmail.com>"


class Alephba(object):
    def __init__(self, ch, level):
        self.character = ch
        self.level = level
        self.possible = []

    def getCandidate(self):
        allofthem = self.possible
        if self.level > 9:
            return Counter(allofthem).most_common(1)[0][0]
        if len(self.possible) < 2:
            return None
        allmost = Counter(allofthem).most_common(2)
        if len(allmost) > 2:
            (key, val) = allmost[randint(0, 2)]
        else:
            (key, val) = Counter(allofthem).most_common(1)[0]
        if self.level == 1:
            if val > 1:
                return key
        elif self.level == 2:
            if val > 2:
                return key
        elif self.level == 3:
            if val > 2:
                return key
        elif self.level == 4:
            if val > 3:
                return key
        elif self.level > 4:
            if val > 3:
                return key
        return None

    def __repr__(self):
        return "{[" + self.character + "] : " + str(self.possible) + "}"


class FrequencyCounter(SubstitutionDecryptor):
    def __init__(self, inp=None, out=None, numSteps=1):
        SubstitutionDecryptor.__init__(self)
        self.input = inp
        self.level = numSteps
        newlines = ''
        with open(self.input, 'r') as in_file:
            for line in in_file.readlines():
                newlines += line
            newlines = self.preProcessMessage(newlines)
            self.frequency = Counter(newlines)

    def crack(self):
        newlines = ''
        with open(self.input, 'r') as in_file:
            for line in in_file.readlines():
                newlines += line
        charObj = []
        res = []
        for ch in ALPHABET:
            temp = Alephba(ch, self.level)
            charObj.append(temp)
            res.append(ch)
        if self.level > 1:
            all_words = ''.join(re.findall(' [a-z]+', newlines.lower()))
            threeLetter = []
            twoLetter = []
            fourLetter = []
            if self.level > 5:
                tln = ["of", "the", "to", "and", "our", "their", "has", "for",
                       "in", "them", "these", "by", "that", "have", "as",
                       "all"]
                tl4 = ["them", "that", "have", "with", "laws", "they", "from",
                       "most"]
                tl3 = ["the", "and", "our", "for", "has", "all", "his", "are",
                       "his", "new"]
                tl2 = ["of", "to", "in", "by", "us", "is", "be", "we", "on",
                       "it", "an", "as", "at"]
            else:
                tln = ["The", "of", "and", "to", "in", "a", "is", "that", "be",
                       "it", "by", "are", "for", "was", "as", "he", "with",
                       "on", "his", "at", "which", "but", "from", "has",
                       "this", "will", "one", "have", "not", "were", "or",
                       "all", "their", "an", "I", "there", "been", "many",
                       "more", "so", "when", "had", "may", "today", "who",
                       "would", "time", "we", "about", "after", "dollars",
                       "if", "my", "other", "some", "them", "being", "its",
                       "no", "only", "over", "very", "you", "into", "most",
                       "than", "they", "day", "even"]
                tl4 = ["that", "with", "have", "this", "will", "your", "from",
                       "they", "know", "want", "been", "good", "much", "some",
                       "when"]
                tl3 = ["the", "and", "for", "are", "but", "not", "you", "all",
                       "any", "can", "had", "her", "was", "one", "our", "out",
                       "day", "get", "has"]
                tl2 = ["of", "to", "in", "it", "is", "be", "as", "at", "so",
                       "we", "he", "by", "or", "on", "do", "if", "me", "my",
                       "up", "an", "go", "no", "us", "am"]
            text = all_words.split(' ')
            new_text = []
            for txt in text:
                if len(txt) > 1:
                    new_text.append(txt)
            for word in text:
                if len(word) == 2:
                    twoLetter.append(word)
                elif len(word) == 3:
                    threeLetter.append(word)
                elif len(word) == 4:
                    fourLetter.append(word)
            j = 0
            sorted_all = Counter(new_text).most_common()
            sorted_4 = Counter(fourLetter).most_common()
            sorted_3 = Counter(threeLetter).most_common()
            sorted_2 = Counter(twoLetter).most_common()
            j = 0
            for (key, value) in sorted_all:
                old_j = j
                while len(key) != len(tln[j]):
                    j = j + 1
                    if j == len(tln) - 1:
                        break
                if j == len(tln) - 1:
                    break
                for idx, ch in enumerate(key):
                    if self.level > 4 and self.level < 10:
                        charObj[ord(ch) - 97].possible.append(tln[j][idx])
                j = old_j + 1
            j = 0
            for (key, value) in sorted_4:
                for idx, ch in enumerate(key):
                    if self.level > 3 and self.level < 10:
                        charObj[ord(ch) - 97].possible.append(tl4[j][idx])
                j = j + 1
                if j == len(tl4):
                    break
            j = 0
            for (key, value) in sorted_3:
                for idx, ch in enumerate(key):
                    if self.level > 2 and self.level < 10:
                        charObj[ord(ch) - 97].possible.append(tl3[j][idx])
                j = j + 1
                if j == len(tl3):
                    break
            j = 0
            for (key, value) in sorted_2:
                for idx, ch in enumerate(key):
                    if self.level > 1 and self.level < 10:
                        charObj[ord(ch) - 97].possible.append(tl2[j][idx])
                j = j + 1
                if j == len(tl2):
                    break
        sorted_1 = sorted(self.frequency.items(),
                          key=operator.itemgetter(1),
                          reverse=True)
        i = 0
        for (key, value) in sorted_1:
            if self.level > 9:
                charObj[ord(key) - 97].possible.append(OPTIMAL[i])
            else:
                charObj[ord(key) - 97].possible.append(LETTERFREQ[i])
            i = i + 1
        for char in charObj:
            candid = char.getCandidate()
            if candid is not None:
                res[ord(char.character) - 97] = candid
        kelid = ''
        for ch in res:
            kelid += ch
        from string import maketrans
        trantab = maketrans(ALPHABET, kelid)
        result = newlines.translate(trantab)
        return result
