import hashlib
import json


def get_url_login(user, password):
    user += "_c3pbchau.cr"

    return f"http://c3pbchau-cr.lms.vnedu.vn/service/security/login" \
           f"?redirect_url=&email={user}&password={hashlib.md5(password.encode()).hexdigest()}"


def get_ids_courses_not_finished(content):
    data = json.loads(content, strict=False)
    list_courses = data["data"]["listCourse"]
    ids = []

    for x in list_courses:
        if x["phan_tram_hoan_thanh"] != 100:
            ids.append(x["id"])

    return ids


def get_progress(content):
    data = json.loads(content, strict=False)
    list_courses = data["data"]["listCourse"]
    m = {}

    for x in list_courses:
        d = {
            "progress": x["phan_tram_hoan_thanh"],
            "name": x["name"]
        }

        m[x["id"]] = d

    return m

