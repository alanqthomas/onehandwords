import sys, argparse, re

def main(argv):
	# Letters mapped to finger number
	leftHand = {
	'q': 1, 'a': 1, 'z': 1,
	'w': 2, 's': 2, 'x': 2,
	'e': 3, 'd': 3, 'c': 3,
	'r': 4, 'f': 4, 'v': 4,
	't': 4, 'g': 4, 'b': 4
	}

	rightHand = {
	'y': 1, 'h': 1, 'n': 1,
	'u': 1, 'j': 1, 'm': 1,
	'i': 2, 'k': 2,
	'o': 3, 'l': 3,
	'p': 4
	}

	# Argument handling
	parser = argparse.ArgumentParser(
	description='Finds all words that can be typed using one hand with no finger used consecutively.',
	prog="OneHandWords"
	)
	parser.add_argument('inputFile', help='Words to parse')
	parser.add_argument('outputFile', help='Destination for results')
	parser.add_argument('--exclude', '-e', nargs='+', help='Characters to exclude')
	parser.add_argument('--right', '-r', action='store_true', help='Generate words for right hand')
	parser.add_argument('--comma', '-c', action='store_true', help='Specify that words are separated by commas instead of new lines')
	parser.add_argument('--allowConsecutive', '-a', action="store_true", help='Allow the same finger to be use consecutively when typing a word')
	parser.add_argument('--version', '-v', action="version", version='%(prog)s 0.1')
	args = parser.parse_args()

	# Open file and create list of words
	with open(args.inputFile, 'r') as f:
		if args.comma:
			content = f.readlines()
			if not content:
				sys.exit("ERROR: Input file is empty")

			words = content[0].split(",")
		else:
			words = f.read().splitlines()
			if not words:
				sys.exit("ERROR: Input file is empty")

	# Set the finger mapping
	if args.right:
		fingers = rightHand
		offHand = leftHand
	else:
		fingers = leftHand
		offHand = rightHand

	# Remove words containing letters of the offhand
	for finger in offHand:
		words = [word for word in words if not finger in word]

	# Remove words containing the letters the user requested to remove
	if args.exclude is not None:
		for letter in args.exclude:
			words = [word for word in words if not letter in word]

	with open(args.outputFile, 'w') as f:
		# Write unique finger words to file
		for word in words:
			if args.allowConsecutive:
				f.write(word + "\n")
			elif uniqueFingers(word, fingers):
				f.write(word + "\n")

	return 0

# Determines whether a word can be typed without using the same
# finger for 2 consecutive letters
def uniqueFingers(word, fingers):

	# Check is word contains only letters
	if not word.isalpha():
		return False

	word = word.lower()
	currentFinger = fingers[word[0]];

	for i in range(1, len(word)):
		if currentFinger != fingers[word[i]]:
			currentFinger = fingers[word[i]]
		else:
			return False

	return True

if __name__ == "__main__":
   main(sys.argv[1:])
