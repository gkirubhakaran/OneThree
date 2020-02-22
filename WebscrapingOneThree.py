import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup

#This function is to determine whether DrugIDs are provided by the user or to use the PreDefined DrugIDs
#using sys package this function reads Drug ID provided at the terminal
def DetermineProcess():
    global process, DrugIDs
    if len(sys.argv) == 1:
        process = 'PreDefined'
        DrugIDs = ['DB00619','DB01048','DB14093','DB00173','DB00734','DB00218','DB05196','DB09095','DB01053','DB00274']
    elif len(sys.argv) == 2:
        process = 'Selective'
        string = sys.argv[1]
        DrugIDs = string.split(',')
    else:
        process = 'Incorrect'
        print('Please provide maximum of one argument with DrugIDs separated by comma')
        
#This function is to request the data from the webpage and check if the status is success 
#Also parse the HTML content to scrape the text we are looking for
def ScrapeDrugBank(DrugID):
    URL = "https://www.drugbank.ca/drugs/"
    Endpoint = DrugID
    page = requests.get( URL + Endpoint )
    pageHTML = page.content
    soup = BeautifulSoup(pageHTML, 'lxml')
    dl_data=soup.find('div','bond-list-container targets')
    return page.status_code,dl_data
    
#This function converts the HTML text to structured pandas dataframe    
def HTMLToDataTable(DrugID,HTMLText):
    res_text=[]
    for item in list(zip(HTMLText.find_all("dt"),HTMLText.find_all("dd"))):
        var , val = item
        res_text.append([', '.join([var.text, val.text])])
    df = pd.DataFrame.from_records(res_text, columns = ['text'])
    df = pd.DataFrame(df.text.str.split(',',1).tolist(),columns = ['category','values'])
    df ['DrugID'] = DrugID
    df = df[df['category']=="Gene Name"][["DrugID","values"]]
    df.columns = ["DrugID","GeneName"]
    return df
    
#Following lines of code are equivalent to running a main() function
#First check whether to run for a specific DrugID or PreDefined list
#Second check the API status 
#Third check whther Target GeneName is available in DrugBank webpage
#If steps 1,2 and 3 are successful then display the dataframe (I have commented the last line which allows you to store the output in an excel file)
DetermineProcess()
if process != 'Incorrect':
    output_df=pd.DataFrame(columns=['DrugID', 'GeneName'])
    for DrugID in DrugIDs:
        status, text_data=ScrapeDrugBank(DrugID)
        if status != 200:
            print ("Unsuccessful API Endpoint for ",DrugID,". Please try different Drug ID")
        elif status == 200 and text_data is None:
            print ("Target Gene for ", DrugID," is currently unavailable at Drug Bank")
            output_df=output_df.append({'DrugID':DrugID,'GeneName':"NA"}, ignore_index=True)
        else:
            output_df=output_df.append(HTMLToDataTable(DrugID,text_data))
    if not output_df.empty:
        print(output_df.to_string(index=False))
        #output_df.to_excel('TargetGeneDrugID.xlsx','Sheet1',index=False)

