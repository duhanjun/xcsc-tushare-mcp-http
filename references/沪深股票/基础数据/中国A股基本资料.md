## 中国A股基本资料

___

接口：stock\_basic

描述：获取基础信息数据，包括股票代码、名称、上市日期、退市日期等

限量：单次最大10000条

**输入参数**

|名称|类型|必选|描述|
|---|---|---|---|
|ts\_code|str|N|股票代码，可输入多个，如000002.SZ,000001.SZ|
|exchange|str|N|交易所 SSE上交所 SZSE深交所|
|is\_shsc|int|N|是否在沪股通或深港通范围内,0:否;1:沪股通;2:深股通|
|start\_date|str|N|开始日期|
|end\_date|str|N|结束日期|

**输出参数**

|名称|类型|默认显示|描述|
|---|---|---|---|
|ts\_code|str|Y|TS代码|
|symbol|str|Y|股票交易代码|
|name|str|Y|证券简称|
|comp\_name|str|Y|公司中文名称|
|comp\_name\_en|str|Y|公司英文名称|
|isin\_code|str|Y|ISIN代码|
|exchange|str|Y|交易所|
|list\_board|str|Y|上市板类型|
|list\_date|str|Y|上市日期|
|delist\_date|str|Y|退市日期|
|crncy\_code|str|Y|货币代码|
|pinyin|str|Y|简称拼音|
|list\_board\_name|str|Y|上市板|
|is\_shsc|int|Y|是否在沪股通或深港通范围内,0:否;1:沪股通;2:深股通|
|comp\_code|str|Y|公司代码|

**接口示例**

```python

pro = ts.pro_api()
data = pro.stock_basic(ts_code='000002.SZ,000001.SZ,',fields="ts_code,symbol,name,comp_name")
```

**数据样例**

```
        ts_code  symbol   comp_name
0  000001.SZ  000001  平安银行股份有限公司
1  000002.SZ  000002  万科企业股份有限公司
```