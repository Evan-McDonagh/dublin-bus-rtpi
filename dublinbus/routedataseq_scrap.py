import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup


# A script to scrap stop data from https://www.dublinbus.ie/RTPI/Sources-of-Real-Time-Information
# driver = webdriver.Chrome('/usr/local/bin/chromedriver')
routes_list = []
routes_dict = {}
# browser = webdriver.Chrome()
# browser.set_window_size(1000, 300000)
routes = '<ul class="rcbList"><li class="rcbItem">1</li><li class="rcbItem">1c</li><li class="rcbItem">4</li><li class="rcbItem">7</li><li class="rcbItem">7a</li><li class="rcbItem">7b</li><li class="rcbItem">7d</li><li class="rcbItem">9</li><li class="rcbItem">11</li><li class="rcbItem">13</li><li class="rcbItem">14</li><li class="rcbItem">14c</li><li class="rcbItem">15</li><li class="rcbItem">15a</li><li class="rcbItem">15b</li><li class="rcbItem">15d</li><li class="rcbItem">15e</li><li class="rcbItem">16</li><li class="rcbItem">16c</li><li class="rcbItem">16d</li><li class="rcbItem">25</li><li class="rcbItem">25a</li><li class="rcbItem">25b</li><li class="rcbItem">25d</li><li class="rcbItem">25x</li><li class="rcbItem">26</li><li class="rcbItem">27</li><li class="rcbItem">27a</li><li class="rcbItem">27b</li><li class="rcbItem">27x</li><li class="rcbItem">29a</li><li class="rcbItem">31</li><li class="rcbItem">31a</li><li class="rcbItem">31b</li><li class="rcbItem">31d</li><li class="rcbItem">32</li><li class="rcbItem">32x</li><li class="rcbItem">33</li><li class="rcbItem">33d</li><li class="rcbItem">33e</li><li class="rcbItem">33x</li><li class="rcbItem">37</li><li class="rcbItem">38</li><li class="rcbItem">38a</li><li class="rcbItem">38b</li><li class="rcbItem">38d</li><li class="rcbItem">39</li><li class="rcbItem">39a</li><li class="rcbItem">39x</li><li class="rcbItem">40</li><li class="rcbItem">40b</li><li class="rcbItem">40d</li><li class="rcbItem">40e</li><li class="rcbItem">41</li><li class="rcbItem">41a</li><li class="rcbItem">41b</li><li class="rcbItem">41c</li><li class="rcbItem">41d</li><li class="rcbItem">41x</li><li class="rcbItem">42</li><li class="rcbItem">42d</li><li class="rcbItem">43</li><li class="rcbItem">44</li><li class="rcbItem">44b</li><li class="rcbItem">46a</li><li class="rcbItem">46e</li><li class="rcbItem">47</li><li class="rcbItem">49</li><li class="rcbItem">51d</li><li class="rcbItem">51x</li><li class="rcbItem">53</li><li class="rcbItem">53a</li><li class="rcbItem">54a</li><li class="rcbItem">56a</li><li class="rcbItem">61</li><li class="rcbItem">65</li><li class="rcbItem">65b</li><li class="rcbItem">66</li><li class="rcbItem">66a</li><li class="rcbItem">66b</li><li class="rcbItem">66e</li><li class="rcbItem">66x</li><li class="rcbItem">67</li><li class="rcbItem">67x</li><li class="rcbItem">68</li><li class="rcbItem">68a</li><li class="rcbItem">68x</li><li class="rcbItem">69</li><li class="rcbItem">69x</li><li class="rcbItem">70</li><li class="rcbItem">70d</li><li class="rcbItem">77a</li><li class="rcbItem">77x</li><li class="rcbItem">79</li><li class="rcbItem">79a</li><li class="rcbItem">83</li><li class="rcbItem">83a</li><li class="rcbItem">84</li><li class="rcbItem">84a</li><li class="rcbItem">84x</li><li class="rcbItem">116</li><li class="rcbItem">118</li><li class="rcbItem">120</li><li class="rcbItem">122</li><li class="rcbHovered">123</li><li class="rcbItem">130</li><li class="rcbItem">140</li><li class="rcbItem">142</li><li class="rcbItem">145</li><li class="rcbItem">150</li><li class="rcbItem">151</li><li class="rcbItem">155</li><li class="rcbItem">747</li><li class="rcbItem">757</li></ul>'
# browser.get('https://www.dublinbus.ie/RTPI/Sources-of-Real-Time-Information/?searchtype=route')
# browser.find_element_by_xpath('//a[@id="ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeSearch1_radComboBoxRoute_Arrow"]').click()
# # browser.find_element_by_xpath('//a[@id="ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeSearch1_radComboBoxRoute_MoreResultsBoxImage"]').click()
# # browser.find_elements_by_id('ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeSearch1_radComboBoxRoute_DropDown')
# browser.find_elements_by_xpath('//input[@id="ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeSearch1_radComboBoxRoute_Input"]').click()
# browser.execute_script("window.scrollBy(0, 180000);")
# time.sleep(1)
# time.sleep(2)
# print(browser.page_source)
soup = BeautifulSoup(routes, "html.parser")

for i in soup.find_all('li'):
    rt = str(i.get_text()).replace(' ', '').replace('\n', '')
    routes_list.append(rt)
print(routes_list)
print(len(routes_list))
# browser.quit()
# print(browser.page_source)
# with open("./local-bus-data/route-data.json") as RT:
#     allroutes = json.load(RT)
#     for route in allroutes:
#         routes_list.append(route)
#     RT.close()
# print(routes_list)
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

