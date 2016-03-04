import argparse
from steepestAscent import SteepestAscent
from frequency import FrequencyCounter
from decryptor import SubstitutionDecryptor, ALPHABET
__author__ = "Abouzar Parvan <abzcoding@gmail.com>"


def main():
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description="Script to Crack mr. Franklin's encryption")
    # Add arguments
    parser.add_argument('-i',
                        '--input',
                        default='files/in.txt',
                        help="input file")
    parser.add_argument('-o',
                        '--output',
                        default='files/out.txt',
                        help="output file")
    parser.add_argument('-m',
                        '--mode',
                        choices=['encrypt', 'decrypt'],
                        help='mode of working',
                        required=True)
    parser.add_argument('-p',
                        '--plugin',
                        choices=['steepestAscent', 'frequency'],
                        help='mode of working',
                        default='steepestAscent')
    parser.add_argument('-n',
                        '--numsteps',
                        type=int,
                        default=7000,
                        help='number of steps')
    parser.add_argument('-r',
                        '--restarts',
                        type=int,
                        default=20,
                        help='number of restarts')
    parser.add_argument('-v',
                        '--verbose',
                        action="store_true",
                        help="increase output verbosity")
    # Array for all arguments passed to script
    args = parser.parse_args()
    if args.mode == "decrypt":
        if args.plugin == "steepestAscent":
            cracker = SteepestAscent(inp=args.input,
                                     out=args.output,
                                     numSteps=args.numsteps,
                                     restarts=args.restarts)
        elif args.plugin == "frequency":
            cracker = FrequencyCounter(inp=str(args.input),
                                       numSteps=args.numsteps)
        if args.verbose:
            print('-' * 60)
        decrypted = cracker.crack()
        with open(str(args.output), "w") as text_file:
            text_file.write(decrypted)
        if args.verbose:
            print(decrypted)
            print('-' * 60)
        print("=" * 60)
        print("result have been written to " + str(args.output))
        if args.plugin == "steepestAscent":
            print(
                "other possiblities have been written to decrypt/possiblities.txt")
        print("=" * 60)
    else:
        coder = SubstitutionDecryptor()
        with open(str(args.input), 'r') as in_file:
            content = in_file.read()
            content = content.lower()
            shfled = coder.shuffler(ALPHABET)
            content = coder.encrypt(content, shfled)
        for i in range(len(shfled)):
            print(ALPHABET[i] + " => " + shfled[i])
        with open(str(args.output), "w") as text_file:
            text_file.write(content)


if __name__ == "__main__":
    main()
