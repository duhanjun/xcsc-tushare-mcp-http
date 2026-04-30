## 中国Wind基金分类

___

接口：fund\_sector

描述：记录基金的Wind分类信息

限量：单次最大10000条

**输入参数**

|名称|类型|必选|描述|
|---|---|---|---|
|ts\_code|str|N|基金代码|
|sector|str|N|所属板块|
|cur\_sign|str|N|最新标志|
|start\_date|str|N|开始日期|
|end\_date|str|N|结束日期|

**输出参数**

|名称|类型|默认显示|描述|
|---|---|---|---|
|ts\_code|str|Y|基金代码|
|s\_info\_sector|str|Y|所属板块|
|s\_info\_sectorentrydt|str|Y|起始日期|
|s\_info\_sectorexitdt|str|Y|截止日期|
|cur\_sign|str|Y|最新标志|

**接口示例**

```python

df=pro.fund_sector(ts_code='001703.OF')
```

**数据示例**

```

      ts_code     s_info_sector  ... s_info_sectorexitdt cur_sign
0   001703.OF        2001030200  ...                None        1
1   001703.OF        2001031400  ...                None        1
2   001703.OF        2001030600  ...                None        1
3   001703.OF        2001031300  ...            20180430        0
4   001703.OF        2001110300  ...                None        1
5   001703.OF        2001030100  ...            20180430        0
6   001703.OF        2001030400  ...            20170831        0
7   001703.OF        2001030700  ...            20170831        0
8   001703.OF  2001010101000000  ...                None        1
9   001703.OF        2001024800  ...                None        1
10  001703.OF        2001060100  ...                None        1
11  001703.OF        2001070100  ...                None        1
```