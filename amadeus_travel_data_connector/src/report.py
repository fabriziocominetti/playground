# Summary report for travel packages
import pandas as pd
import logging

def generate_summary_report(merged_df):
	"""
	Generate a summary report from the merged DataFrame.
	:param merged_df: Cleaned DataFrame with package data
	:return: Summary DataFrame
	"""
	if merged_df.empty:
		logging.warning("No data available for summary report.")
		return pd.DataFrame()

	summary = {
		'average_package_price': merged_df['package_price'].mean(),
		'min_package_price': merged_df['package_price'].min(),
		'max_package_price': merged_df['package_price'].max(),
		'total_packages': len(merged_df),
		'unique_flights': merged_df['flight_price'].nunique(),
		'unique_hotels': merged_df['hotel_name'].nunique() if 'hotel_name' in merged_df.columns else None,
		'available_dates': merged_df['departure_date'].nunique() if 'departure_date' in merged_df.columns else None
	}
	logging.info(f"Summary report generated: {summary}")
	return pd.DataFrame([summary])
