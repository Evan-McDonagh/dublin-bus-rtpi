# import requests
#
#
# def rtmarkerinfo(stop_id):
#     url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation" +"?stopid=" + stop_id+"&format=json"
#     obj = requests.get(url)
#     obj_json = obj.json()
#     print(obj_json)
#     # allinfo = "Stop No." + obj_json.get('stopid') +"<br>"
#     # rsp ={obj_json.get('stopid'): []}
#     # for result in obj_json['results']:
#     #     key = result.get('route')
#     #     rsp[obj_json.get('stopid')].append({key: {'arrivaltime':result.get('arrivaldatetime'), 'destination':result.get('destination')}})
#     #     allinfo += "Route:"+ key + "  arrive at:" + result.get('arrivaldatetime') + " Towards " + result.get('destination') +"<br>"
#     # print(rsp)
#         # return HttpResponse(json.dumps({"allinfo":allinfo}))
#
# rtmarkerinfo("848")
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://book.douban.com/')
print(browser.page_source)
browser.close()
