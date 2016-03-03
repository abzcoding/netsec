NetSec
===============

###Background Story

It was dark and quiet , you were heading home. that day was possibly the worst day of your life, because [Mr Franklin][https://en.wikipedia.org/wiki/Benjamin_Franklin] had made you to stay till midnight to finish some works. and now your only hope was to get to bed as soon as possible and finish this day, you were sunk in your thought that they came , they had masks , you couldn’t see their faces , but they didn’t seem friendly , all of a sudden you’ve realized that you’re in big trouble , because they were [Paxton Boys][https://en.wikipedia.org/wiki/Paxton_Boys]!
you fought bravely but briefly!
they had attacked [Mr Franklin][https://en.wikipedia.org/wiki/Benjamin_Franklin] and stole the encrypted text of the [Declaration of Independence][https://en.wikipedia.org/wiki/United_States_Declaration_of_Independence] , but before extracting the key from him , he became Unconscious, so they reached to me to get ahold of the key, they gave a choice ; either decrypt the message , or face a horrible death…



###Your Mission

Your life is at stake! you have to decrypt the message by any means possible!



##Usage

####Help

![help](https://raw.githubusercontent.com/abzcoding/netsec/master/files/help.gif)

```bash
➜ git clone https://github.com/abzcoding/netsec.git
➜ pip install tqdm
➜ python main.py --help
```

####Encryption

for encryption all you need to is to specify the input and output file:

```bash
➜ cat files/in.txt
➜ python main.py -m encrypt -i files/in.txt -o files/out.txt
➜ cat files/out.txt
```

![encrypt](https://raw.githubusercontent.com/abzcoding/netsec/master/files/encrypt.gif)

####Decryption

in order to crack the code there are currently one plugin available:

```bash
➜ cat files/Aldrich_Ames.txt
➜ python main.py -m decrypt -i files/August_Schluga.txt -o files/out.txt -n 14000 -r 40
➜ cat files/out.txt
➜ cat decrypt/possiblities.txt
```

![decrypt](https://raw.githubusercontent.com/abzcoding/netsec/master/files/decrypt.gif)



###Full Options List

- `-h, --help`
  - Get all the help you need
- `-m, --mode {encrypt, decrypt}`
  - Mode of working : either Encryption or Decryption
- `-i, --input [input-file]`
  - Input file for decryption or encryption
- `-o, --output`
  - Output file
- `-p, --plugin {steepestAscent}`
  - plugin to use in decryption , right now only the [Gradient descent][https://en.wikipedia.org/wiki/Gradient_descent] is working
- `-n, --numsteps [7000]`
  - Number of steps that need to be taken before restart
- `-r, --restarts [20]`
  - Specify of restarts.

### License MIT

Project License can be found [here](LICENSE.md)