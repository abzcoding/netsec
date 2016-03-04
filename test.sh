echo "Welcome ... "
echo "Installing tqdm..."
pip install tqdm
echo
echo "For help please head to https://github.com/abzcoding/netsec or run python main.py -h"
echo
echo
read -p "Do you want to decrypt using frequency[ level 1 ]? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "decrypting the Declaration of Independence using frequency calculation using letter freq"
  python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 1
fi
read -p "Do you want to decrypt using frequency[ level 2 ]? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "adding two letter words freq"
  python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 2
fi
read -p "Do you want to decrypt using frequency[ level 3 ]? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "adding three letter words freq"
  python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 3
fi
read -p "Do you want to decrypt using frequency[ level 4 ]? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "adding four letter words freq"
  python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 4
fi
read -p "Do you want to decrypt using frequency[ level 5 ]? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "adding all letter words freq"
  python main.py -m decrypt -p frequency -i files/declaration.txt -o files/out.txt -n 5
fi
read -p "Do you want to decrypt using steepestAscent [ Warning : this might take more than 10 minutes!]? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "adding all letter words freq"
  python main.py -m decrypt -p steepestAscent -i files/declaration.txt -o files/out.txt -n 7000 -r 20
fi
echo
read -p "Do you want to decrypt using cheating!!!!!!!!!? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "adding all letter words freq"
  python main.py -m decrypt -p steepestAscent -i files/declaration.txt -o files/out.txt -n 11
fi
