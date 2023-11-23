
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
import pandas as pd

def content_items(row):
    details = row.split('•')
    items = {}
    items["Course-type"] =    details[0]
    items["Title"] =  details[1]
    items["University"] =          details[2]
    items["Location"] =   details[3]
    return items


def main():

    
    data = []

    driver = webdriver.Firefox()
    for i in range(23):
        print(i)

        if i == 0:
            offset = str("")
        else:
            offset = str(i*100)
        
        url = f'https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=&lang%5B%5D=&fos=&cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&limit=100&offset={offset}&display=list'

        driver.get(url)
        time.sleep(4)

        if i == 0:
            driver.find_element(By.CSS_SELECTOR,"button.snoop-button.qa-cookie-consent-accept-all").click()

            time.sleep(2)


        element = driver.find_element(By.XPATH,'/html/body/div[3]/main/div[2]/div[2]/div/div/div/div/div')
        b = element.find_elements(By.CLASS_NAME,'c-ad-carousel') 

        time.sleep(2)
        for i in b:
            merged_dict = {}

            inline_item = i.find_element(By.CLASS_NAME,'list-inline-item').text

            merged_dict.update(content_items(inline_item))
            
            z = i.find_elements(By.CLASS_NAME,'c-ad-carousel__content-list') 
            u = i.find_element(By.CLASS_NAME,'c-ad-carousel__content-list') 
            for k in z:
                dict2 = {}
                v = k.find_elements(By.CLASS_NAME,"c-ad-carousel__highlight")

                for g in v:
                    if g.text == "":
                        break

                    path = f".//h3[contains(text(),'{g.text}')]"

                    title_element = u.find_element(By.XPATH,path)
    
                    
                    data_element = title_element.find_element(By.XPATH,"following-sibling::span")
                    

                    dict2[g.text] =  data_element.text

            try:
            
                merged_dict['C-badge'] = i.find_element(By.CLASS_NAME,'c-badge').text
            except:
            
                merged_dict['C-badge'] = None


            merged_dict.update(dict2)

            data.append(merged_dict)


    df = pd.DataFrame(data)
    df.to_csv("daad_data.csv", index =False)      

    driver.close()
    driver.quit()

    return 



if __name__ == "__main__":
    main()







