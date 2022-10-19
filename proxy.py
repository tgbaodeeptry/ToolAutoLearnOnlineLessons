import requests
import json


def get_ips():
    url = "https://proxypage1.p.rapidapi.com/v1/tier1"

    querystring = {"type": "HTTP", "limit": "100", "country": "VN"}

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "1594de5ea2msh9b693575fa3ba9ap1fda7ejsnc2fab8798186",
        'x-rapidapi-host': "proxypage1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    d = json.loads(response.text, strict=False)

    return [f"{x['ip']}:{x['port']}" for x in d]

    # headers = {
    #         'content-type': "application/x-www-form-urlencoded",
    # }
    #
    # url = "https://api.getproxylist.com/proxy?country[]=VN"
    # response = requests.request("GET", url, headers=headers)
    #
    # d = json.loads(response.text, strict=False)
    #
    # return [f"{d['ip']}:{d['port']}"]
