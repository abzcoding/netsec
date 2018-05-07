NetSec
===============

### Background Story

It was dark and quiet , you were heading home. that day was possibly the worst day of your life, because [Mr Franklin][franklin] had made you to stay till midnight to finish some works. and now your only hope was to get to bed as soon as possible and finish this day, you were sunk in your thought that they came , they had masks , you couldn’t see their faces , but they didn’t seem friendly , all of a sudden you’ve realized that you’re in big trouble , because they were [Paxton Boys][paxton]!
you fought bravely but briefly!
they had attacked [Mr Franklin][franklin] and stole the encrypted text of the [Declaration of Independence][independence], but before extracting the key from him , he became Unconscious, so they reached to me to get ahold of the key, they gave a choice ; either decrypt the message , or face a horrible death…

[franklin]: https://en.wikipedia.org/wiki/Benjamin_Franklin
[paxton]: https://en.wikipedia.org/wiki/Paxton_Boys
[independence]: https://en.wikipedia.org/wiki/United_States_Declaration_of_Independence

### Your Mission

Your life is at stake! you have to decrypt the message by any means possible!



## Usage

please run [test.sh][testbash] for testing:
```bash
bash test.sh
```
[testbash]: https://raw.githubusercontent.com/abzcoding/netsec/master/test.sh
#### Help

![help](https://raw.githubusercontent.com/abzcoding/netsec/master/files/help.gif)

```bash
➜ git clone https://github.com/abzcoding/netsec.git
➜ pip install tqdm
➜ python main.py --help
```

#### Encryption

for encryption all you need to is to specify the input and output file:

```bash
➜ cat files/in.txt
➜ python main.py -m encrypt -i files/in.txt -o files/out.txt
➜ cat files/out.txt
```

![encrypt](https://raw.githubusercontent.com/abzcoding/netsec/master/files/encrypt.gif)

#### Decryption

in order to crack the code there are currently one plugin available:

```bash
➜ cat files/Aldrich_Ames.txt
➜ echo "decryption using steepestAscent"
➜ python main.py -m decrypt -i files/August_Schluga.txt -o files/out.txt -n 14000 -r 40
➜ cat files/out.txt
➜ cat decrypt/possiblities.txt
➜
➜
➜ echo "decrypting the Declaration of Independence using frequency calculation using letter freq"
➜ python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 1
➜ echo "adding two letter words freq"
➜ python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 2
➜ echo "adding three letter words freq"
➜ python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 3
➜ echo "adding four letter words freq"
➜ python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 4
➜ echo "adding optimization!"
➜ python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 11
➜
➜
➜ echo "decrypting the Declaration of Independence using steepestAscent - ( Warning : this will take at least 12 minutes)"
➜ python main.py -m decrypt -p steepestAscent -i files/declaration.txt -o files/out.txt -n 6000 -r 20
```

![decrypt](https://raw.githubusercontent.com/abzcoding/netsec/master/files/decrypt.gif)



### Full Options List

- `-h, --help`
  - Get all the help you need
- `-m, --mode {encrypt, decrypt}`
  - Mode of working : either Encryption or Decryption
- `-i, --input [input-file]`
  - Input file for decryption or encryption
- `-o, --output`
  - Output file
- `-p, --plugin {steepestAscent}`
  - plugin to use in decryption , right now only the [Gradient descent][decent] is working
- `-n, --numsteps [numSteps]`
  - (Number of steps that need to be taken before restart) or (level of frequency {1: '1 lt',2: '1 & 2 lt',... , 11:'optimal'})
- `-r, --restarts [20]`
  - Specify of restarts.
- `-v, --verbose`
  - print out the result

[decent]: https://en.wikipedia.org/wiki/Gradient_descent  
### License MIT

Project License can be found [here](LICENSE.md)
