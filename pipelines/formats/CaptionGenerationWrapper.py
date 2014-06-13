

class CaptionGenerationWrapper(object):
	def __init__(self, vocfile, csel_file, pA_file, lenmodel_file, lenmodel_type, beam_size = 25, lmfile = None, M = None, lowercase_csel = False):
		self.vocfile = vocfile
		self.csel_file = csel_file
		self.pA_file = pA_file
		self.lenmodel_file = lenmodel_file
		self.lenmodel_type = lenmodel_type
		self.lmfile = lmfile
		self.M = int(M)
		self.beam_size = beam_size
		self.lowercase_csel = bool(lowercase_csel)

		self.voc = None
		self.lm = None
		self.lenmodel = None
		self.pA_model = None
		self.csel_model = None
	
	def encode(self):
		outlines = []
		outlines.append("lmfile\t"+self.lmfile)
		outlines.append("M\t"+str(self.M_lm))
		outlines.append("vocfile\t"+self.vocfile)
		outlines.append("csel_file\t"+self.csel_file)
		outlines.append("lowercase_csel\t"+str(self.lowercase_csel))
		outlines.append("pA_file\t"+self.pA_file)
		outlines.append("lenmodel_file\t"+self.lenmodel_file)
		outlines.append("lenmodel_type\t"+self.lenmodel_type)
		outlines.append("beam_size\t"+str(self.beam_size))
		return "\n".join(outlines)

	@staticmethod
	def decode(string):
		return CaptionGenerationWrapper(dict(map(lambda x:x.split("\t"), string.split("\n"))))
	
	def get_config(self):
		params = {}
		params["lmfile"] = self.lmfile
		params["M"] = self.M
		params["pA_file"] = self.pA_file
		params["lenmodel_file"] = self.lenmodel_file
		params["lenmodel_type"] = self.lenmodel_type
		params["csel_file"] = self.csel_file
		params["lowercase_csel"] = self.lowercase_csel
		params["vocfile"] = self.vocfile
		params["beam_size"] = self.beam_size
		return params

	def get_parameters(self):
		pass	
	
	def set_parameters(self, params):
		#Extract parameters for static components -- all that is left will be LM parameters
		pA_eps = params.pop("pA_epsilon")
		#TODO: fix this -- it's all wrong!
		lenmodel_mean = params.pop("lenmodel_mean")	
		lenmodel_standard_deviation = params.pop("lenmodel_")
		csel_file = params.pop("csel_file")
		lowercase_csel = params.pop("lowercase_csel")
		vocfile = params.pop("vocfile")
		beam_size = params.pop("beam_size")
		if not self.lm is None:
			self.lm.set_updates(params)
			self.lm.ReInit()

	def generate(self):
		pass		
	
