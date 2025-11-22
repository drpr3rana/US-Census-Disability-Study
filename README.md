

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

## Data Sources

### IPUMS CPS (Integrated Public Use Microdata Series)
We used [IPUMS CPS](https://cps.ipums.org/) to access harmonized microdata from the CPS Disability Supplement (July 2021).

IPUMS provides free, harmonized census and survey data with consistent variable coding across time, making longitudinal and cross-sectional analysis more tractable.

### Census Bureau API
We also pulled basic monthly CPS data directly via the Census Bureau API using the `cpsR` package.

---

## Data Extraction Process

### Step 1: Create an IPUMS Account
1. Register at [cps.ipums.org](https://cps.ipums.org/)
2. Request access to CPS microdata

### Step 2: Select Variables and Samples
1. Navigate to "Select Data"
2. Choose your sample(s): We selected the **July 2021 CPS Disability Supplement**
3. Add variables to your cart:
   - Demographics: `AGE`, `SEX`, `RACE`, `HISPAN`, `EDUC`
   - Employment: `EMPSTAT`, `LABFORCE`
   - Disability: `DIFFREM`, `DIFFPHYS`, `DIFFMOB`, `DIFFCARE`, `DIFFEYE`, `DIFFHEAR`
   - Barriers: `DIEMPBAR1` through `DIEMPBAR9`, `DIEMPBARR`
   - Weights: `DISUPPWT`

### Step 3: Submit and Download Extract
1. Submit your data extract request
2. Once processed, download TWO files:
   - **DDI/XML file** (`.xml`): Contains metadata, variable descriptions, and value labels
   - **Data file** (`.dat.gz` or `.csv.gz`): Contains the actual microdata

### Step 4: Load Data in R Using `ipumsr`
```r
# Install ipumsr if needed
install.packages("ipumsr")
library(ipumsr)

# Read the data using the DDI/XML file
# The XML file tells R how to parse the data file
cps_data <- read_ipums_micro("/path/to/your/cps_00001.xml")

# The DDI file contains:
# - Variable names and labels
# - Value labels (what codes 1, 2, 3 etc. mean)
# - Universe information (who was asked each question)
# - Sample design information

# View variable information
ipums_var_info(cps_data)

# Check value labels for a specific variable
ipums_val_labels(cps_data$EMPSTAT)
```

### Why the DDI/XML File Matters
The DDI (Data Documentation Initiative) XML file is essential because:
- It maps numeric codes to meaningful labels (e.g., `1 = "Yes"`, `2 = "No"`)
- It documents which respondents were asked each question (universe)
- It preserves variable descriptions and survey methodology notes
- It enables `ipumsr` to automatically apply labels and handle missing values

Without the DDI file, we'd just have unlabeled numeric codes with no documentation.

---

## Project Structure
```
├── data/
│   ├── cps_00002.xml          # IPUMS DDI metadata file
│   └── cps_00002.dat.gz       # IPUMS microdata (not tracked in git)
├── scripts/
│   ├── 01_data_wrangling.R    # Data cleaning and transformation
│   ├── 02_analysis.R          # Statistical analysis
│   └── 03_visualizations.R    # Charts and figures
├── app/
│   └── app.R                  # R Shiny dashboard
├── outputs/
│   ├── viz1_barriers_lollipop.png
│   ├── viz2_education_gradient.png
│   └── results_*.csv
└── README.md
```

---

## Key R Packages Used

| Package | Purpose |
|---------|---------|
| `ipumsr` | Read IPUMS microdata with DDI metadata |
| `cpsR` | Extract CPS data via Census API |
| `tidyverse` | Data wrangling and visualization |
| `survey` / `srvyr` | Survey-weighted analysis |
| `shiny` | Interactive dashboard |
| `plotly` | Interactive visualizations |

---

## Data Wrangling Highlights

### Challenge 1: Education Recoding
Condensed 44 education codes into 8 ordered categories for interpretable analysis.

### Challenge 2: Barrier Variables
Handled complex skip patterns where barrier questions were only asked of non-employed respondents with disabilities.

### Challenge 3: Survey Weights
Applied `DISUPPWT` weights throughout to produce population-representative estimates.

---

## Reproducing This Analysis

1. Clone this repository
2. Create an IPUMS account and request the same extract (or use our variable list)
3. Download your DDI/XML file and data file to `data/`
4. Set your Census API key: `Sys.setenv(CENSUS_API_KEY = "your_key_here")`
5. Run scripts in order: `01_data_wrangling.R` → `02_analysis.R` → `03_visualizations.R`

---

## Data Citation

Sarah Flood, Miriam King, Renae Rodgers, Steven Ruggles, J. Robert Warren, Daniel Backman, Annie Chen, Grace Cooper, Stephanie Richards, Megan Schouweiler, and Michael Westberry. IPUMS CPS: Version 12.0 [dataset]. Minneapolis, MN: IPUMS, 2024. https://doi.org/10.18128/D030.V12.0

