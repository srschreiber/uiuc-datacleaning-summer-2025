# @BEGIN data_cleaning_workflow
# @IN NYPL_Menu_Data
# @OUT cleaned_NYPL_Menu_Data

# @BEGIN load_and_prepare_data
# @IN raw_data
# @OUT df
# @DESC Load raw dataset and prepare for processing (e.g., convert curencies to ISO codes, parse dates, select columns)
# @END load_and_prepare_data

# @BEGIN convert_to_usd
# @IN df
# @OUT df_usd_converted
# @DESC Convert prices from source currencies to USD using historical FX rates via forex-python
# @END convert_to_usd

# @BEGIN adjust_for_inflation
# @IN df_usd_converted
# @OUT df_inflation_adjusted
# @DESC Adjust USD prices for inflation to a target year using the CPI library
# @PARAM target_year
# @END adjust_for_inflation

# @BEGIN finalize_clean_data
# @IN df_inflation_adjusted
# @OUT cleaned_data
# @DESC Final cleanup, drop missing data, reorder columns, and prepare for export/analysis
# @END finalize_clean_data

# @END data_cleaning_workflow