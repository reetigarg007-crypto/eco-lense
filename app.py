from __future__ import annotations

import requests
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="EcoLens | Economics, made clearer",
    page_icon="📊",
    layout="wide",
)

WORLD_BANK_API = "https://api.worldbank.org/v2"

INDICATORS = {
    "Inflation (consumer prices, annual %)": {
        "code": "FP.CPI.TOTL.ZG",
        "description": "The annual percentage change in the consumer price index. It is a commonly used measure of changes in the general price level.",
        "format": ".2f",
        "color_title": "Annual inflation (%)",
    },
    "GDP growth (annual %)": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "description": "The annual percentage growth rate of GDP at market prices, based on constant local currency.",
        "format": ".2f",
        "color_title": "GDP growth (%)",
    },
    "Unemployment (total, % of labour force)": {
        "code": "SL.UEM.TOTL.ZS",
        "description": "The share of the labour force that is without work but available for and seeking employment, based on ILO modelled estimates.",
        "format": ".2f",
        "color_title": "Unemployment (%)",
    },
}

COUNTRIES = {
    "India": "IND",
    "United States": "USA",
    "United Kingdom": "GBR",
    "China": "CHN",
    "Japan": "JPN",
    "Germany": "DEU",
    "France": "FRA",
    "Brazil": "BRA",
    "South Africa": "ZAF",
    "Indonesia": "IDN",
    "Australia": "AUS",
    "Canada": "CAN",
    "Bangladesh": "BGD",
    "Pakistan": "PAK",
    "Sri Lanka": "LKA",
    "Nepal": "NPL",
    "Mexico": "MEX",
    "Nigeria": "NGA",
    "Singapore": "SGP",
    "South Korea": "KOR",
}


@st.cache_data(ttl=60 * 60)
def load_indicator(country_code: str, indicator_code: str) -> pd.DataFrame:
    """Fetch annual indicator observations from the World Bank API."""
    url = (
        f"{WORLD_BANK_API}/country/{country_code}/indicator/{indicator_code}"
        "?format=json&per_page=100"
    )
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
        return pd.DataFrame(columns=["year", "value"])

    rows = [
        {"year": int(item["date"]), "value": item["value"]}
        for item in payload[1]
        if item.get("value") is not None and str(item.get("date", "")).isdigit()
    ]
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    return frame.sort_values("year").reset_index(drop=True)


st.title("📊 EcoLens")
st.subheader("Explore economic indicators. Understand the bigger picture.")
st.write(
    "A beginner-friendly, open-source economics research toolkit using "
    "publicly available data."
)

with st.sidebar:
    st.header("Explore the data")
    country = st.selectbox("Choose a country", list(COUNTRIES.keys()), index=0)
    indicator_name = st.selectbox("Choose an indicator", list(INDICATORS.keys()))
    year_range = st.slider("Select year range", min_value=2000, max_value=2025, value=(2010, 2025))
    st.caption("Data source: World Bank World Development Indicators.")

indicator = INDICATORS[indicator_name]

st.markdown(f"### {country}: {indicator_name}")
st.write(indicator["description"])

try:
    data = load_indicator(COUNTRIES[country], indicator["code"])
    if data.empty:
        st.warning("No observations were returned for this selection. Try another indicator or country.")
    else:
        selected = data[data["year"].between(year_range[0], year_range[1])].copy()
        selected = selected.sort_values("year")

        if selected.empty:
            st.info("There is no data in the selected year range.")
        else:
            latest = selected.dropna(subset=["value"]).tail(1)
            first = selected.dropna(subset=["value"]).head(1)

            col1, col2, col3 = st.columns(3)
            if not latest.empty:
                latest_row = latest.iloc[0]
                col1.metric(
                    "Latest available value",
                    f'{latest_row["value"]:.2f}%',
                    help=f'Observation year: {int(latest_row["year"])}',
                )
                col2.metric("Latest observation year", int(latest_row["year"]))
            else:
                col1.metric("Latest available value", "Not available")
                col2.metric("Latest observation year", "—")

            col3.metric("Observations in range", len(selected))

            fig = px.line(
                selected,
                x="year",
                y="value",
                markers=True,
                title=f"{indicator_name} in {country}",
                labels={"year": "Year", "value": indicator["color_title"]},
                hover_data={"year": True, "value": ":.2f"},
            )
            fig.update_layout(
                hovermode="x unified",
                margin=dict(l=10, r=10, t=55, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("View the data table"):
                display_data = selected.rename(
                    columns={"year": "Year", "value": indicator["color_title"]}
                )
                st.dataframe(display_data, use_container_width=True, hide_index=True)
                csv = display_data.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download data as CSV",
                    data=csv,
                    file_name=f"ecolens_{COUNTRIES[country]}_{indicator['code']}.csv",
                    mime="text/csv",
                )

            st.caption(
                "Note: World Bank indicators can be revised and may have a publication lag. "
                "The latest available observation is not necessarily for the current year."
            )

except requests.RequestException as exc:
    st.error("EcoLens could not reach the World Bank data service. Please try again later.")
    st.caption(f"Technical detail: {exc}")
except (ValueError, KeyError, TypeError) as exc:
    st.error("The returned data could not be processed. Please try another selection.")
    st.caption(f"Technical detail: {exc}")

st.divider()
st.markdown("**About this project**")
st.write(
    "EcoLens is an open-source learning project. It is designed to make public economic "
    "indicators easier to explore; it is not a forecasting tool and does not provide "
    "investment or policy advice."
)
st.markdown(
    "[World Bank Data](https://data.worldbank.org/) · "
    "[World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392)"
)
