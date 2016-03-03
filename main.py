import argparse
from steepestAscent import SteepestAscent
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
                        choices=['steepestAscent'],
                        help='mode of working',
                        default='steepestAscent')
    parser.add_argument('-n',
                        '--numsteps',
                        type=int,
                        default=14000,
                        help='number of steps')
    parser.add_argument('-r',
                        '--restarts',
                        type=int,
                        default=40,
                        help='number of restarts')
    # Array for all arguments passed to script
    args = parser.parse_args()
    if args.mode == "decrypt":
        if args.plugin == "steepestAscent":
            cracker = SteepestAscent(inp=args.input,
                                     out=args.output,
                                     numSteps=args.numsteps,
                                     restarts=args.restarts)
            print('-' * 60)
            decrypted = cracker.crack()
            with open(str(args.output), "w") as text_file:
                text_file.write(decrypted)
            print(decrypted)
            print('-' * 60)
            print(
                "other possiblities have been written to decrypt/possiblities.txt")
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
