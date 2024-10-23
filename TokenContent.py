# -*- coding: utf-8 -*-

import traceback

from RawContent import *

class TokenItem :
    # 初始化对象
    def __init__(self, token):
        # 检查参数
        assert token is not None
        assert (isinstance(token, str) and len(token) == 1)
        # 频次计数器
        self.count = 1.0
        # 设置字符
        self.token = token
        # 设置Unicode值
        self.unicode = ord(token)

    def dump(self):
        # 打印信息
        print("TokenItem.dump : show properties !")
        print("\ttoken = \'%c\'" % self.token)
        print("\tunicode = 0x%4X" % self.unicode)
        print("\tcount = %d" % self.count)
        print("\tremark = \"%s\"" % TokenItem.remark(self.token))

    @staticmethod
    def remark(token):
        # 检查参数
        if token is not None:
            assert (isinstance(token, str) and len(token) == 1)
        # 获得Unicode值
        unicode = ord(token)
        # 检查结果
        if unicode <= 0x007F : return "C0控制符及基本拉丁文"
        if unicode <= 0x00FF : return "C1控制符及拉丁文补充-1"
        if unicode <= 0x017F : return "拉丁文扩展-A"
        if unicode <= 0x024F : return "拉丁文扩展-B"
        if unicode <= 0x02AF : return "国际音标扩展"
        if unicode <= 0x02FF : return "空白修饰字母"
        if unicode <= 0x036F : return "结合用读音符号"
        if unicode <= 0x03FF : return "希腊文及科普特文"
        if unicode <= 0x04FF : return "西里尔字母"
        if unicode <= 0x052F : return "西里尔字母补充"
        if unicode <= 0x058F : return "亚美尼亚语"
        if unicode <= 0x05FF : return "希伯来文"
        if unicode <= 0x06FF : return "阿拉伯文"
        if unicode <= 0x074F : return "叙利亚文"
        if unicode <= 0x077F : return "阿拉伯文补充"
        if unicode <= 0x07BF : return "马尔代夫语"
        if unicode <= 0x07FF : return "西非书面語言"
        if unicode <= 0x085F : return "阿维斯塔语及巴列维语"
        if unicode <= 0x087F : return "Mandaic"
        if unicode <= 0x08AF : return "撒马利亚语"
        if unicode <= 0x097F : return "天城文书"
        if unicode <= 0x09FF : return "孟加拉语"
        if unicode <= 0x0A7F : return "锡克教文"
        if unicode <= 0x0AFF : return "古吉拉特文"
        if unicode <= 0x0B7F : return "奥里亚文"
        if unicode <= 0x0BFF : return "泰米尔文"
        if unicode <= 0x0C7F : return "泰卢固文"
        if unicode <= 0x0CFF : return "卡纳达文"
        if unicode <= 0x0D7F : return "德拉维族语"
        if unicode <= 0x0DFF : return "僧伽罗语"
        if unicode <= 0x0E7F : return "泰文"
        if unicode <= 0x0EFF : return "老挝文"
        if unicode <= 0x0FFF : return "藏文"
        if unicode <= 0x109F : return "缅甸语"
        if unicode <= 0x10FF : return "格鲁吉亚语"
        if unicode <= 0x11FF : return "朝鲜文"
        if unicode <= 0x137F : return "埃塞俄比亚语"
        if unicode <= 0x139F : return "埃塞俄比亚语补充"
        if unicode <= 0x13FF : return "切罗基语"
        if unicode <= 0x167F : return "统一加拿大土著语音节"
        if unicode <= 0x169F : return "欧甘字母"
        if unicode <= 0x16FF : return "如尼文"
        if unicode <= 0x171F : return "塔加拉语"
        if unicode <= 0x173F : return "Hanunóo"
        if unicode <= 0x175F : return "Buhid"
        if unicode <= 0x177F : return "Tagbanwa"
        if unicode <= 0x17FF : return "高棉语"
        if unicode <= 0x18AF : return "蒙古文"
        if unicode <= 0x18FF : return "Cham"
        if unicode <= 0x194F : return "Limbu"
        if unicode <= 0x197F : return "德宏泰语"
        if unicode <= 0x19DF : return "新傣仂语"
        if unicode <= 0x19FF : return "高棉语记号"
        if unicode <= 0x1A1F : return "Buginese"
        if unicode <= 0x1A5F : return "Batak"
        if unicode <= 0x1AEF : return "Lanna"
        if unicode <= 0x1B7F : return "巴厘语"
        if unicode <= 0x1BB0 : return "巽他语"
        if unicode <= 0x1BFF : return "Pahawh Hmong"
        if unicode <= 0x1C4F : return "雷布查语"
        if unicode <= 0x1C7F : return "Ol Chiki"
        if unicode <= 0x1CDF : return "曼尼普尔语"
        if unicode <= 0x1D7F : return "语音学扩展"
        if unicode <= 0x1DBF : return "语音学扩展补充"
        if unicode <= 0x1DFF : return "结合用读音符号补充"
        if unicode <= 0x1EFF : return "拉丁文扩充附加"
        if unicode <= 0x1FFF : return "希腊语扩充"
        if unicode <= 0x206F : return "常用标点"
        if unicode <= 0x209F : return "上标及下标"
        # 货币符号
        if unicode <= 0x20CF : return "货币符号"
        if unicode <= 0x20FF : return "组合用记号"
        if unicode <= 0x214F : return "字母式符号"
        if unicode <= 0x218F : return "数字形式"
        if unicode <= 0x21FF : return "箭头"
        if unicode <= 0x22FF : return "数学运算符"
        if unicode <= 0x23FF : return "杂项工业符号"
        if unicode <= 0x243F : return "控制图片"
        if unicode <= 0x245F : return "光学识别符"
        if unicode <= 0x24FF : return "封闭式字母数字"
        if unicode <= 0x257F : return "制表符"
        if unicode <= 0x259F : return "方块元素"
        if unicode <= 0x25FF : return "几何图形"
        if unicode <= 0x26FF : return "杂项符号"
        if unicode <= 0x27BF : return "印刷符号"
        if unicode <= 0x27EF : return "杂项数学符号-A"
        if unicode <= 0x27FF : return "追加箭头-A"
        if unicode <= 0x28FF : return "盲文点字模型"
        if unicode <= 0x297F : return "追加箭头-B"
        if unicode <= 0x29FF : return "杂项数学符号-B"
        if unicode <= 0x2AFF : return "追加数学运算符"
        if unicode <= 0x2BFF : return "杂项符号和箭头"
        if unicode <= 0x2C5F : return "格拉哥里字母"
        if unicode <= 0x2C7F : return "拉丁文扩展-C"
        if unicode <= 0x2CFF : return "古埃及语"
        if unicode <= 0x2D2F : return "格鲁吉亚语补充"
        if unicode <= 0x2D7F : return "提非纳文"
        if unicode <= 0x2DDF : return "埃塞俄比亚语扩展"
        if unicode <= 0x2E7F : return "追加标点"
        if unicode <= 0x2EFF : return "CJK 部首补充"
        if unicode <= 0x2FDF : return "康熙字典部首"
        if unicode <= 0x2FFF : return "表意文字描述符"
        if unicode <= 0x303F : return "CJK 符号和标点"
        if unicode <= 0x309F : return "日文平假名"
        if unicode <= 0x30FF : return "日文片假名"
        if unicode <= 0x312F : return "注音字母"
        if unicode <= 0x318F : return "朝鲜文兼容字母"
        if unicode <= 0x319F : return "象形字注释标志"
        if unicode <= 0x31BF : return "注音字母扩展"
        if unicode <= 0x31EF : return "CJK 笔画"
        if unicode <= 0x31FF : return "日文片假名语音扩展"
        if unicode <= 0x32FF : return "封闭式 CJK 文字和月份"
        if unicode <= 0x33FF : return "CJK 兼容"
        if unicode <= 0x4DBF : return "CJK 统一表意符号扩展 A"
        if unicode <= 0x4DFF : return "易经六十四卦符号"
        # 基础汉字
        if unicode <= 0x9FBF : return "CJK 统一表意符号"
        if unicode <= 0xA48F : return "彝文音节"
        if unicode <= 0xA4CF : return "彝文字根"
        if unicode <= 0xA61F : return "Vai"
        if unicode <= 0xA6FF : return "统一加拿大土著语音节补充"
        if unicode <= 0xA71F : return "声调修饰字母"
        if unicode <= 0xA7FF : return "拉丁文扩展-D"
        if unicode <= 0xA82F : return "Syloti Nagri"
        if unicode <= 0xA87F : return "八思巴字"
        if unicode <= 0xA8DF : return "Saurashtra"
        if unicode <= 0xA97F : return "爪哇语"
        if unicode <= 0xA9DF : return "Chakma"
        if unicode <= 0xAA3F : return "Varang Kshiti"
        if unicode <= 0xAA6F : return "Sorang Sompeng"
        if unicode <= 0xAADF : return "Newari"
        if unicode <= 0xAB5F : return "越南傣语"
        if unicode <= 0xABA0 : return "Kayah Li"
        if unicode <= 0xD7AF : return "朝鲜文音节"
        # 不可见字符
        if unicode <= 0xDBFF : return "High-half zone of UTF-16"
        # 不可见字符
        if unicode <= 0xDFFF : return "Low-half zone of UTF-16"
        if unicode <= 0xF8FF : return "自行使用区域"
        if unicode <= 0xFAFF : return "CJK 兼容象形文字"
        if unicode <= 0xFB4F : return "字母表達形式"
        if unicode <= 0xFDFF : return "阿拉伯表達形式A"
        if unicode <= 0xFE0F : return "变量选择符"
        if unicode <= 0xFE1F : return "竖排形式"
        if unicode <= 0xFE2F : return "组合用半符号"
        if unicode <= 0xFE4F : return "CJK 兼容形式"
        if unicode <= 0xFE6F : return "小型变体形式"
        if unicode <= 0xFEFF : return "阿拉伯表達形式B"
        if unicode <= 0xFFEF : return "半型及全型形式"
        # 不可见字符
        if unicode <= 0xFFFF : return "特殊"
        # 返回结果
        return None

class TokenContent :
    # 初始化对象
    def __init__(self) :
        # Hash表
        self._tokens = {}

    def __contains__(self, token) :
        # 检查参数
        assert token is not None and len(token) == 1
        # 返回结果
        return token in self._tokens.keys()

    def __getitem__(self, token) :
        # 检查参数
        assert token is not None and len(token) == 1
        # 返回结果
        return self._tokens[token]

    def __setitem__(self, token, tokenItem) :
        # 检查参数
        assert token is not None and len(token) == 1
        # 设置数值
        self._tokens[token] = tokenItem

    def add(self, rawItem) :
        # 检查参数
        assert rawItem is not None
        assert isinstance(rawItem, RawItem)

        # 扫描结果
        for token in rawItem.content :
            # 检查字典
            if token in self._tokens :
                # 获得对象
                tokenItem = self._tokens[token]
                # 计数器加一
                tokenItem.count = tokenItem.count + 1
            else :
                # 增加字典内容
                self._tokens[token] = TokenItem(token)

    def save(self, fileName) :
        # 检查文件名
        if fileName is None:
            fileName = "tokens.json"
        # 打开文件
        jsonFile = open(fileName, "w", encoding = "utf-8")
        # 打印信息
        print("TokenContent.save : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = len(self._tokens)
        # 打印数据总数
        print("TokenContent.save : try to save %d row(s) !" % total)
        # 将总数写入文件
        jsonFile.write(str(total))
        jsonFile.write("\n")

        # 百分之一
        percent = 0
        onePercent = total / 100.0
        # 检查数据结果
        for item in self._tokens.values() :
            # 计数器加1
            count = count + 1
            # 写入文件
            jsonFile.write(json.dumps({"count" : item.count , "token" : item.token}, ensure_ascii = False))
            jsonFile.write("\n")
            # 检查结果
            if count >= (percent + 1) * onePercent:
                # 增加百分之一
                percent = percent + 1
                # 打印进度条
                print("\r", end="")
                print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                sys.stdout.flush()
        # 打印数据总数
        print("")
        print("TokenContent.save : %d row(s) saved !" % total)
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("TokenContent.save : file(\"%s\") closed !" % fileName)

    # 加载数据
    def load(self, fileName):
        # 检查文件名
        if fileName is None:
            fileName = "tokens.json"
        # 检查文件是否存在
        if not os.path.isfile(fileName):
            # 打印信息
            print("TokenContent.load : invalid file(\"%s\") !" % fileName)
            return -1
        # 打开文件
        jsonFile = open(fileName, "r", encoding = "utf-8")
        # 打印信息
        print("TokenContent.load : file(\"%s\") opened !" % fileName)
        # 检查文件
        assert jsonFile is not None

        # 计数器
        count = 0
        # 获得总数
        total = 0
        # 百分之一
        percent = 0
        onePercent = total / 100.0

        try:
            # 按行读取
            line = jsonFile.readline()
            # 循环处理
            while line :
                # 剪裁字符串
                line = line.strip()
                # 检查结果
                if len(line) <= 0:
                    # 读取下一行
                    line = jsonFile.readline()
                    continue

                # 计数器加1
                count = count + 1
                # 检查计数器
                if count == 1:
                    # 获得数据总数
                    total = int(line)
                    # 检查结果
                    if total <= 0 :
                        # 打印信息
                        print("TokenContent.load : invalid total(\"%s\") !" % line)
                        break
                    # 设置百分之一
                    onePercent = total / 100.0
                    # 打印数据总数
                    print("TokenContent.load : try to load %d row(s) !" % total)
                else:
                    # 按照json格式解析
                    jsonItem = json.loads(line)
                    # 生成原始数据对象
                    tokenItem = \
                        TokenItem(jsonItem["token"])
                    # 设置计数
                    tokenItem.count = jsonItem["count"]

                    # 检查结果
                    if (count - 1) >= (percent + 1) * onePercent:
                        # 增加百分之一
                        percent = percent + 1
                        # 打印进度条
                        print("\r", end="")
                        print("Progress({}%) :".format(percent), "▓" * (percent * 3 // 5), end="")
                        sys.stdout.flush()
                    # 加入字典
                    self._tokens[tokenItem.token] = tokenItem
                # 读取下一行
                line = jsonFile.readline()
            # 打印信息
            print("")
            print("TokenContent.load : %d line(s) processed !" % count)
        except Exception as e:
            traceback.print_exc()
            print("TokenContent.load : ", str(e))
            print("TokenContent.load : unexpected exit !")
        # 关闭文件
        jsonFile.close()
        # 打印信息
        print("TokenContent.load : file(\"%s\") closed !" % fileName)
        print("TokenContent.load : %d item(s) loaded !" % len(self._tokens))
        return total

def main():

    # 建立原始数据
    rawContent = RawContent()
    # 加载数据
    rawContent.load("normalized.json")
    # 建立字符表
    tokenContent = TokenContent()
    # 加载数据
    rawContent.traverse(tokenContent.add)
    # 保存文件
    tokenContent.save("tokens.json")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("TokenContent.main :__main__ : ", str(e))
        print("TokenContent.main :__main__ : unexpected exit !")