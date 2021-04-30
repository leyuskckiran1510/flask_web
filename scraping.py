from bs4 import BeautifulSoup as bs
import requests
import pprint

from urllib3.connection import ConnectionError


def scrape(query):
    if query != "":
        headers = {
            "method": "GET",
            "scheme": "https",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "0",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) \
            AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        jason_data = []
        sastoDL_url = "https://www.sastodeal.com/catalogsearch/result/?q={}".format(query)
        try:
            thulo_url = "https://thulo.com/search/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=\
            Y&pkeywords=Y&search_performed=Y&cid=0&q={}&security_hash=9538cf3fb88a7c54561d39312d499a99".format(
                query)
            response_thulo = requests.get(thulo_url, headers=headers)
            soup_thulo = bs(response_thulo.text, "html.parser")
            soup_thulo = soup_thulo.find_all("div", {"class": "et-column4 et-grid-item-wrapper"})
            thulo_min_lis = []
            for sn, i in enumerate(soup_thulo):
                pseudo_lis = []
                ''' <img class="ty-pict cm-image et_js" 
                id="det_img_3445" 
                data-cfsrc="./design/themes/vivashop/media/images/et-empty.png" 
                alt="" title="" width="239" height="239" 
                src="https://thulo.com/images/thumbnails/239/239/detailed/5/_MG_8751.jpg">'''
                pseudo_lis.append(i.find_all("img")[0].get("data-src"))
                pseudo_lis.append("From Thulo :- {}".format(i.find('bdi').text))
                pseudo_lis.append(i.find_all('a')[0].get('href'))
                pseudo_lis.append(i.find('span', {'class': 'ty-price'}).text)
                thulo_min_lis.append(list(pseudo_lis))
            jason_data.insert(0, thulo_min_lis)
        except Exception as e:
            jason_data.insert(0, [[
                                      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse\
                                      1.mm.bing.net%2Fth%3Fid%3DOIP.UfjWfAaC10VN7p1s-r9KWQE0DK%26pid%3DApi&f=1",
                                      "Error Fetching Data From Thulo", "", "ERROR"]])
        try:
            response_sasto = requests.get(sastoDL_url, headers=headers)
            soup_sasto = bs(response_sasto.text, "html.parser")
            soup_sasto = soup_sasto.find("div", {"class": "products wrapper grid products-grid"})
            soup_sasto = soup_sasto.find_all("li", {"class": "item product product-item"})
            # sastoDL_link_dic={}
            xyz = []
            for no, i in enumerate(soup_sasto):
                pseudo_dic = {"name": "", "link": "", "price": ""}
                pseudo_lis = [i.find_all("img")[0].get("data-cfsrc")]
                for sn, link in enumerate((i.find_all('a', {"class": "product-item-link"}))):
                    pseudo_lis.append("From SastoDeal :- {}".format(link.text))
                    pseudo_lis.append(link.get('href'))
                sasto_price = i.find_all('span', {"class": "price-container price-final_price tax weee"})
                for lol in sasto_price:
                    try:
                        pseudo_lis.append(lol.text)
                    except IndexError:
                        pass
                xyz.append(list(pseudo_lis))
            jason_data.insert(1, xyz)
        except ConnectionError as c:
            jason_data.insert(1, [[
                "404.jfif",
                "Error Fetching Data From SASTO", "", "CERROR"
            ]])
        except Exception as e:
            jason_data.insert(1, [[
                                      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net\
                                      %2Fth%3Fid%3DOIP.UfjWfAaC10VN7p1s-r9KWQE0DK%26pid%3DApi&f=1",
                                      "Error Fetching Data From Sasto ", "", "ERROR"]])
        return jason_data


if __name__ == "__main__":
    query = input("ENTER A PRODUCT NAME  ")
    pprint.pprint(scrape(query))
