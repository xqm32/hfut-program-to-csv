import httpx
import hashlib
import json
import pandas

client = httpx.Client(follow_redirects=True)

username, password = "", ""
with open("config.json") as f:
    config = json.load(f)
    username, password = config["username"], config["password"]

salt = client.get("http://jxglstu.hfut.edu.cn/eams5-student/login-salt").text
password = hashlib.sha1((salt + "-" + password).encode()).hexdigest()

resp = client.post(
    "http://jxglstu.hfut.edu.cn/eams5-student/login",
    json={
        "username": username,
        "password": password,
    },
)
assert resp.json()["result"] == True

resp = client.get(
    "http://jxglstu.hfut.edu.cn/eams5-student/for-std/program-completion-preview"
)
json_url = str(resp.url).replace("info", "json")
id = str(resp.url).rsplit("/", maxsplit=1)[1]

# with open(f"{id}.json", "w") as f:
#     resp = client.get(json_url)
#     f.write(resp.text)

data_list = []

resp = client.get(json_url)
if resp.text == "null":
# if True:
    resp = client.get(
        f"http://jxglstu.hfut.edu.cn/eams5-student/for-std/program/root-module-json/{id}"
    )
    data = resp.json()

    # with open(f"{id}.json", "w") as f:
    #     f.write(resp.text)

    for i in data["children"]:
        for j in i["planCourses"]:
            data_list.append(
                {
                    "id": j["id"],
                    "terms": j["terms"],
                    "nameZh": j["course"]["nameZh"],
                    "nameEn": j["course"]["nameEn"],
                    "code": j["course"]["code"],
                    "credits": j["course"]["credits"],
                    "defaultExamMode": j["course"]["defaultExamMode"]["nameZh"],
                    "type": i["type"]["nameZh"],
                }
            )
else:
    data = resp.json()
    for i in data["moduleList"]:
        data_list.extend(i["courseList"])

df = pandas.DataFrame(data_list)
df.to_csv(f"{id}.csv", index=False)
