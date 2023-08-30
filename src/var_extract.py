
class IOConfig():
	#输入输出格式:
	# 0 json {orig:''}
	# 1 json {orig:orig}
	# 2 json [{name,message}]
	outputFormat = 0
	ouputFileName = ''
	inputFileName = ''
	prefix = ''

class ExtractVar():
	Postfix = '.txt'
	EncodeRead = 'utf-8'
	contentSeprate = None
	nameList = []
	regDic = {}
	cutoff = False
	cutoffCopy = False
	noInput = False
	indent = 2 #缩进
	#可选参数
	startline = 0 #起始行数
	extractName = '^.'
	structure = ''
	extraData = '' #引擎自定义的数据
	ignoreDecodeError = False #忽略编码错误
	postSkip = None #匹配后置skip，匹配成功则跳过
	checkJIS = None #检查JIS，可配置允许的单字符匹配
	endStr = None #匹配到则结束
	ctrlStr = None #控制段跳过
	version = '0' #版本
	decrypt = '' #加解密密钥
	#
	parseImp = None
	replaceOnceImp = None
	readFileDataImp = None
	replaceEndImp = None
	workpath = ''
	#导出配置
	io = IOConfig()
	ioExtra = IOConfig()
	curIO:IOConfig = None

	partMode = 0 # 0 单json; 1 多json
	outputDir = 'ctrl'
	inputDir = 'ctrl'

	#-------------------
	transDic = {}
	transDicIO = {} #读取写入时的原本字典，不参与write()，模式01则不需要
	allOrig = []

	#-------------------
	filename = ''
	content = None
	insertContent = {} #需要插入的内容
	isInput = False #是否写入译文
	inputCount = 0 #导出文件个数
	outputCount = 0 #导出文件个数
	listOrig = [] #原文表
	listCtrl = [] #控制表
	addSeprate = True
	cutoffDic = {}

	#-------------------
	#窗口
	window = None

	def clear(self):
		self.insertContent = {}
		self.inputCount = 0
		self.outputCount = 0
		#
		self.startline = 0
		self.extractName = '^.'
		self.structure = ''
		self.extraData = ''
		self.ignoreDecodeError = False
		self.postSkip = None
		self.checkJIS = None
		self.endStr = None
		self.ctrlStr = None
		self.version = '0'
		self.decrypt = ''

gExtractVar = ExtractVar()