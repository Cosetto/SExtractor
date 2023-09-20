# SExtractor
 仅用于提取和导入GalGame脚本文本（大部分都需要明文）
 
## Python依赖模块：
国内推荐先配置镜像再下载：`pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
* pyqt5
* colorama
* pandas

## 支持的引擎：
同引擎不同游戏的格式也可能不同，请参看程序内示例使用。
* TXT纯文本 (正则匹配。可选utf-8，utf-8-sig，utf-16(LE BOM))
* BIN二进制文本 (正则匹配。默认读shift-jis写GBK)
* JSON文本 (正则匹配，只搜索value)
* AST (移除，转为正则预设)
* Artemis
* CSV
* Cyberworks / CSystem (仅用于文本为UTF-16的新版)
* EAGLS
* FVP
* Kaguya
* Krkr (可正则)
* MED (DxLib)
* MoonHir
* NekoSDK
* RPGMaker MV
* RenPy
* SiglusEngine (弃用)
* SystemC
* WillPlus
* Yu-ris

## 其他功能
* 可以导出VNT的JIS隧道文件sjis_ext.bin，需要配合VNTProxy一起使用。
* 文件夹下自定义的config*.ini都会被读取，*中不能以数字开头。(例：configTest.ini)
* reg.ini中可自定义正则匹配规则

## 当前正则预设
* AST
* Artemis
* EntisGLS
* Krkr
* Nexas
* RealLive (选项分开提取)
* SFA(AOS)
* SystemC
* Valkyria_ODN
* Yuris_txt (非ybn)
* BIN暴力匹配
* 替换符号
* JSON_Key(TXT转JSON)
* 猜测名字
* 两行TXT
* 导出所有(多用于格式转换)
* 自定义规则(自动保存)
* None还原为引擎默认

## 支持的导出格式：
* json字典 { 文本 : "" }
* json字典 { 文本 : 文本 }
* json列表 [ { name : 名字, message : 带换行对话 } ]
* json字典 { 带换行文本 : "" }
* json字典 { 带换行文本 : 带换行文本 }
* txt文档  { 文本 }
* txt文档  [ 带换行文本 ]
* json列表 [ 带换行文本 ]

## 相关参考项目
1. [ssynn](https://github.com/ssynn/game_translation)
2. [SiglusTools](https://github.com/yanhua0518/GALgameScriptTools)
3. [CSystemTools](https://github.com/arcusmaximus/CSystemTools)
4. [VNTranslationTools](https://github.com/arcusmaximus/VNTranslationTools)
