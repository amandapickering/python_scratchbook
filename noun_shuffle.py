from textblob import TextBlob
from textblob.taggers import NLTKTagger
import random
from sys import argv
import sys

def make_pos_dict(text):
	nltk_tagger = NLTKTagger()
	blob = TextBlob(text, pos_tagger=nltk_tagger)
	pos_words = dict(blob.pos_tags)
	return pos_words

def get_nouns(posword_dict):
	nouns = [str(k) for k, v in posword_dict.iteritems() if (v == u'NNP' or v == u'NN' or v == u'NNS' or v == u'NNPS')]
	return nouns

def get_indices(token_list, noun_list):
	indices = []
	for i in token_list:
		if i in noun_list:
			indices.append(token_list.index(i))
	return indices

def shuffle_nouns(text_file):
	with open(text_file) as f:
		text = ' '.join(f.readlines())
		blob = TextBlob(text)
		tokens = list(blob.words) #cast WordList as a list
		pos_text = make_pos_dict(text)
		nouns = get_nouns(pos_text) #this is a list
		extra_nouns = nouns[:] #for when a noun occurs more than once
		noun_indices = get_indices(tokens, nouns)
		random.shuffle(nouns)
		random.shuffle(extra_nouns)
		for index in noun_indices:
			if nouns:
				tokens[index] = nouns[random.randint(0, len(nouns) - 1)]
			elif extra_nouns:
				tokens[index] = extra_nouns[random.randint(0, len(nouns) - 1)]
		return (' '.join(tokens)).lower()

if __name__ == '__main__':
	args = argv[:]
	try:
		input_file = args[1]
	except IndexError:
		print 'usage: python noun_shuffle.py file.txt'
		sys.exit()
	print shuffle_nouns(input_file)
