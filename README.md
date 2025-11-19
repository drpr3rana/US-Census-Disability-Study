



# To download and clean datasets for Python 

# To run the CPS Disability Prevalence Explorer

An interactive app for exploring weighted disability prevalence across U.S. geographies using the Current Population Survey (CPS) disability supplement** for 2012, 2019, and 2021.

The app lets you:

- Select year (2012, 2019, 2021)
- Choose geography: **state**, **Census region**, or **Census division**
- Choose disability domain (any disability, cognitive, hearing, mobility, vision, self-care, independent living)
- View **weighted prevalence maps** with a tooltip that also shows an approximate **mean family income** per geography.

---

```text
repo-root/
├─ map_app/
│  ├─ app.py
│  ├─ geo_utils.py                  # functions to create geodataframe (for mapping)
│  ├─ CPSdata12w-API.csv             # data for 2012, 2019, 2021 with weights
│  ├─ CPSdata19w-API.csv
│  ├─ CPSdata21w-API.csv             
│  ├─ tl_2021_us_state/              # state shapefile folder (shp + related files)
│  ├─ cb_2018_us_region_5m/          # region shapefile folder
│  ├─ cb_2018_us_division_5m/        # division shapefile folder
|  ├─ cb_2018_us_division_5m/        # division shapefile folder
│  ├─ requirements.txt
│  ├─divst.csv                      #state fips - division mapping data
└─ README.md
```

**1. Clone repo and Navigate to your project folder**

Clone this git repository and open a terminal (macOS/Linux) or Command Prompt/PowerShell (Windows) and change to your project directory:
```
cd path/to/cloned/repo
```

**2. Install dependencies from requirements.txt**

Assuming you’ve created requirements.txt with all needed packages:
```
pip install -r requirements.txt
```

**3. Run App  **
```
python -m streamlit run app.py
```
