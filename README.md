# README

通过生成csv解决wakeup无法直接解析buaa本科生新教务学期课程表的问题

## Usage

```
pip install -r requirements.txt
python3 main.py
```

然后根据提示输入内容即可获得`schedule.csv`

保存并导入wakeup即可

## 导入日历

支持生成ics文件，让你彻底不用给~~wakeup掏钱~~

生成ics文件导入日历的方法可以参考[该链接](https://jackyu.cn/tech/apple-ics-import/)

## 登录失败

如果出现登录失败，请检查：

- 账号密码是否正确
- 本机是否开启代理，若开启可能存在登录失败问题，请手动配置代码7行的`proxies`；若本机没有开启代理请将该字典注释掉，并且在下方代码中自行删除掉所有request中的`proxies=proxies`的字段
- 当前代码中默认使用了`burpsuite`的8080端口代理，没有开启代理的请按照上一条删除该代理配置
- 或者~~多试几次~~，可能是获取`CASTGC`的API存在retry时间间隔限制，我们至今仍未知为什么会登录失败（误）