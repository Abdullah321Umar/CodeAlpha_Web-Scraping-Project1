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

b) Setting up Selenium WebDriver
service = Service("path_to_chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)
