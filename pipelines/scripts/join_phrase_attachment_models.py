"""
Usage:
	join_phrase_attachment_models.py <modelfile>...
"""
from docopt import docopt
from pipelines.formats.PhraseAttachments import PhraseAttachmentModel
from collections import Counter

def main():
	a = docopt(__doc__, version="0.1a")
	
	counts = Counter({})
	for modelfile in a["<modelfile>"]:
		f = open(modelfile, "r")
		model = PhraseAttachmentModel.decode(f.read())
		counts.update(Counter(model.counts))
	totalmodel = PhraseAttachmentModel(counts)
	print totalmodel.encode()	

if __name__ == "__main__":
	main()
