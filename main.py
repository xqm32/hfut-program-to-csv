import httpx
import hashlib
import json
import pandas


class EAMS:
    base_url = "http://jxglstu.hfut.edu.cn/eams5-student"

    def __init__(self, config=None) -> None:
        self.client = httpx.Client(follow_redirects=True)

        if config is None:
            username = input("username: ")
            password = input("password: ")
        else:
            with open(config) as f:
                config = json.load(f)
                username = config["username"]
                password = config["password"]

        salt = self.client.get(f"{EAMS.base_url}/login-salt").text
        password = hashlib.sha1((salt + "-" + password).encode()).hexdigest()

        resp = self.client.post(
            f"{EAMS.base_url}/login",
            json={
                "username": username,
                "password": password,
            },
        )

        if resp.json()["result"] == False:
            raise Exception("Login failed")

        resp = self.client.get(f"{EAMS.base_url}/for-std/program-completion-preview")
        self.student_id = str(resp.url).rsplit("/", maxsplit=1)[1]

    def to_csv(self) -> None:
        data_list = []

        resp = self.client.get(
            f"{EAMS.base_url}/for-std/program-completion-preview/json/{self.student_id}"
        )
        # with open("preview.json", "w") as f:
        #     f.write(resp.text)

        if resp.text == "null":
            data_list = self.__unadited()
        else:
            data = resp.json()
            for i in data["moduleList"]:
                data_list.extend(i["courseList"])
            data_list.extend(data["outerCourseList"])

        df = pandas.DataFrame(data_list)
        df.to_csv(f"{self.student_id}.csv", index=False)

    def __unadited(self) -> list:
        data_list = []
        grade = self.__grade()

        resp = self.client.get(
            f"http://jxglstu.hfut.edu.cn/eams5-student/for-std/program/root-module-json/{self.student_id}"
        )
        # with open("module.json", "w") as f:
        #     f.write(resp.text)

        data = resp.json()
        for i in data["children"]:
            for j in i["planCourses"]:
                code = j["course"]["code"]

                if code not in grade.index:
                    result_type = "UNREPAIRED"
                    gp, score = "", ""
                else:
                    result_type = "PASSED"
                    gp = grade.loc[code]["绩点"]
                    score = grade.loc[code]["成绩"]

                data_list.append(
                    {
                        "planCourseId": j["id"],
                        "courseId": j["course"]["id"],
                        "code": code,
                        "nameZh": j["course"]["nameZh"],
                        "nameEn": j["course"]["nameEn"],
                        "credits": j["course"]["credits"],
                        "terms": j["terms"],
                        "compulsory": j["compulsory"],  # TODO 是否必修
                        "resultType": result_type,
                        "score": score,
                        "rank": "",
                        "gp": gp,
                        "remark": "",
                        "finalResultType": "",
                    }
                )

        return data_list

    def __grade(self) -> pandas.DataFrame:
        resp = self.client.get(
            f"{EAMS.base_url}/for-std/grade/sheet/info/{self.student_id}"
        )
        sheet = pandas.read_html(resp.text)
        return pandas.concat(sheet).set_index("课程代码")


EAMS("config.json").to_csv()
