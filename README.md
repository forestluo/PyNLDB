# PyNLDB

 基于Python3（PyCharm 2024）和NLDB的数据处理程序。主要是实现断句，分词和词性检测等功能。

 原始数据库的内容过大（超过40G），无法在Github上免费分享。因此没有选择上传（如有需要，请捐助之后联系）。

 数据文件均以json格式保存在本地。考虑数据量比较大（原始数据超过5G），未来将会增加爬虫机制，直接从互联网获得原始数据进行分析。

 NLDB3.py：用于连接数据库。main程序用于测试与NLDB3的连接情况。

 NLDB3Raw.py：（1）main程序用于将NLDB3中的原始数据（RawContent）导出成raw.json文件；（2）transverse用于嵌入式遍历处理；（3）random用于随机在数据库中选择一条数据（用于测试其他例程）。

 RawContent.py：用于保存、加载和遍历原始数据。（1）main程序用于将原始数据（raw.json）加载后，进行正则（“清洗”）化处理，然后另存为数据文件normalized.json；（2）trasverse用于嵌入式遍历处理。

 SentenceTool.py：用于分拆（“断句”）的工具。（1）main程序用于将数据库中的一条随机内容，进行分拆处理；（2）split函数会将内容按照标点符号进行拆解，并做好标记；（3）merge函数会对拆解后的标记内容进行逐级合并。

 SentenceTemplate.py：句子模板。按照模板匹配，提取出完整的句子。（1）main程序将会生成缺省的模板内容，并保存至templates.json文件；（2）extract函数用于从内容中，按照标点符号，提取出完整的句子。断句的基本过程：按照标点符号彻底拆解->做好标记，并作适当合并->逐级合并->按照模板提取。

 需要注意几点：（1）缺省模板的排序是固定的，不能随意调整。基本是按照最大匹配法的原则排列。如果自己想增加模板，也必须遵守这个原则。（2）对于没有完整标点符号指示的内容，程序会认为不是一个完整的句子。这种标点不全的内容，将会被直接抛弃。

 SentenceContent.py：用于保存、加载和遍历句子数据。main程序将利用templates.json指定的模板，从normalized.json中提取句子数据。

 TokenContent.py：用于保存、加载和遍历Token数据。Token是以单个Unicode字符为单位进行处理。除了Token，还有统计计数。main程序将从normalized.json中统计Token的次数。

# 参考链接

www.algmain.com

我的NLP（自然语言处理）历程（8）——频次统计：https://zhuanlan.zhihu.com/p/539109593

我的NLP（自然语言处理）历程（9）——词典导入：https://zhuanlan.zhihu.com/p/539464788

我的NLP（自然语言处理）历程（10）——相关系数：https://zhuanlan.zhihu.com/p/541794935

我的NLP（自然语言处理）历程（11）——疯狂的麦克斯：https://zhuanlan.zhihu.com/p/542073251

我的NLP（自然语言处理）历程（12）——分词算法：https://zhuanlan.zhihu.com/p/542550863

我的NLP（自然语言处理）历程（13）——断句算法：https://zhuanlan.zhihu.com/p/542904661

我的NLP（自然语言处理）历程（14）——基于相关系数的分词算法：https://zhuanlan.zhihu.com/p/552443996

我的NLP（自然语言处理）历程（15）——相关系数与词性检测：https://zhuanlan.zhihu.com/p/555630299

我的NLP（自然语言处理）历程（16）——提取数量词：https://zhuanlan.zhihu.com/p/557053336

我的NLP（自然语言处理）历程（17）——信息熵与分词：https://zhuanlan.zhihu.com/p/557433900

我的NLP（自然语言处理）历程（18）——分词最后环节：https://zhuanlan.zhihu.com/p/558171316

我的NLP（自然语言处理）历程（19）——词性检测：https://zhuanlan.zhihu.com/p/560504920

---

给作者捐赠：

<div align=center>
<img src="https://github.com/forestluo/AlgMain/blob/main/weixin.jpg" width="210px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/forestluo/AlgMain/blob/main/zhifubao.jpg" width="210px">
</div>
