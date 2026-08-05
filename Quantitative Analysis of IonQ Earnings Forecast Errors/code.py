"""
Noel Burra
Quantitative Evaluation of Analyst Forecast Accuracy
"""

import pandas as pd
import requests

# API CONNECTION

API_KEY = '1VKFYODASUO8GIZ2'
url = "https://www.alphavantage.co/query"

params = {
    "function": "EARNINGS",
    "symbol": "IONQ",
    "apikey": API_KEY
}

response = requests.get(
    url,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()

earnings_df = pd.DataFrame(data["quarterlyEarnings"])

print(earnings_df)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# DATA PREPARATION

# Convert to numeric
# Invalid replaced with NaN
earnings_df["reportedEPS"] = pd.to_numeric(
    earnings_df["reportedEPS"],
    errors="coerce"
)

earnings_df["estimatedEPS"] = pd.to_numeric(
    earnings_df["estimatedEPS"],
    errors="coerce"
)

# Convert date to datetime
earnings_df["reportedDate"] = pd.to_datetime(
    earnings_df["reportedDate"],
    errors="coerce"
)

# Remove rows missing required values
earnings_df = earnings_df.dropna(
    subset=["reportedEPS", "estimatedEPS", "reportedDate"]
)

# Sort chronologically
earnings_df = (
    earnings_df
    .sort_values("reportedDate")
    .reset_index(drop=True)
)



# FORECAST ERROR METRICS


# Positive error: reported EPS exceeded estimated EPS
# Negative error: reported EPS was below estimated EPS
earnings_df["ForecastError"] = (
    earnings_df["reportedEPS"] - earnings_df["estimatedEPS"]
)

earnings_df["AbsoluteForecastError"] = (
    earnings_df["ForecastError"].abs()
)

earnings_df["Year"] = earnings_df["reportedDate"].dt.year



# OVERALL FORECAST BIAS AND MAE

forecast_bias = earnings_df["ForecastError"].mean()
mae = earnings_df["AbsoluteForecastError"].mean()

print(f"Overall Forecast Bias: {forecast_bias:.4f}")
print(f"Overall Mean Absolute Error: {mae:.4f}")



# PRE-2025 VS. POST-2025 REGIME COMPARISON

pre_2025 = earnings_df[
    earnings_df["reportedDate"] < pd.Timestamp("2025-01-01")
].copy()

post_2025 = earnings_df[
    earnings_df["reportedDate"] >= pd.Timestamp("2025-01-01")
].copy()

pre_2025_mae = pre_2025["AbsoluteForecastError"].mean()
post_2025_mae = post_2025["AbsoluteForecastError"].mean()

pre_2025_volatility = pre_2025["ForecastError"].std()
post_2025_volatility = post_2025["ForecastError"].std()

# Avoid division by zero
mae_increase = (
    post_2025_mae / pre_2025_mae
    if pd.notna(pre_2025_mae) and pre_2025_mae != 0
    else np.nan
)

volatility_increase = (
    post_2025_volatility / pre_2025_volatility
    if pd.notna(pre_2025_volatility) and pre_2025_volatility != 0
    else np.nan
)

print("\nPre-2025 vs. Post-2025 Comparison")
print(f"Pre-2025 MAE: {pre_2025_mae:.4f}")
print(f"Post-2025 MAE: {post_2025_mae:.4f}")
print(f"MAE Ratio (Post / Pre): {mae_increase:.2f}x")

print(f"Pre-2025 Forecast Volatility: {pre_2025_volatility:.4f}")
print(f"Post-2025 Forecast Volatility: {post_2025_volatility:.4f}")
print(f"Volatility Ratio (Post / Pre): {volatility_increase:.2f}x")


# REGIME-SHIFT HYPOTHESIS TEST

# H0: Mean forecast error is the same before and after 2025
# H1: Mean forecast error is different before and after 2025

pre_errors = pre_2025["ForecastError"].dropna()
post_errors = post_2025["ForecastError"].dropna()

if len(pre_errors) >= 2 and len(post_errors) >= 2:
    t_stat, p_value = ttest_ind(
        pre_errors,
        post_errors,
        equal_var=False
    )

    print("\nWelch's Independent-Samples T-Test")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        print(
            "Conclusion: Reject the null hypothesis. "
            "The mean forecast errors are significantly different."
        )
    else:
        print(
            "Conclusion: Fail to reject the null hypothesis. "
            "There is not enough evidence of a difference in mean "
            "forecast errors."
        )
else:
    t_stat = np.nan
    p_value = np.nan
    print(
        "\nThe hypothesis test could not be performed because one "
        "of the periods contains fewer than two observations."
    )


# OUTLIERS

mean_error = earnings_df["ForecastError"].mean()
std_error = earnings_df["ForecastError"].std()

if pd.notna(std_error) and std_error != 0:
    earnings_df["ZScore"] = (
        earnings_df["ForecastError"] - mean_error
    ) / std_error
else:
    earnings_df["ZScore"] = np.nan

# Flag observations more than two standard deviations from the mean
outliers = earnings_df[
    earnings_df["ZScore"].abs() > 2
].copy()

print(f"\nNumber of Outliers: {len(outliers)}")

if not outliers.empty:
    print(
        outliers[
            [
                "reportedDate",
                "reportedEPS",
                "estimatedEPS",
                "ForecastError",
                "ZScore"
            ]
        ].to_string(index=False)
    )



# YEARLY FORECAST ERROR SUMMARY

yearly_summary = (
    earnings_df
    .groupby("Year")
    .agg(
        AvgForecastError=("ForecastError", "mean"),
        AvgAbsoluteForecastError=("AbsoluteForecastError", "mean"),
        ForecastVolatility=("ForecastError", "std"),
        ObservationCount=("ForecastError", "count")
    )
    .reset_index()
)

print("\nYearly Forecast Error Summary")
print(yearly_summary.to_string(index=False))


# FORECAST ERROR TIME-SERIES CHART

plt.figure(figsize=(12, 6))

plt.plot(
    earnings_df["reportedDate"],
    earnings_df["ForecastError"],
    marker="o",
    linewidth=2,
    label="Forecast Error"
)

plt.axhline(
    y=0,
    color="red",
    linestyle="--",
    label="No Forecast Error"
)

plt.axvline(
    x=pd.Timestamp("2025-01-01"),
    color="black",
    linestyle=":",
    label="2025 Regime Split"
)

plt.title("IONQ Analyst Forecast Error Through Time")
plt.xlabel("Report Date")
plt.ylabel("Reported EPS − Estimated EPS")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# FORECAST ERROR HEATMAP

heatmap_data = yearly_summary[
    [
        "Year",
        "AvgForecastError",
        "AvgAbsoluteForecastError",
        "ForecastVolatility"
    ]
].copy()

heatmap_data = heatmap_data.set_index("Year")

plt.figure(figsize=(10, 5))

heatmap = plt.imshow(
    heatmap_data,
    aspect="auto",
    cmap="coolwarm"
)

plt.colorbar(
    heatmap,
    label="Metric Value"
)

plt.xticks(
    ticks=np.arange(len(heatmap_data.columns)),
    labels=[
        "Average Error",
        "Average Absolute Error",
        "Volatility"
    ],
    rotation=25,
    ha="right"
)

plt.yticks(
    ticks=np.arange(len(heatmap_data.index)),
    labels=heatmap_data.index
)

plt.title("IONQ Forecast Error Heatmap by Year")

# Add metric values inside each heatmap cell
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        value = heatmap_data.iloc[i, j]
        label = "N/A" if pd.isna(value) else f"{value:.2f}"

        plt.text(
            j,
            i,
            label,
            ha="center",
            va="center",
            color="black",
            fontsize=9
        )

plt.tight_layout()
plt.show()