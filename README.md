# 合肥工业大学培养方案表格化工具

## 安装依赖

```sh
pip install -r requirements.txt
```

## 使用方法

创建 `config.json` 文件如下：

```json
{
    "username": "你的学号",
    "password": "你的教务系统密码"
}
```

执行如下命令：

```sh
python main.py
```

在部分操作系统上，你可能需要执行：

```sh
python3 main.py
```

在当前目录下生成的 `.csv` 文件即为表格化的培养方案 