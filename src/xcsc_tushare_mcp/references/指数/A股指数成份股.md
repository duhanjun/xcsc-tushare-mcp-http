## A股指数成份股

___

接口：index\_members

描述：获取各类指数成分

限量：单次最大10000条

**输入参数**

|名称|类型|必选|描述|
|---|---|---|---|
|ts\_code|str|N|ts代码|
|cur\_sign|str|N|最新标志 0-否,1-是|
|start\_date|str|N|开始日期|
|end\_date|str|N|结束日期|

**输出参数**

|名称|类型|默认显示|描述|
|---|---|---|---|
|ts\_code|str|Y|ts代码|
|con\_ts\_code|str|Y|成份股ts代码|
|in\_date|str|Y|纳入日期|
|out\_date|str|Y|剔除日期|
|cur\_sign|float|Y|最新标志|

**接口调用**

```python
pro = ts.pro_api(your token)
df = pro.index_members(ts_code="000300.SH")
```

**数据样例**

```
    ts_code con_ts_code   in_date  out_date  cur_sign
0    000300.SH   600649.SH  20050408  20180608         0
1    000300.SH   000402.SZ  20050408  20191213         0
2    000300.SH   600739.SH  20050408  20190614         0
3    000300.SH   000792.SZ  20050408  20190614         0
4    000300.SH   000060.SZ  20050408  20181214         0
..         ...         ...       ...       ...       ...
351  000300.SH   600989.SH  20191216      None         1
352  000300.SH   601236.SH  20191216      None         1
353  000300.SH   601698.SH  20191216      None         1
354  000300.SH   603501.SH  20191216      None         1
355  000300.SH   603899.SH  20191216      None         1
```