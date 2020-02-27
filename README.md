# HVZ-Text-Alerts
Python 2 script that sends messages through GroupMe when the game server (umbchvz.com) reports deaths. Create a GroupMe developer account, edit the bot id in config.xml, and then run monitor.py to use. Requires Python 2 and shell with the utilities curl and at. Rewritten from Czyryca's HvZ-Text-Alerts program to run in the UMBC GL servers, which do not have access to certain useful packages like Beautiful Soup.

File Overview:

config.py must be edited to include your bot id from dev.groupme.com/bots before the script can run. It contains timing preferences as well.

monitor.py is the main script to be run during weeklongs. It holds the main logic of the program. Currently, messages have no delay by default because the server has a 1 hour delay. 

library.py defines functions used to manipulate data -- it contains no program logic and is separated for testing purposes. test.py contains unit tests for the functions defined in the library.

parser.py contains a parser that separates the data on umbchvz.com/players.php into a dict of key-value pairs "name":"status", but this mwas made obselete by the edits to allow for this program to run without certain packages
