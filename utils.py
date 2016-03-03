#!/usr/bin/python
__author__ = "Abouzar Parvan <abzcoding@gmail.com>"
import math
from decryptor import ProbabilityCalculator

wordPossibility = ProbabilityCalculator('dictionaries/kalame.txt')


def wordSeqFitness(words):
    return sum(math.log10(wordPossibility(w)) for w in words)


def memoize(f):
    cache = {}

    def memoizedFunction(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    memoizedFunction.cache = cache
    return memoizedFunction


@memoize
def segment(word):
    if not word:
        return []
    word = word.lower()  # change to lower case
    allSegmentations = [[first] + segment(rest)
                        for (first, rest) in splitPairs(word)]
    return max(allSegmentations, key=wordSeqFitness)


def splitPairs(word, maxLen=20):
    return [(word[:i + 1], word[i + 1:]) for i in range(max(
        len(word), maxLen))]


@memoize
def segmentWithProb(word):
    segmented = segment(word)
    return (wordSeqFitness(segmented), segmented)
