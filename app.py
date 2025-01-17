import requests
import time
from bs4 import BeautifulSoup

# Step 1: Visit the index page to establish a session and retrieve cookies
session = requests.Session()
index_url = "https://datawarehouse.dbd.go.th/index"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://datawarehouse.dbd.go.th/index",  # Adjust based on the actual referrer
}
response = session.get(index_url, headers=headers)

if response.status_code == 200:
    data_url = "https://datawarehouse.dbd.go.th/searchBusinessObject/18122?type=business"
    data_response = session.get(data_url, headers=headers)

    if data_response.status_code == 200:
        soup = BeautifulSoup(data_response.text, "html.parser")
        table = soup.find("table", class_="table table-bordered table-striped table-hover text-end" ) 

        if table:
            rows = table.find_all("tr")
            columns = rows[1].find_all("td")  
            values = [col.get_text(strip=True) for col in columns]
            print("จำนวนนิติบุคคล = ", values[3])
        else:
            print("Table not found.")
            
        post_url = "https://datawarehouse.dbd.go.th/business/condensed/year/18122"
        form_data = {
            "yearFilter": "2566",
            "compareType": "YEAR",
            "compareBizSize": "ALL",
            "compareBizArea": "",
            "compareBizPv": "",
            "compareAvgType": "MEDIAN",
            "comparePage": "condensed",
            "module": "BIZ"
        }

        finance_data_response = session.post(post_url, headers=headers, data=form_data)
        if finance_data_response.status_code == 200:
            soupFinance = BeautifulSoup(finance_data_response.text, "html.parser")
            tableFinance = soupFinance.find("table", class_="table table-hover text-end" ) 
            if tableFinance:
                row_table_finance = tableFinance.find_all("tr")

                totalIncome = row_table_finance[4].find_all("td") 
                totalExpense = row_table_finance[6].find_all("td")
                totalProfit = row_table_finance[7].find_all("td")

                numOflegalEntities = row_table_finance[8].find_all("th")
                del numOflegalEntities[0]
                numOfLegalEntitiesWithProfile = row_table_finance[9].find_all("td")
                numOfLegalEntitiesWithOutProfile = row_table_finance[10].find_all("td")

                print("รายได้รวม (64-66):", [col.get_text(strip=True) for col in totalIncome])
                print("รายจ่ายรวม (64-66):", [col.get_text(strip=True) for col in totalExpense])
                print("กำไร (64-66):", [col.get_text(strip=True) for col in totalProfit])
                print("จำนวนนิติ (64-66):", [col.get_text(strip=True) for col in numOflegalEntities])
                print("นิติมีกำไร (64-66):", [col.get_text(strip=True) for col in numOfLegalEntitiesWithProfile])
                print("นิติขาดทุน (64-66):", [col.get_text(strip=True) for col in numOfLegalEntitiesWithOutProfile])
            else:
                print("Table not found.")
        else:
            print(f"Request failed with status code: {finance_data_response.status_code}")
    else:
        print(f"Failed to access the data URL. Status code: {data_response.status_code}")
else:
    print(f"Failed to access the data URL. Status code: {response.status_code}")