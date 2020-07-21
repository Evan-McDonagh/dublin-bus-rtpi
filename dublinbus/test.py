import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup


# A script to scrap stop data from https://www.dublinbus.ie/RTPI/Sources-of-Real-Time-Information
# driver = webdriver.Chrome('/usr/local/bin/chromedriver')
routes_list = []
routes_dict = {}
with open("./local-bus-data/route-data.json") as rt:
    allroutes = json.load(rt)
    for route in allroutes:
        routes_list.append(route)
    rt.close()
print(routes_list)
# browser = webdriver.Chrome()
with open("./local-bus-data/route-data-sequence.json", 'w') as rds:
    for route in routes_list:
        browser = webdriver.Chrome()
        print(route)
        Route = {}
        browser.get('https://www.dublinbus.ie/RTPI/Sources-of-Real-Time-Information/?searchtype=route&searchquery={}'.format(route))
        # print(browser.page_source)
        view_directions = ['//a[@id="ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeRouteListing1_lnkViewInDirection"]', '//a[@id="ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeRouteListing1_lnkChangeDirection"]']
        for DIR in view_directions:
            # print(DIR)
            # browser.get('https://www.dublinbus.ie/RTPI/Sources-of-Real-Time-Information/?searchtype=route&searchquery={}'.format(route))
            # browser.find_element_by_xpath('//a[@id="ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeRouteListing1_lnkViewInDirection"]').click()
            try:
                browser.find_element_by_xpath(DIR).click()
                soup = BeautifulSoup(browser.page_source, "html.parser")
                # route = soup.select("#ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeRouteListing1_lblRouteNumber2")[0].get_text()
                # print(route)
                direction = soup.select("#ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeRouteListing1_lblRouteDirection")[0].get_text()
                Route[direction] = {}
                # print('lnkViewInDirection' in DIR)
                if ('lnkViewInDirection' in DIR):
                    Route[direction]['in/out'] = 'in'
                else:
                    Route[direction]['in/out'] = 'out'
                # print(Route[direction]['in/out'])
                Route[direction]['stops'] = []
                for i in soup.find_all('tr', class_=['even', 'odd']):
                    tdsoup = BeautifulSoup(str(i), "html.parser")
                    Route[direction]['stops'].append({
                        'stopno': str(tdsoup.find_all('td')[0].get_text()).replace(' ', '').replace('\n', ''),
                        'address': str(tdsoup.find_all('td')[1].get_text()).replace(' ', '').replace('\n', ''),
                        'location': str(tdsoup.find_all('td')[2].get_text()).replace(' ', '').replace('\n', ''),
                        'href': str(tdsoup.find_all('a')[0]['href']).replace(' ', '').replace('\n', '')
                    })
                # print(len(Route[direction]['stops']))
            except Exception:
                    print(route, Exception)
        browser.quit()
        routes_dict[route] = Route
        print(route, 'finish')
        # time.sleep(5)
        # print(routes_dict[route])

    routeswithseq = json.dumps(routes_dict)
    rds.write(routeswithseq)
    rds.close()

