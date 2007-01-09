#$ neutron_plugin 01

import urllib

QUOTE_FILE = 'static/quotes.txt'

def handler_quote_quote(type, source, parameters):
	reply = random.choice(open(QUOTE_FILE, 'r').readlines()).strip()
	smsg(type, source, reply)

def handler_quote_fortune(type, source, parameters):
	reply = urllib.urlopen('http://www.hypothetic.org/fortune.php').read()[:2000]
	smsg(type, source, reply)

register_command_handler(handler_quote_quote, '!quote', 0, 'Gives a random quote.', '!quote', ['!quote'])
register_command_handler(handler_quote_fortune, '!fortune', 0, 'Gives a random fortune.', '!fortune', ['!fortune'])
