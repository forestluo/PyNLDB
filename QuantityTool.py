# -*- coding: utf-8 -*-

import re

from Common import WordType

class QuantityTool :
    # 单位标识
    _unit_symbols = \
    [
        "%", "′", "″", "°", "A", "Bq", "C", "℃", "cal", "cm", "d",
        "db", "ev", "F", "℉", "g", "Gy", "H", "hz", "j", "K", "kg",
        "km", "kn", "kpa", "kw", "kwh", "kΩ", "l", "lm", "lx", "m",
        "mg", "min", "ml", "mm", "ms", "mΩ", "n", "nm", "ns", "pa",
        "ps", "rad", "s", "sr", "Sv", "T", "tex", "u", "V", "w", "wb",
        "um", "us", "Ω"
    ]
    # 单位名称
    _unit_names = \
    [
        "埃", "安", "安培", "盎司", "巴", "百克", "百米", "百帕", "百升",
        "磅", "贝", "贝尔", "标准大气压", "长吨", "尺", "寸", "打兰", "大气压",
        "担", "电子伏特", "斗", "度", "短吨", "吨", "吨标准煤", "吨当量煤",
        "尔格", "法拉", "费密", "分贝", "分克", "分米", "分升", "分钟",
        "弗隆", "伏", "伏安", "伏特", "格令", "公斤", "公里", "公亩", "公顷",
        "光年", "海里", "毫", "毫安", "毫巴", "毫伏", "毫克", "毫米", "毫米汞柱",
        "毫米水柱", "毫升", "合", "赫兹", "亨", "亨利", "弧度", "华氏度", "及耳",
        "加仑", "焦耳", "角分", "角秒", "节", "斤", "开尔文", "开氏度", "坎德拉",
        "克", "克拉", "夸脱", "兰氏度", "勒", "勒克斯", "厘", "厘克", "厘米",
        "厘升", "里", "立方", "立方分米", "立方厘米", "立方码", "立方米", "立方英尺",
        "立方英寸", "两", "量滴", "列氏度", "流", "流明", "马力", "码", "美担", "米",
        "米制马力", "密耳", "秒", "摩尔", "亩", "纳法", "纳米", "奈培", "年", "牛顿",
        "欧", "欧姆", "帕", "帕斯卡", "配克", "皮法", "皮米", "品脱", "平方尺", "平方寸",
        "平方分", "平方分米", "平方公里", "平方毫米", "平方厘", "平方厘米", "平方里",
        "平方码", "平方米", "平方千米", "平方英尺", "平方英寸", "平方英里", "平方丈",
        "蒲式耳", "千伏", "千卡", "千克", "千米", "千帕", "千升", "千瓦", "钱", "顷",
        "球面度", "勺", "摄氏度", "升", "十克", "十米", "十升", "石", "人",
        "市尺", "市斤", "市里", "市亩", "市升", "特", "特克斯", "特斯拉", "天文单位",
        "桶", "瓦", "万伏", "微法", "微克", "微米", "微升", "韦", "韦伯", "西", "西门子",
        "像素", "小时", "英磅", "英尺", "英寸", "英担", "英里", "英亩", "英钱", "英石",
        "英寻", "英制马力", "丈", "兆瓦", "转", "月", "时", "分", "秒", "毫秒", "微秒"
    ]
    # 数量词名称
    _quantifier_names = \
    [
        "把", "班", "般", "板", "版", "瓣", "帮", "包", "抱", "杯", "辈", "辈子", "本",
        "笔", "边", "彪", "柄", "拨", "钵", "簸箕", "部", "部分", "步", "餐", "册", "层",
        "茬", "场", "车", "车皮", "匙", "池", "出", "处", "船", "串", "床", "丛", "簇",
        "沓", "代", "袋", "担", "刀", "道", "等", "滴", "点", "碟", "叠", "顶", "锭", "栋",
        "兜", "蔸", "堵", "段", "堆", "对", "队", "墩", "囤", "朵", "垛", "驮", "发", "番",
        "方", "房", "份", "封", "幅", "副", "服", "竿", "杆", "缸", "格", "根",
        "钩", "股", "挂", "管", "罐", "贯", "桄", "锅", "行", "号", "盒", "痕", "泓", "壶",
        "户", "环", "伙", "辑", "集", "级", "剂", "季", "家", "夹", "架", "驾", "间", "肩",
        "件", "角", "窖", "截", "节", "介", "届", "进", "茎", "局", "具", "句", "卷", "开",
        "窠", "棵", "颗", "孔", "口", "块", "筐", "捆", "栏", "篮", "揽子", "粒", "例", "辆",
        "列", "领", "流", "绺", "溜", "笼", "垄", "篓", "炉", "路", "缕", "轮", "箩", "摞",
        "码", "脉", "毛", "枚", "门", "面", "名", "抹", "幕", "年", "排", "派", "盘", "泡",
        "盆", "棚", "捧", "批", "匹", "篇", "片", "瓢", "撇", "瓶", "期", "畦", "起", "腔",
        "墙", "锹", "丘", "曲", "阕", "群", "任", "色", "扇", "勺", "哨", "身", "声", "乘",
        "首", "手", "树", "束", "双", "丝", "艘", "所", "台", "抬", "滩", "摊", "坛", "潭",
        "塘", "堂", "樘", "套", "提", "屉", "挑", "条", "贴", "帖", "听", "挺", "通", "筒",
        "头", "团", "坨", "弯", "丸", "汪", "网", "尾", "味", "位", "瓮", "窝", "握", "席",
        "袭", "匣", "线", "箱", "项", "些", "宿", "眼", "页", "叶", "印张", "羽", "园", "员",
        "扎", "则", "盏", "章", "张", "着", "折", "针", "帧", "支", "枝", "纸", "盅", "站",
        "轴", "株", "注", "炷", "柱", "桩", "幢", "桌", "宗", "组", "嘴", "尊", "樽", "撮",
        "座", "平", "次", "重", "居", "个", "只", "岁", "种", "档", "类", "天", "日", "倍",
        "界", "周", "挡"
    ]
    # 货币符号
    _currency_symbols = \
    [
        "¥", "＄", "₠", "₡", "₢", "₣", "₤", "₥", "₦", "₧", "₨", "₩", "₪", "₫", "€", "₭",
        "₮", "₯", "₰", "₱", "₲", "₳", "₴", "₵", "₶", "₷", "₸", "₹", "₺", "₻", "₼", "₽", "₾", "₿"
    ]
    # 货币名称
    _currency_names = \
    [
        "阿富汗尼", "埃斯库多", "澳大利亚元", "澳元", "巴波亚", "埃镑", "镑", "比尔", "比塞塔", "比索",
        "玻利瓦", "达拉西", "丹麦克郎", "迪拉姆", "第纳尔", "盾", "多步拉", "法郎", "菲律宾比索",
        "分", "福林", "港元", "格查尔", "古德", "瓜拉尼", "韩国元", "韩元", "基纳", "基普", "加拿大元",
        "加元", "角", "科多巴", "科朗", "克郎", "克鲁塞罗", "克瓦查", "宽札", "拉菲亚", "兰特",
        "厘", "里拉", "里兰吉尼", "里亚尔", "利昂", "列弗", "列克", "列伊", "卢布", "伦皮拉", "洛蒂",
        "马克", "梅蒂卡尔", "美分", "美元", "奈拉", "努扎姆", "挪威克郎", "欧元", "潘加", "普拉", "人民币",
        "日元", "瑞典克郎", "瑞士法郎", "塞迪", "苏克雷", "索尔", "塔卡", "塔拉", "台币", "泰铢", "图格里克",
        "瓦图", "乌吉亚", "先令", "谢克尔", "新加坡元", "新台币", "新西兰元", "新元", "印度卢布", "英镑",
        "元", "越南盾", "扎伊尔", "铢", "兹罗提"
    ]

    # 拼合
    @staticmethod
    def __rule__(items) :
        # 规则
        rule = "("
        # 循环处理
        for item in items :
            # 增加字符
            rule += item + "|"
        # 删除最后一个字符
        rule = rule[:len(rule) - 1] + ")"
        # 返回结果
        return rule

    # 获得规则
    @staticmethod
    def __get_rule__(item) :
        # 检查类型
        if item == "$a" :
            # 返回结果
            # 标点符号
            return "(((?!(，|：|；|、|…|—|《|》|\\。|\\？|\\！|\\s)).)*)"
        # 检查类型
        if item == "$b" :
            # 返回结果
            # 标点符号（至少一个）
            return "(((?!(，|：|；|、|…|—|《|》|\\。|\\？|\\！|\\s)).)+)"
        # 检查类型
        if item == "$c" :
            # 返回结果
            # 中文数字
            return "[零|一|二|三|四|五|六|七|八|九|十]"
        # 检查类型
        if item == "$d" :
            # 返回结果
            # 整数数字
            return "(-?[1-9]\\d*|0)"
        # 检查类型
        if item == "$e" :
            # 返回结果
            # 英文字符（含大小写）
            return "[A-Za-z]"
        # 检查类型
        if item == "$f" :
            # 返回结果
            # 浮点数字
            return "(-?([1-9]\\d*|[1-9]\\d*\\.\\d+|0\\.\\d+))"
        # 检查类型
        if item == "$h" :
            # 返回结果
            # 单个中文汉字
            return "[\u4E00-\u9FA5]"
        # 检查类型
        if item == "$n" :
            # 返回结果
            # 整数
            return "(\\d+)"
        # 检查类型
        if item == "$s" :
            # 返回结果
            # 字符串
            return "[A-Za-z]+[A-Za-z'' ]*"
        # 检查类型
        if item == "$q" :
            # 排序
            QuantityTool._quantifier_names. \
                sort(key = lambda i : len(i), reverse = True)
            # 返回结果
            # 量词名称
            return QuantityTool.__rule__(QuantityTool._quantifier_names)
        # 检查类型
        if item == "$u" :
            # 排序
            QuantityTool._unit_names. \
                sort(key = lambda i : len(i), reverse = True)
            # 返回结果
            # 单位名称
            return QuantityTool.__rule__(QuantityTool._unit_names)
        # 检查类型
        if item == "$v" :
            # 排序
            QuantityTool._unit_symbols. \
                sort(key = lambda i : len(i), reverse = True)
            # 返回结果
            # 单位符号
            return QuantityTool.__rule__(QuantityTool._unit_symbols)
        # 检查类型
        if item == "$y" :
            # 排序
            QuantityTool._currency_names. \
                sort(key = lambda i : len(i), reverse = True)
            # 返回结果
            # 货币名称
            return QuantityTool.__rule__(QuantityTool._currency_names)
        # 检查类型
        if item == "$z" :
            # 返回结果
            # 中文字符串
            return "([\u4E00-\u9FA5]+)"
        # 返回结果
        return None

    @staticmethod
    def _get_rule_(rule) :
        # 检查参数
        assert isinstance(rule, str)
        # 替换参数
        rule = rule.replace("$a", QuantityTool.__get_rule__("$a"))
        rule = rule.replace("$b", QuantityTool.__get_rule__("$b"))
        rule = rule.replace("$c", QuantityTool.__get_rule__("$c"))
        rule = rule.replace("$d", QuantityTool.__get_rule__("$d"))
        rule = rule.replace("$e", QuantityTool.__get_rule__("$e"))
        rule = rule.replace("$f", QuantityTool.__get_rule__("$f"))
        rule = rule.replace("$h", QuantityTool.__get_rule__("$h"))
        rule = rule.replace("$n", QuantityTool.__get_rule__("$n"))
        rule = rule.replace("$s", QuantityTool.__get_rule__("$s"))
        rule = rule.replace("$q", QuantityTool.__get_rule__("$q"))
        rule = rule.replace("$u", QuantityTool.__get_rule__("$u"))
        rule = rule.replace("$v", QuantityTool.__get_rule__("$v"))
        rule = rule.replace("$y", QuantityTool.__get_rule__("$y"))
        rule = rule.replace("$z", QuantityTool.__get_rule__("$z"))
        # 返回结果
        return rule

class MatchedSegment :
    # 初始化
    # matched为正则表达式匹配结果
    def __init__(self, matched = None) :
        # 设置缺省值
        # 计数
        self.count = 0
        # 检查参数
        if matched is None:
            # 内容
            self.content = ""
            # 索引【开始，结束】
            # 长度 = 结束 - 开始
            self._index = [-1, -1]
        else :
            # 设置内容
            self.content = matched.group()
            # 设置长度
            self._index = [matched.start(), matched.end()]

    # 终止
    @property
    def end(self) :
        # 返回结果
        return self._index[1]

    @end.setter
    def end(self, value) :
        # 返回结果
        self._index[1] = value

    # 起始
    @property
    def start(self) :
        # 返回结果
        return self._index[0]

    @start.setter
    def start(self, value) :
        # 设置数值
        self._index[0] = value

    # 判断是否相等
    def __eq__(self, segment) :
        # 检查参数
        assert isinstance(segment, MatchedSegment)
        # 检查内容
        return self.content == segment.content

    # 是否为空
    @property
    def empty(self) :
        # 返回结果
        return len(self.content) == 0 or self.start >= self.end

class MatchedGroup :
    # 初始化
    def __init__(self) :
        # 初始化为私有对象
        # 否则会被认为是静态对象
        self._segments = []

    # 检查是否为空
    @property
    def empty(self) :
        # 返回结果
        return len(self._segments) == 0

    # 增加段落
    def add_segment(self, segment) :
        # 增加项目
        self._segments.append(segment)

    # 增加匹配项目
    def add_matched(self, matched) :
        # 增加项目
        self._segments.append(MatchedSegment(matched))

    # 找到可以匹配的字符
    # index为基于整个匹配字符串的索引
    def get_char(self, index) :
        # 查找匹配的段落
        segment = self._get_segment_(index)
        # 检查结果
        if segment is None : return None
        # 检查参数
        assert index < segment.end
        assert index >= segment.start
        # 返回结果
        return segment.content[index - segment.start]

    # 通过索引查找可以匹配的段落
    # index为基于整个匹配字符串的索引
    def _get_segment_(self, index):
        # 循环处理
        for segment in self._segments:
            # 检查索引位置
            if segment.start <= index < segment.end : return segment
        # 返回空
        return None

    def dump(self) :
        # 打印信息
        print("MatchedGroup.dump : show segments !")
        for i in range(0, len(self._segments)) :
            # 获得段落
            segment = self._segments[i]
            # 打印信息
            print("\tsegment[%d](%d,%d) = \"%s\"" % (i, segment.start, segment.end, segment.content))

class QuantityTemplate(QuantityTool) :
    # 匹配模板
    _patterns = []
    # 数量词模板
    _templates = \
    [
        "\\d+", # 编号

        "\\d+$v", # 单位符号
        "\\d+$u", # 单位名称
        "\\d+$q", # 量词
        "\\d+$y", # 货币名称

        ",\\d{3}",
        "\\d+[至|比]",
        "[￥|＄]\\d+",

        "$c+$u", # 单位名称
        "$c+$q", # 量词
        "$c+$y", # 货币名称

        "[\\.|+|\\-|*|/|<|=|#|＋|－|×|÷]+[A-Za-z\\d]+",
        "[A-Za-z\\d]+[\\.|~|'|\"|:|+|\\-|*|/|>|=|#|：|～|＋|－|×|÷]+",

        "[十|百|千|万|亿][多|余]?[十|百|千|万|亿]?$c{1,2}",
        "$c{1,2}[十|百|千|万|亿][多|余]?[个|十|百|千|万|亿]?($u|$q|$y)?",

        "\\d+[十|百|千|万|亿][多|余]?[个|十|百|千|万|亿]?($u|$q|$y)?",
        # 序数
        "每$u",
        "第$c", # 序数
        "第\\d+", # 序数
        # 百分数
        "$c+分之",
        "[百]?分之$c+",
        "[\\d+|$c+]个百分点", # 百分点
        # 时间
        "[上|中|下]午",
        "(\\d+|$c+)个(月|小时)",
        "(\\d+|$c+)(周|年|季度|刻钟)"
    ]

    @staticmethod
    def _extract_(content) :
        # 匹配的段落集合
        group = MatchedGroup()
        # 循环处理
        for pattern in QuantityTemplate._patterns :
            # 匹配
            matched = pattern.finditer(content)
            # 检查结果
            for match in matched : group.add_matched(match)
        # 返回结果
        return None if group.empty else group

    @staticmethod
    def extract(content) :
        # 检查参数
        assert isinstance(content, str)

        # 获得所有匹配的段落集合
        group = QuantityTemplate._extract_(content)
        # 检查结果
        if group is None : return None

        # 索引
        index = 0
        # 新集合
        new_group = MatchedGroup()
        # 循环处理
        while index < len(content) :
            # 获得当前字符
            value = group.get_char(index)
            # 检查结果
            if value is None : index += 1; continue

            # 生成新的段落
            segment = MatchedSegment()
            # 设置索引
            segment.start = index
            # 设置内容
            segment.content = value
            # 设置类型
            segment.remark = WordType.quantity

            # 循环处理
            for j in range(index + 1, len(content)) :
                # 设置结束标记
                segment.end = j
                # 获得当前字符
                value = group.get_char(j)
                # 检查结果
                if value is None: break
                # 增加内容
                segment.content += value

            # 设置索引
            index = segment.end + 1
            # 检查结果
            assert not segment.empty
            # 增加段落
            new_group.add_segment(segment)
        # 检查结果
        return None if new_group.empty else new_group

    @staticmethod
    def set_default() :
        # 获得预编译模板
        QuantityTemplate._patterns = \
            [re.compile(QuantityTool._get_rule_(template)) for template in QuantityTemplate._templates]

# 设置缺省提取模板
QuantityTemplate.set_default()
# 打印信息
print("QuantityTool.QuantityTemplate : default templates were set !")

