import string
import random
import re
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
LETTERFREQ = "etaoinsrhldcumfpgwybvkxjqz"
OPTIMAL = "etonsairhdlucfmpgwbyvjkxqz"
__author__ = "Abouzar Parvan <abzcoding@gmail.com>"


class SubstitutionDecryptor(object):
    def __init__(self):
        self._possibilities = [0.0, 0.0, 0.0, 0.0, 0.0]

    def possibility(self, length):
        length = length - 1
        if length < len(self._possibilities):
            return self._possibilities[length]

    def letterNpos(self, msg, n):
        return [msg[i:i + n] for i in range(len(msg) - (n - 1))]

    def encrypt(self, msg, key):
        return msg.translate(string.maketrans(ALPHABET, key))

    def decrypt(self, msg, key):
        return msg.translate(string.maketrans(key, ALPHABET))

    def keySwap(self, key, a, b):
        return key.translate(string.maketrans(a + b, b + a))

    def shuffler(self, input_alpha):
        listOfAlpha = list(input_alpha)
        random.shuffle(listOfAlpha)
        return ''.join(listOfAlpha)

    def preProcessMessage(self, chars):
        return ''.join(re.findall('[a-z]+', chars.lower()))

    def crack(self):
        return NotImplementedError


class ProbabilityCalculator(dict):
    def __init__(self, filename):
        self.posCount = 0

        for line in open(filename):
            (word, count) = line[:-1].split('\t')
            self[word] = int(count)
            self.posCount += self[word]

    def __call__(self, key):
        if key in self:
            return float(self[key]) / self.posCount
        else:
            return 1.0 / (self.posCount * (10**(len(key) - 2)))
