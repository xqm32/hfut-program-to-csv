# 合肥工业大学培养方案表格化工具

## 安装 hfut-program-to-csv

在 [Release](https://github.com/xqm32/hfut-program-to-csv/releases) 中下载 `hfut-program-to-csv` 的最新版本，并执行如下命令（请替换命令中的 `<VERSION>` 为具体的版本号）：

```sh
pip install hfut_program_to_csv-<VERSION>-py3-none-any.whl
```

## 使用方法

### 方法一：键入学号和密码

执行如下命令：

```sh
hfut_program_to_csv
```

输入学号和密码，在当前目录下生成的 `.csv` 文件即为表格化的培养方案 

### 方法二：通过配置文件获取学号和密码

创建 `config.json` 文件如下：

```json
{
    "username": "你的学号",
    "password": "你的教务系统密码"
}
```

执行如下命令：

```sh
hfut_program_to_csv -c config.json
```

在当前目录下生成的 `.csv` 文件即为表格化的培养方案 