import re
import sys
import os
import struct
from common import *
import extract_TXT

# ---------------- Group: JSON -------------------
def parseImp(content, listCtrl, dealOnce):
	var = extract_TXT.ParseVar()
	var.listIndex = 0
	var.listCtrl = listCtrl
	var.dealOnce = dealOnce
	#print(len(content))
	regDic = GetG('Var').regDic
	var.regList = []
	for key, value in regDic.items():
		if re.search('skip', key):
			var.regList.append([value, 'skip'])
		elif re.search('search', key):
			var.regList.append([value, 'search'])
	for contentIndex in range(len(content)):
		#if contentIndex < 1: continue 
		lineData = content[contentIndex][:-1] #不检查末尾换行
		# 每行
		#print('>>> Line ' + str(contentIndex), ': ', lineData)
		if lineData == '': continue #空白行
		if re.match(r'\s*[\[\]\{\}]', lineData): continue #括号
		# 确认需要匹配的数据段
		ret = re.match(r'\s*"(.+?)":\s*"(.*?)"', lineData)
		if ret:
			value = ret.group(2)
			var.searchStart = ret.start(2)
			var.searchEnd = ret.end(2)
			# value为空则复制key到value
			if value == '':
				key = ret.group(1)
				strNew = content[contentIndex][:var.searchStart] + key + content[contentIndex][var.searchEnd:]
				content[contentIndex] = strNew
				lineData = content[contentIndex][:-1]
				var.searchEnd += len(key)
		else:
			print('\033[33m查找键值对失败\033[0m', lineData)
			continue
		# 跳过
		var.contentIndex = contentIndex
		var.lineData = lineData
		extract_TXT.searchLine(var)

# -----------------------------------
def replaceOnceImp(content, lCtrl, lTrans):
	extract_TXT.replaceOnceImp(content, lCtrl, lTrans)