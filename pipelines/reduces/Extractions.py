import shutil
import os, os.path
from pipelines.formats.Sentences import *
from pipelines.scripts.TER import *

def add_ID_file(item, ID_attr):
	item.set_attribute(ID_attr, item.ID)

def extract_text_from_sent_attr(item, sent_attr, one_per_line = False):
	sents = item.get_attribute(sent_attr, Sentences)
	print sents.get_text(one_per_line=one_per_line)

def extract_generated_info_latex(itemiterator, outfolder):
	#Include-all file
	outfile = os.path.join(outfolder, "outfile.tex")
	inc_f = open(outfile, "wb")
	outimgfolder = os.path.join(outfolder, "images/")
	outtexfolder = os.path.join(outfolder, "tex/")
	try:
		os.makedirs(outimgfolder)
	except OSError as e:
		pass
	try:
		os.makedirs(outtexfolder)
	except OSError as e:
		pass
	
	for item in itemiterator:
		name = item.get_attribute("original_name")
		inc_f.write("%ID "+ str(item.ID)+"\n")
		inc_f.write("\\input{./tex/%s.tex}\n" % (name))

		c_orig = item.get_attribute("txt")
		cap = item.get_attribute("caption_sentences_stanford", Sentences).get_text(phrase_delimiter = " | ")
		cap_words = item.get_attribute("caption_sentences_stanford", Sentences).get_text().split()
		doc = item.get_attribute("doc")[0:504]+" ..."
		imgpath = item.get_attribute_path("jpg")
		w0 = item.get_attribute("FMA_FL.len+0.words.beam_size_500.paramsearch_length_attenuation_12.0", list)
		w3 = item.get_attribute("FMA_FL.len+3.words.beam_size_500.paramsearch_length_attenuation_15.0", list)
		w6 = item.get_attribute("FMA_FL.len+6.words.beam_size_500.paramsearch_length_attenuation_6.0", list)
		p0 = item.get_attribute("FMA_FL.len+0.beam_size_500.paramsearch_length_attenuation_12.0", list)
		p3 = item.get_attribute("FMA_FL.len+3.beam_size_500.paramsearch_length_attenuation_15.0", list)
		p6 = item.get_attribute("FMA_FL.len+6.beam_size.paramsearch_length_attenuation_6.0", list)
		w0 = map(lambda a: map(lambda b: b[0], a), w0[1][1][1][0])
		w3 = map(lambda a: map(lambda b: b[0], a), w3[1][1][1][0])
		w6 = map(lambda a: map(lambda b: b[0], a), w6[1][1][1][0])
		p0 = map(lambda a: map(lambda b: b[0], a), p0[1][1][1][0])
		p3 = map(lambda a: map(lambda b: b[0], a), p3[1][1][1][0])
		p6 = map(lambda a: map(lambda b: b[0], a), p6[1][1][1][0])

		outimgpath = os.path.join(outfolder, "images/%s.jpg" % (name))

		shutil.copyfile(imgpath, outimgpath)
		name_spaces = name.replace("_", " ")
		out_f = open(os.path.join(outtexfolder, "%s.tex" %(name)), "wb")
		out_f.write("\section*{%s}\n" % (name_spaces))
		out_f.write("""\\begin{wrapfigure}{r}{0.5\\textwidth}\n
\\vspace{-1em}\n
  \includegraphics[scale=0.85]{%s}\n
  \caption*{%s}\n
\end{wrapfigure}\n""" % (outimgpath, c_orig.strip()))

		out_f.write(doc+"\n")
		out_f.write("""\\vspace{1em}\n
\\begin{center}\n
\\def\\arraystretch{1.25}\n
%\\begin{tabular}{|c|c|c|}\n
\\begin{tabular}{|m{0.05\\textwidth}|m{0.81\\textwidth}|m{0.04\\textwidth}|}\n
\hline
 & caption & TER \\\\
\hline
""")
		w0o = " ".join(map(lambda x: " ".join(x),w0)).replace("<S_START>", "\\textbf{<}S\\_START\\textbf{>}").replace("<S_END>", "\\textbf{<}S\\_END\\textbf{>}")
		w3o = " ".join(map(lambda x: " ".join(x),w3)).replace("<S_START>", "\\textbf{<}S\\_START\\textbf{>}").replace("<S_END>", "\\textbf{<}S\\_END\\textbf{>}")
		w6o = " ".join(map(lambda x: " ".join(x),w6)).replace("<S_START>", "\\textbf{<}S\\_START\\textbf{>}").replace("<S_END>", "\\textbf{<}S\\_END\\textbf{>}")
		TW0 = TER(" ".join(map(lambda x: " ".join(x),w0)).split(), cap_words)
		TW3 = TER(" ".join(map(lambda x: " ".join(x),w3)).split(), cap_words)
		TW6 = TER(" ".join(map(lambda x: " ".join(x),w6)).split(), cap_words)
		p0o = " | ".join(map(lambda x: " ".join(x),p0)).replace("<S_START>", "\\textbf{<}S\\_START\\textbf{>}").replace("<S_END>", "\\textbf{<}S\\_END\\textbf{>}")
		p3o = " | ".join(map(lambda x: " ".join(x),p3)).replace("<S_START>", "\\textbf{<}S\\_START\\textbf{>}").replace("<S_END>", "\\textbf{<}S\\_END\\textbf{>}")
		p6o = " | ".join(map(lambda x: " ".join(x),p6)).replace("<S_START>", "\\textbf{<}S\\_START\\textbf{>}").replace("<S_END>", "\\textbf{<}S\\_END\\textbf{>}")
		TP0 = TER(" ".join(map(lambda x: " ".join(x),p0)).split(), cap_words)
		TP3 = TER(" ".join(map(lambda x: " ".join(x),p3)).split(), cap_words)
		TP6 = TER(" ".join(map(lambda x: " ".join(x),p6)).split(), cap_words)
		out_f.write("ORIG & %s & 0\\\\ \n" % (cap.strip().replace("<S_START>", "\\textbf{<}S\\_START\\textbf{>}").replace("<S_END>", "\\textbf{<}S\\_END\\textbf{>}")))
		out_f.write("\\hline\n")
		out_f.write("W1 & %s & %.2f\\\\ \n" % (w0o.strip(), TW0))
		out_f.write("\\hline\n")
		out_f.write("W2 & %s & %.2f\\\\ \n" % (w3o.strip(), TW3))
		out_f.write("\\hline\n")
		out_f.write("W3 & %s & %.2f\\\\ \n" % (w6o.strip(), TW6))
		out_f.write("\\hline\n")
		out_f.write("P1 & %s & %.2f\\\\ \n" % (p0o.strip(), TP0))
		out_f.write("\\hline\n")
		out_f.write("P2 & %s & %.2f\\\\ \n" % (p3o.strip(), TP3))
		out_f.write("\\hline\n")
		out_f.write("P3 & %s & %.2f\\\\ \n" % (p6o.strip(), TP6))
		out_f.write("\\hline\n")
		out_f.write("\\end{tabular}\n")
		out_f.write("\\end{center}\n")
	inc_f.close()
