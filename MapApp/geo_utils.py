import pandas as pd
import geopandas as gpd

#Used Chatgpt to format, document, and build income aggregation logic

#NON-WEIGHTED - only use for sampling distribution 
def plot_disability_map(
    df,
    geo_group_col="GESTFIPS",              # column in df to group by (e.g., state FIPS)
    shapefile_path="tl_2021_us_state",     # path to the shapefile
    shape_geo_id_col="GEOID",              # ID column in the shapefile to join on
    disability_flag_col="PRDISFLG",        # selected disability flag column
    disability_yes_value=1,                # value indicating "has disability" for the selected flag
    general_dis_flag_col="PRDISFLG",       # general disability indicator column
    general_yes_value=1,                   # value indicating "has any disability"
    count_col_name="n_disabled",           # name for the numerator count
    total_col_name="n_total",              # name for the denominator count
    prev_col_name="prev_disabled",         # name for prevalence column
    include_income=True,                   # whether to compute mean income by geo
    income_col="HEFAMINC",                 # family income code column (1–16)
    income_mean_col_name="mean_income"     # output column name for mean income
):
    """
    Create a choropleth-ready GeoDataFrame of disability prevalence by geography.

    Prevalence logic:

    - If disability_flag_col == general_dis_flag_col (e.g., PRDISFLG):
        prevalence = (# with general disability) / (# with general flag in {1,2})

    - If disability_flag_col != general_dis_flag_col (e.g., PEDISREM, PEDISEAR, ...):
        prevalence = (# with specific disability AND general disability) /
                     (# with general disability)

    Income logic (optional input):

        mean_income = mean of mapped dollar values for HEFAMINC per geo.
        uses midpoints for each category to approximate. 
    """

    # Disability numerator/denominator

    # CASE 1: general disability indicator selected
    if disability_flag_col == general_dis_flag_col:
        # Numerator: # with disability_flag_col == disability_yes_value
        dis_yes = (
            df[df[disability_flag_col] == disability_yes_value]
            .groupby(geo_group_col)
            .size()
            .reset_index(name=count_col_name)
        )

        # Denominator: all with disability_flag_col in {1,2}(yes or no)
        total = (
            df[df[disability_flag_col].isin([1, 2])]
            .groupby(geo_group_col)
            .size()
            .reset_index(name=total_col_name)
        )

    # CASE 2: specific disability type selected
    else:
        # Restrict to people with general disability PRDISFLG == 1
        df_general_yes = df[df[general_dis_flag_col] == general_yes_value]

        # Numerator: among those with general disability, those who also have the specific type
        dis_yes = (
            df_general_yes[df_general_yes[disability_flag_col] == disability_yes_value]
            .groupby(geo_group_col)
            .size()
            .reset_index(name=count_col_name)
        )

        # Denominator: all with general disability (PRDISFLG == 1)
        total = (
            df_general_yes
            .groupby(geo_group_col)
            .size()
            .reset_index(name=total_col_name)
        )

    # Merge numerator + denominator
    dis_group = pd.merge(total, dis_yes, on=geo_group_col, how="left")

    # If some geos have no cases for that disability type, set count to 0 instead of NaN
    dis_group[count_col_name] = dis_group[count_col_name].fillna(0)

    # Prevalence: numerator / denominator
    dis_group[prev_col_name] = dis_group[count_col_name] / dis_group[total_col_name]

    # Income aggregation 

    if include_income and income_col in df.columns:
        # Map HEFAMINC categories to representative dollar values (approximate midpoints).
        # You can tweak these midpoints if you like!
        income_map = {
            1:  2500,     # < 5,000
            2:  6250,     # 5,000–7,499
            3:  8750,     # 7,500–9,999
            4:  11250,    # 10,000–12,499
            5:  13750,    # 12,500–14,999
            6:  17500,    # 15,000–19,999
            7:  22500,    # 20,000–24,999
            8:  27500,    # 25,000–29,999
            9:  32500,    # 30,000–34,999
            10: 37500,    # 35,000–39,999
            11: 45000,    # 40,000–49,999
            12: 55000,    # 50,000–59,999
            13: 67500,    # 60,000–74,999
            14: 87500,    # 75,000–99,999
            15: 125000,   # 100,000–149,999
            16: 175000,   # 150,000 or more (assumed; adjust if desired)
        }

        df_inc = df[[geo_group_col, income_col]].copy()

        # Keep only valid coded values
        df_inc = df_inc[df_inc[income_col].isin(income_map.keys())]

        # Map codes to dollar values
        df_inc["income_value"] = df_inc[income_col].map(income_map)

        # Mean income per geo
        inc_group = (
            df_inc
            .groupby(geo_group_col)["income_value"]
            .mean()
            .reset_index(name=income_mean_col_name)
        )

        # Merge into dis_group
        dis_group = dis_group.merge(inc_group, on=geo_group_col, how="left")

    #Join to shapefile

    gdf = gpd.read_file(shapefile_path)
    gdf2 = gdf[[shape_geo_id_col, "geometry"]].copy()

    # Align types for join
    gdf2[shape_geo_id_col] = gdf2[shape_geo_id_col].astype(str)
    dis_group[geo_group_col] = dis_group[geo_group_col].astype(str)

    merged = pd.merge(
        dis_group,
        gdf2,
        how="left",
        left_on=geo_group_col,
        right_on=shape_geo_id_col
    )

    dgdf = gpd.GeoDataFrame(merged, geometry="geometry", crs=gdf.crs)

    return dgdf

#WEIGHTED 
def plot_disability_mapw(
    df,
    geo_group_col="GESTFIPS",              # column in df to group by (e.g., state FIPS)
    shapefile_path="tl_2021_us_state",     # path to the shapefile
    shape_geo_id_col="GEOID",              # ID column in the shapefile to join on
    disability_flag_col="PRDISFLG",        # selected disability flag column (e.g., PRDISFLG, PEDISREM, ...)
    disability_yes_value=1,                # value indicating "has disability" for the selected flag
    general_dis_flag_col="PRDISFLG",       # general disability indicator column
    general_yes_value=1,                   # value indicating "has any disability"
    count_col_name="n_disabled",           # name for the numerator (weighted) count
    total_col_name="n_total",              # name for the denominator (weighted) count
    prev_col_name="prev_disabled",         # name for prevalence column
    include_income=True,                   # whether to compute mean income by geo
    income_col="HEFAMINC",                 # family income code column (1–16)
    income_mean_col_name="mean_income",    # output column name for mean income
    weight_col="PWCMPWGT",                 # survey weight column
    weight_suffix="_w"                     # suffix used in add_disability_weights (e.g., "_w")
):
    """
    Create a choropleth-ready GeoDataFrame of *weighted* disability prevalence by geography.

    Weighted prevalence logic:

    Let W be the survey weight (PWCMPWGT), and X_w be the weighted indicator column
    created by add_disability_weights: X_w = W if X == 1 else 0.

    - If disability_flag_col == general_dis_flag_col (e.g., PRDISFLG):
        Numerator   = sum over geo of PRDISFLG_w
        Denominator = sum over geo of W for people with PRDISFLG in {1, 2}
        Prevalence  = Numerator / Denominator

    - If disability_flag_col != general_dis_flag_col (e.g., PEDISREM, PEDISEAR, ...):
        Restrict to people with general_dis_flag_col == general_yes_value (e.g., PRDISFLG == 1).

        Numerator   = sum over geo of (specific_disability_w) among general disabled
        Denominator = sum over geo of PRDISFLG_w among general disabled
        Prevalence  = Numerator / Denominator

    Income logic (optional input) is unchanged and currently unweighted:
        mean_income = mean of mapped dollar values for HEFAMINC per geo.
    """

    # Figure out the names of the weighted columns
    disability_weight_col = f"{disability_flag_col}{weight_suffix}"
    general_weight_col = f"{general_dis_flag_col}{weight_suffix}"

    # Basic checks to help debug if weights aren't present
    if disability_weight_col not in df.columns:
        raise ValueError(f"Expected weighted column '{disability_weight_col}' not found in df.")
    if general_weight_col not in df.columns:
        raise ValueError(f"Expected weighted column '{general_weight_col}' not found in df.")
    if weight_col not in df.columns:
        raise ValueError(f"Expected weight column '{weight_col}' not found in df.")

    # Ensure weight column is numeric
    df[weight_col] = pd.to_numeric(df[weight_col], errors="coerce")

    #  Disability numerator/denominator (weighted)

    # CASE 1: general disability indicator selected (e.g., PRDISFLG)
    if disability_flag_col == general_dis_flag_col:
        # Numerator: sum of weighted general disability indicator (PRDISFLG_w) for yes
        df_yes = df[df[disability_flag_col] == disability_yes_value].copy()
        dis_yes = (
            df_yes
            .groupby(geo_group_col)[disability_weight_col]
            .sum()
            .reset_index(name=count_col_name)
        )

        # Denominator: sum of survey weights W for people with PRDISFLG in {1,2}
        df_den = df[df[disability_flag_col].isin([1, 2])].copy()
        df_den["_wtmp"] = df_den[weight_col].fillna(1)  # treat missing weights as 1
        total = (
            df_den
            .groupby(geo_group_col)["_wtmp"]
            .sum()
            .reset_index(name=total_col_name)
        )

    # CASE 2: specific disability type selected (e.g., PEDISREM)
    else:
        # Restrict to people with general disability (PRDISFLG == 1)
        df_general_yes = df[df[general_dis_flag_col] == general_yes_value].copy()

        # Numerator: among those with general disability, sum of specific weighted indicator
        dis_yes = (
            df_general_yes
            .groupby(geo_group_col)[disability_weight_col]
            .sum()
            .reset_index(name=count_col_name)
        )

        # Denominator: among those with general disability, sum of general weighted indicator
        total = (
            df_general_yes
            .groupby(geo_group_col)[general_weight_col]
            .sum()
            .reset_index(name=total_col_name)
        )

    # Merge numerator + denominator
    dis_group = pd.merge(total, dis_yes, on=geo_group_col, how="left")

    #round population totals
    dis_group[total_col_name] =  dis_group[total_col_name].round(decimals=0).astype(int)

    # If some geos have no cases for that disability type, set count to 0 instead of NaN
    dis_group[count_col_name] = dis_group[count_col_name].fillna(0)

    # Prevalence: numerator / denominator
    dis_group[prev_col_name] = dis_group[count_col_name] / dis_group[total_col_name]

    # Income aggregation (unchanged, unweighted for now)

    if include_income and income_col in df.columns:
        income_map = {
            1:  2500,     # < 5,000
            2:  6250,     # 5,000–7,499
            3:  8750,     # 7,500–9,999
            4:  11250,    # 10,000–12,499
            5:  13750,    # 12,500–14,999
            6:  17500,    # 15,000–19,999
            7:  22500,    # 20,000–24,999
            8:  27500,    # 25,000–29,999
            9:  32500,    # 30,000–34,999
            10: 37500,    # 35,000–39,999
            11: 45000,    # 40,000–49,999
            12: 55000,    # 50,000–59,999
            13: 67500,    # 60,000–74,999
            14: 87500,    # 75,000–99,999
            15: 125000,   # 100,000–149,999
            16: 175000,   # 150,000 or more (assumed; adjust if desired)
        }

        df_inc = df[[geo_group_col, income_col]].copy()
        df_inc = df_inc[df_inc[income_col].isin(income_map.keys())]
        df_inc["income_value"] = df_inc[income_col].map(income_map)

        inc_group = (
            df_inc
            .groupby(geo_group_col)["income_value"]
            .mean()
            .reset_index(name=income_mean_col_name)
        )

        dis_group = dis_group.merge(inc_group, on=geo_group_col, how="left")

    # Join to shapefile

    gdf = gpd.read_file(shapefile_path)
    gdf2 = gdf[[shape_geo_id_col, "geometry"]].copy()

    # Align types for join
    gdf2[shape_geo_id_col] = gdf2[shape_geo_id_col].astype(str)
    dis_group[geo_group_col] = dis_group[geo_group_col].astype(str)

    merged = pd.merge(
        dis_group,
        gdf2,
        how="left",
        left_on=geo_group_col,
        right_on=shape_geo_id_col
    )

    dgdf = gpd.GeoDataFrame(merged, geometry="geometry", crs=gdf.crs)

    return dgdf