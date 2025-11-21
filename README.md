

# To download and clean datasets for Python 

(All relevant datasets have been pulled and included in the PythonAnalysis directory)

Run the notebook "DWprevtesting.ipynb"  and generate datasets as desired, from the PythonAnalysis folder

# To conduct paired (by states) t-testing 

(All relevant datasets have been pulled and included in the PythonAnalysis directory)

Run the notebook "DWcpsDataRetrieval.ipynb" in PythonAnalysis folder

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
│  ├─ CPSdata12w-API.csv             # data for 2012, 2019, 2021 with or without weights (indicating by "w" after year)
│  ├─ CPSdata19w-API.csv
│  ├─ CPSdata21w-API.csv
|  ├─ ....    
│  ├─ tl_2021_us_state/              # state shapefile folder (shp + related files)
│  ├─ cb_2018_us_region_5m/          # region shapefile folder
│  ├─ cb_2018_us_division_5m/        # division shapefile folder
|  ├─ cb_2018_us_division_5m/        # division shapefile folder
│  ├─ requirements.txt
│  ├─divst.csv                      #state fips - division mapping data
└─ README.md
```

**1. Clone repo and Navigate to your project folder**

Clone this git repository and open a terminal (macOS/Linux) or Command Prompt/PowerShell (Windows) and change to the MapApp project directory:
```
cd path/to/cloned/repo
```

**2. Install dependencies from requirements.txt**

Assuming you’ve created requirements.txt with all needed packages:
```
pip install -r requirements.txt
```

**3. Run App**
```
python -m streamlit run app.py
```

# To download datasets for R
1. Request a U.S. Census API key if needed: https://api.census.gov/data/key_signup.html
2. Supply the API key at line 43 of the R Markdown "Data Wrangling Final Project.Rmd"

# Running "Data Wrangling Final Project.Rmd"
Run the R Markdown "Data Wrangling Final Project.Rmd".

**This file contains code that:**
- Extracts data from the U.S. Census Bureau Current Population Survey for May 2012, July 2019, and July 2021.
- Cleans the datasets and recodes the variables accordingly.
- Creates a table one displaying labor-force participation in individuals with disabilities by disability status, disability type, household family income, and education for May 2012, July 2019, July 2021.
- Plots labor-force participation in individuals with disabilities by disability status, disability type, household family income, and education for May 2012, July 2019, July 2021.
- Fits 4 logistic regression models to predict individual disability status across the years while adjusting for household family income, education, race, sex, age, and region for May 2012, July 2019, July 2021.
- Creates a forest plot to display odds ratios for each predictor variable included in the regression model.
