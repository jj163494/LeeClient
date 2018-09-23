# -*- coding: utf-8 -*-

import os
import re
import json
from LeePyLibs import LeeCommon

class LeeBaseTranslator:
	def __init__(self):
		self.leeCommon = LeeCommon()
		self.leeFileIO = None
		self.translateDefaultDBPath = None
		self.translateMap = {}
		self.reSrcPathPattern = None
		self.reDstPathPattern = None
	
	def clear(self):
		self.translateMap.clear()

	def load(self, translateDBPath = None):
		self.clear()
		if translateDBPath is None: translateDBPath = self.translateDefaultDBPath
		translatePath = '%s/%s' % (self.leeCommon.getScriptDirectory(), translateDBPath)
		if not self.leeCommon.isFileExists(translatePath): return False
		try:
			self.translateMap = json.load(open(translatePath, 'r', encoding='utf-8'))
			return True
		except FileNotFoundError as _err:
			raise
	
	def save(self, translateDBPath = None):
		if saveFilename is None: saveFilename = self.translateDefaultDBPath
		scriptDir = self.leeCommon.getScriptDirectory()
		try:
			savePath = os.path.abspath('%s/%s' % (scriptDir, saveFilename))
			json.dump(self.translateMap, open(savePath, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
			return True
		except FileNotFoundError as _err:
			raise
	
	def doTranslate(self):
		leeClientDir = self.leeCommon.getLeeClientDirectory()
		scriptDir = self.leeCommon.getScriptDirectory()
		patchesDir = os.path.normpath('%s/Patches/' % scriptDir)

		if self.reSrcPathPattern is None: return False
		if self.reDstPathPattern is None: return False

		sourceFilePathList = []
		for dirpath, _dirnames, filenames in os.walk(patchesDir):
			for filename in filenames:
				fullpath = os.path.normpath('%s/%s' % (dirpath, filename))
				if not re.match(self.reSrcPathPattern, fullpath, re.I): continue
				sourceFilePathList.append(fullpath)

		self.load()
		
		for sourceFilePath in sourceFilePathList:
			print('正在汉化, 请稍候: %s' % os.path.relpath(sourceFilePath, leeClientDir))
			match = re.search(self.reDstPathPattern, sourceFilePath, re.MULTILINE | re.IGNORECASE | re.DOTALL)
			if match is None:
				self.leeCommon.exitWithMessage('无法确定翻译后的文件的存放位置, 程序终止')
			destinationPath = '%s/Translated/%s' % (match.group(1), match.group(2))
			self.trans(sourceFilePath, destinationPath)
			print('汉化完毕, 保存到: %s\r\n' % os.path.relpath(destinationPath, leeClientDir))
		
		return True

	def trans(self, srcFilepath, dstFilepath):
		pass