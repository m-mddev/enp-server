import copy
import sys
import requests
from bs4 import BeautifulSoup

sys.setrecursionlimit(10000)

header_template = {
    "title": "title_placeholder",
    "type": "type_placeholder",
    "ukp": "ukp_placeholder",
    "usp": "usp_placeholder"
}

di_body_template = {
    "entrys": []
}

entry_template = {
    "sub_entry": []
}

entry_body_element_template = {
    "header": {},
    "body": {}
}

dsense_template = {
    "header": {},
    "defenitions": []
}

defenition_template = {
    "defenition": "",
    "where_to_use": "",
    "examples": []
}

body_template = {
    "dsense": []
}



URL = "https://dictionary.cambridge.org/us/dictionary/english/"
HEADER = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

def scrape(word: str):
    new_di_body = copy.deepcopy(di_body_template)


    # downloading related html
    html = requests.get(URL + word, headers=HEADER)

    # load html to bs4
    full_page = BeautifulSoup(html.content, "html.parser")

    # here we get the all di_body that represent each dictionary e.g advanced, learner
    di_body = full_page.find_all("div", class_="di-body")

    # if its advaned dictionary
    entry_body_array = di_body[0].find_all("div", class_="entry-body")
    
    for entry_body in entry_body_array:
        new_entry_body = copy.deepcopy(entry_template)
        new_di_body["entrys"].append(new_entry_body)
        entry_body_element_array = entry_body.find_all('div', class_="pr entry-body__el")

        for entry_body_element in entry_body_element_array:
            new_entry_body_element = copy.deepcopy(entry_body_element_template)
            new_entry_body["sub_entry"].append(new_entry_body_element)
            
            ############################# header ######################################
            new_header = copy.deepcopy(header_template)
            new_entry_body_element["header"] = new_header
            new_header["title"] = entry_body_element.find('div', class_="di-title").text    
            new_header["type"] = entry_body_element.find('div', class_="posgram dpos-g hdib lmr-5").text
            new_header["usp"] = entry_body_element.find('span', class_="us dpron-i").find('span', class_="pron dpron").text
            new_header["ukp"] = entry_body_element.find('span', class_="uk dpron-i").find('span', class_="pron dpron").text
            ############################# body #########################################
            
            dsense_array = entry_body_element.find_all("div", class_=["pr", "dsense"])
            new_body = copy.deepcopy(body_template)
            new_entry_body_element["body"] = new_body
            
            for dsense in dsense_array:
                new_dsense = copy.deepcopy(dsense_template)
                new_body["dsense"].append(new_dsense)
                
                try:
                    new_dsense["header"] = " ".join(dsense.find("h3", class_="dsense_h").text.split())
                except:  # noqa: E722
                    pass
                defenition_block_array = dsense.find_all("div", class_="def-block ddef_block")
                
                for defenition_block in defenition_block_array:
                    new_defenition_block = copy.deepcopy(defenition_template)
                    new_defenition_block["defenition"] = " ".join(defenition_block.find("div", class_="def ddef_d db").text.split())
                    new_dsense["defenitions"].append(new_defenition_block)
                    try:
                        new_defenition_block["where_to_use"] = defenition_block.find("span", class_="gram dgram").text
                    except:  # noqa: E722
                        pass
                    examples = defenition_block.find_all("div", "examp dexamp")
                    for example in examples:
                        new_defenition_block["examples"].append(example.text)

    return new_di_body