# 🌍 FIFA Data Web Scraping Project ⚽

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.12.0-green?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12.2-orange?logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)

---

## 📝 Project Overview
This project is an **automated web scraping solution** to extract FIFA World Rankings and team statistics from the official FIFA website.  
The goal is to **collect, clean, and store football data** for analysis, visualization, or research purposes.

Key Highlights:
- Automated extraction of FIFA rankings and team information  
- Data cleaning and structured storage using **Pandas**  
- Integration of **Selenium** and **BeautifulSoup** for dynamic content  
- Exporting data to CSV for easy analysis  

---

## 🛠️ Tools & Technologies
| Technology | Purpose |
|------------|---------|
| Python 🐍 | Scripting and data handling |
| Selenium ⚡ | Browser automation for dynamic content |
| BeautifulSoup 🍲 | HTML parsing and data extraction |
| Pandas 📊 | Data structuring and CSV export |
| ChromeDriver 🌐 | Browser control for Selenium |
| Jupyter Notebook 📓 | Development and testing environment |

---

## 🧩 Project Workflow

### 1️⃣ Problem Identification
Manual extraction of FIFA rankings is time-consuming and prone to errors.  
This project automates the process to:
- Collect FIFA World Rankings  
- Capture team names, ranks, points, and country codes  
- Export the data in a structured format for analysis  

### 2️⃣ Web Scraping Strategy
#### Dynamic Content Handling
- Use **Selenium** to open and interact with FIFA’s dynamic pages  
- Wait for tables to fully load before parsing  

#### HTML Parsing
- Use **BeautifulSoup** to extract:
  - Team names 🏷️  
  - Ranking positions 🥇🥈🥉  
  - Points and statistics 📊  

---

## 🔧 Code Structure

### a) Importing Libraries
```python
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
```

### b) Setting up Selenium WebDriver
```python
service = Service("path_to_chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)
```

### c) Navigating FIFA Rankings Page
```python
url = "https://www.fifa.com/fifa-world-ranking/"
driver.get(url)
time.sleep(5)  # Wait for dynamic content to load
```

### d) Parsing Rankings Table
```python
soup = BeautifulSoup(driver.page_source, "html.parser")
teams = []
for row in soup.find_all("tr", class_="ranking-row"):
    rank = row.find("td", class_="rank").text.strip()
    team = row.find("td", class_="team-name").text.strip()
    points = row.find("td", class_="points").text.strip()
    teams.append([rank, team, points])

```

### e) Saving Data to CSV
```python
df = pd.DataFrame(teams, columns=["Rank", "Team", "Points"])
df.to_csv("FIFA_Rankings.csv", index=False)

```


---


## ⚡ Challenges & Solutions
| Challenge | Solution |
|------------|---------|
| Dynamic content loading	| Added time.sleep() and Selenium waits |
| Complex HTML structure	| Used browser inspect tools to locate elements |
| Missing data | Added checks to skip empty rows |
| Large dataset |	Stored results in CSV for structured analysis |

---


## 📊 Output & Results
- Successfully scraped all FIFA-ranked teams ✅
- Data exported to FIFA_Rankings.csv 📂


---

## Top 5 Teams
| Rank | Team | Points |
|------------|---------|--------|
| 1 |	Argentina |	1841 |
| 2 |	France |	1827 |
| 3 |	Brazil |	1818 | 
| 4 |	Belgium |	1778 |
| 5 |	England |	1769 |

---

## 🚀 Future Improvements
- Schedule automatic scraping for real-time updates
- Visualize rankings using matplotlib or seaborn 📈
- Store historical data in a database for trend analysis
- Extend scraping to include team stats, goals, and player rankings

---

## 🎯 Learning Outcomes
- Hands-on experience with Selenium and BeautifulSoup integration
- Understanding dynamic web content and HTML parsing
- Improved Python, automation, and data handling skills
- Learned to handle real-world web scraping challenges

---


## ✅ Conclusion
This project demonstrates the ability to automate FIFA ranking extraction, producing structured datasets for analysis or reporting.
It showcases skills in Python programming, web scraping, and data management, useful for sports analytics, data science, and research projects.

---

## 🔗 Connect
### 💼 LinkedIn: https://www.linkedin.com/in/abdullah-umar-730a622a8/
### 💼 Portfolio: https://linktr.ee/AbdullahUmar.DataAnalyst
### 📧 Email: umerabdullah048@gmail.com

---


### Task Statement:-
![Preview](https://github.com/Abdullah321Umar/CodeAlpha_Web-Scraping-Project1/blob/main/Project%201.png)


---

### Screenshots / Demos:-
Show what the Code and Output look like.
![Preview](https://github.com/Abdullah321Umar/CodeAlpha_Web-Scraping-Project1/blob/main/Project%201(Code%2BOutput).ipynb)
































