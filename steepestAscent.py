#!/usr/bin/python
from tqdm import *  # NOQA
import math
import random
from utils import *  # NOQA
from decryptor import ALPHABET, SubstitutionDecryptor, ProbabilityCalculator

__author__ = "Abouzar Parvan <abzcoding@gmail.com>"


class SteepestAscent(SubstitutionDecryptor):
    def __init__(self,
                 inp=None,
                 out=None,
                 numSteps=14000,
                 restarts=40,
                 pos_file="decrypt/possiblities.txt"):
        SubstitutionDecryptor.__init__(self)
        self.input = inp
        self.output = out
        self.numSteps = numSteps
        self.restarts = restarts
        self.__pos_file = pos_file
        self._possibilities[1] = ProbabilityCalculator(
            'dictionaries/2harfi.txt')
        self._possibilities[2] = ProbabilityCalculator(
            'dictionaries/3harfi.txt')

    def seHarfiProb(self, msg):
        return sum(math.log10(self.possibility(3)(trigram))
                   for trigram in self.letterNpos(msg, 3))

    def localMaximum(self, msg, key, decryptionFitness, numSteps):
        decryption = self.decrypt(msg, key)
        value = decryptionFitness(decryption)
        neighbors = iter(self.neighboringKeys(key, decryption))

        for step in range(numSteps):
            nextKey = neighbors.next()
            nextDecryption = self.decrypt(msg, nextKey)
            nextValue = decryptionFitness(nextDecryption)

            if nextValue > value:
                key, decryption, value = nextKey, nextDecryption, nextValue
                neighbors = iter(self.neighboringKeys(key, decryption))
        return decryption

    def neighboringKeys(self, key, decryptedMsg):
        # an iterator over some neighboring keys, heuristically chosen by
        # repairing uncommon bigrams in the decoded message
        value = self.possibility(2)
        bigrams = sorted(self.letterNpos(decryptedMsg, 2), key=value)

        for c1, c2 in bigrams:
            for a in self.shuffler(ALPHABET):
                if c1 == c2 and value(a + a) > value(c1 + c2):
                    yield self.keySwap(key, a, c1)
                else:
                    if value(a + c2) > value(c1 + c2):
                        yield self.keySwap(key, a, c1)
                    if value(c1 + a) > value(c1 + c2):
                        yield self.keySwap(key, a, c2)

        while True:
            yield self.keySwap(key, random.choice(ALPHABET),
                               random.choice(ALPHABET))

    def crack(self):
        pos_file = file(self.__pos_file, 'w')
        # remove all other alphabetic chars
        # with open(self.input, 'r') as in_file:
        #    content = in_file.read()
        newlines = ''
        with open(self.input, 'r') as in_file:
            for line in in_file.readlines():
                newlines += line
        result = ''
        if len(newlines) == 1:
            newlines.append("DONOTSEARCH")
        for i in range(int(len(newlines) / 100)):
            if (len(newlines) - (i * 100)) < 100:
                content = newlines[i * 100:]
            else:
                content = newlines[i * 100:(i * 100) + 100]
            if content == "DONOTSEARCH":
                continue
            msg = self.preProcessMessage(content)
            localMaxes = []
            startingKeys = [self.shuffler(ALPHABET)
                            for i in range(self.restarts)]
            for i in tqdm(range(len(startingKeys))):
                key = startingKeys[i]
                localMaxes.append(self.localMaximum(msg, key, self.seHarfiProb,
                                                    self.numSteps))
            for x in localMaxes:
                (prob, words) = segmentWithProb(x)
                pos_file.write(str(self.possibility(3)(x)) + str(prob) + str(
                    words))
                pos_file.write("\n")

            prob, words = max(segmentWithProb(decryption)
                              for decryption in localMaxes)
            result += ' '.join(words)
        return result
