# Web Scraper for DataWarehouse.DBD.go.th

This project demonstrates how to scrape financial and legal entity data from the DBD Data Warehouse website using Python, `requests`, and `BeautifulSoup`. It handles session management, form submissions, and table parsing to extract meaningful information.

## Features
- Establishes a session and retrieves cookies for authentication.
- Handles redirections and session persistence.
- Performs both `GET` and `POST` requests to fetch and scrape data.
- Extracts specific data from HTML tables, such as income, expenses, and profit for legal entities.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- pip (Python package installer)

### Required Python Libraries
Install the required libraries using:
```bash
pip install requests beautifulsoup4
```

## Project Structure
- **main.py**: Contains the Python code for web scraping.
- **README.md**: Documentation for the project.

## How to Run
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## Workflow
1. The script starts by visiting the DBD Data Warehouse index page to establish a session.
2. It performs a `GET` request to retrieve initial data, handling cookies and redirections.
3. Data is extracted from tables using `BeautifulSoup`:
   - Legal entity counts
   - Financial data (income, expenses, profit)
4. A `POST` request is sent with specific form data to retrieve additional information.
5. The results are printed to the console.

## Code Breakdown
### Session Initialization
```python
session = requests.Session()
response = session.get(index_url, headers=headers)
```
Establishes a session and retrieves cookies from the index page.

### Data Extraction
- **Table Parsing**:
```python
soup = BeautifulSoup(data_response.text, "html.parser")
table = soup.find("table", class_="table table-bordered table-striped table-hover text-end")
```
Finds and parses the desired table by class name.

- **Row and Column Handling**:
```python
rows = table.find_all("tr")
columns = rows[1].find_all("td")
values = [col.get_text(strip=True) for col in columns]
```
Extracts rows, columns, and text data.

### POST Request for Financial Data
```python
form_data = {"yearFilter": "2566", "compareType": "YEAR", ...}
finance_data_response = session.post(post_url, headers=headers, data=form_data)
```
Submits a form with parameters to retrieve specific financial data.

## Example Output
```
จำนวนนิติบุคคล = 12345
รายได้รวม (64-66): ['100,000', '200,000', '300,000']
รายจ่ายรวม (64-66): ['50,000', '100,000', '150,000']
กำไร (64-66): ['50,000', '100,000', '150,000']
จำนวนนิติ (64-66): ['500']
นิติมีกำไร (64-66): ['300']
นิติขาดทุน (64-66): ['200']
```

## Notes
- Ensure the `User-Agent` header mimics a real browser to prevent the server from blocking requests.
- Cookies are crucial for successful requests, especially when dealing with authentication or session management.
- If the HTML structure changes, the scraping logic might need adjustments.

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

---
Feel free to contribute to this project by submitting issues or pull requests.
