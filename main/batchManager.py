import os
import re
from PyQt5.QtCore import QCoreApplication
from main.thread import extractThread

class BatchManager():
	mainWindow = None
	oldDir = None
	cmdList = []
	index = 0
	running = False

	def __init__(self, mainWindow):
		self.mainWindow = mainWindow

	def runCommand(self, cmd=None):
		#运行子线程
		self.thread = extractThread(cmd)
		self.thread.window = self.mainWindow
		self.thread.finished.connect(self.handleThreadFinished)
		self.thread.start()

	def handleThreadFinished(self, ret):
		if ret == 1:
			self.mainWindow.statusBar.showMessage(QCoreApplication.translate('MainWindow','提取或导入时发生错误！！！    具体错误详见控制台打印！！！'), 'red')
		self.next()

	# ------------------------- 命令 -------------------------
	def getCmdList(self, text='', join=True):
		#保存设置
		edit = self.mainWindow.batchCmdListEdit.toPlainText()
		self.mainWindow.mainConfig.setValue('batchCmdListText', edit)
		checked = self.mainWindow.batchAutoStartCheck.isChecked()
		self.mainWindow.mainConfig.setValue('batchAutoStart', checked)
		checked = self.mainWindow.batchCmdCurCheck.isChecked()
		self.mainWindow.mainConfig.setValue('batchCmdCur', checked)
		self.runInCurPath = checked
		#拼接
		if text == '':
			join = True
		if join == True:
			text += '\n' + edit
		cmdList = []
		strList = re.split(r'[\r\n]+', text)
		for i, str in enumerate(strList):
			str = str.strip()
			if re.search(r'^\s*($|#|//|:: |;)', str):
				continue
			if re.search(r'^extract ', str):
				dirpath = str[8:]
				cmd = {
					"type": "extract",
					"data": dirpath
				}
			elif re.search(r'^set ', str):
				str = str[4:].strip()
				cmd = {
					"type": "set",
					"data": str
				}
			else:
				cmd = {
					"type": "command",
					"data": str
				}
			cmdList.append(cmd)
		return cmdList
	
	def start(self, status=False, cmd='', join=False):
		if self.running:
			self.resultAppend("正在运行中...")
			return
		self.mainWindow.batchResultBrowser.clear()
		self.running = True
		self.oldDir = self.mainWindow.mainDirPath
		#设置环境变量
		os.environ["extract_dir"] = self.mainWindow.mainDirPath
		self.index = 0
		self.cmdList = self.getCmdList(cmd, join)
		if len(self.cmdList) == 0:
			self.resultAppend("default env: extract_dir")
			self.resultAppend("Support commands:")
			self.resultAppend("extract dirpath")
			self.resultAppend("simple-system-command")
		self.next()

	def next(self):
		if len(self.cmdList) <= self.index:
			self.resultAppend(">> Done.\n")
			self.mainWindow.chooseMainDir(dir=self.oldDir)
			self.oldDir = None
			self.running = False
			return
		cmd = self.cmdList[self.index]
		self.index += 1
		data = cmd["data"]
		print(f"--------------------------- {self.index}/{len(self.cmdList)} ---------------------------")
		if cmd["type"] == "extract":
			# 提取
			data = self.getStrWithEnv(data)
			if not os.path.isdir(data):
				self.resultAppend(f'目录不存在：{data}')
			else:
				self.resultAppend(f"提取目录：{data}")
				self.mainWindow.chooseMainDir(dir=data) #切换到指定目录
				os.environ["extract_dir"] = self.mainWindow.mainDirPath
				self.mainWindow.prepareArgs()
				self.runCommand()
				return
		elif cmd["type"] == "set":
			# 设置环境变量
			m = re.search(r'=', data)
			if m:
				key = data[:m.start()]
				value = data[m.end():]
				value = self.getStrWithEnv(value)
				if value:
					self.resultAppend(f"环境变量：{key}={value}")
					os.environ[key] = value
				else:
					self.resultAppend(f"变量错误：{data}")
			else:
				self.resultAppend(f"命令错误：{data}")
		else:
			# 系统命令
			if self.runInCurPath:
				data = f'cd "{self.mainWindow.mainDirPath}" && {data}'
			self.resultAppend(f"系统命令：{data}")
			self.runCommand(data)
			return
		self.next()

	# ------------------------- 结果 -------------------------
	def resultAppend(self, line):
		self.mainWindow.batchResultBrowser.append(line)
		print(line)

	def getStrWithEnv(self, string):
		matches = re.findall(r'%[^%]+?%', string)
		for key in matches:
			name = key[1:-1]
			value = os.environ.get(name)
			if not value:
				self.resultAppend(f"未找到环境变量：{key}")
				return None
			string = string.replace(key, value)
		return string