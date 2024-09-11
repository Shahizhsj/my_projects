from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading
import concurrent.futures
import gradio as gr
def res(name):
    opt = Options()
    opt.add_argument('--headless')
    dr = webdriver.Chrome(options=opt)
    dr.get('https://www.mysmartprice.com/')
    search_box = WebDriverWait(dr, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '.srch-wdgt__fld.js-atcmplt.js-hdr-srch.js-srch-lght.ui-autocomplete-input')))
    search_box.clear()
    search_box.send_keys(name)
    WebDriverWait(dr,20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,'a[tabindex="-1"]')))
    lis=dr.find_elements(By.CSS_SELECTOR,'a[tabindex="-1"]')
    count=0
    for i in lis:
        if(count==1):
            i.click() 
            break
        else:
            count=count+1
    price=WebDriverWait(dr,10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,'span[class="prdct-dtl__prc-val"]'))
    )
    data=WebDriverWait(dr,10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="kyspc clearfix"]'))
    )
    
    
    more_data=WebDriverWait(dr,10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="exprt-rvw__dtls clearfix"]'))
        )
    return f'Specs of {name} is \n{data.text } \n more about mobile is {more_data.text}'

with gr.Blocks() as demo:
    gr.Markdown(
        '''
enter the mobile mobels exactly as they are realsed 
'''
    )
    name_1=gr.Textbox(placeholder="Enter model name")
    name_2=gr.Textbox(placeholder="Enter model name")
    output=gr.Textbox()
    click=gr.Button('Compare!')
    @click.click(inputs=[name_1,name_2],outputs=output)
    def result(name_1,name_2):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            lis=[str(name_1),str(name_2)]
            re=executor.map(res,lis)
            s=""
            for i in re:
                s=s+'\n'+i+"\n"
            return s
demo.launch()
    
