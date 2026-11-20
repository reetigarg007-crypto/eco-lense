# EcoLens

**An open-source toolkit for exploring, visualising and understanding economic data.**

EcoLens aims to make public economic data easier to access, understand, compare and use for research.

## Current status

The first working module is an interactive dashboard for exploring annual macroeconomic indicators for selected countries:

- Consumer price inflation (annual %)
- GDP growth (annual %)
- Unemployment (total, % of labour force)

The dashboard currently supports country and indicator selection, a year-range filter, interactive time-series charts, a data table, and CSV export.

## Run EcoLens locally

### 1. Requirements

- Python 3.10 or newer
- An internet connection (the dashboard retrieves data from the World Bank API)

### 2. Download the project

Clone this repository:

```bash
git clone https://github.com/reetigarg007-crypto/eco-lense.git
cd eco-lense
```

### 3. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Streamlit will provide a local address to open in your browser.

## Data source and methodology

The first module retrieves indicator observations from the **World Bank Indicators API (V2)**. It uses the following indicator series:

| Indicator | World Bank code |
|---|---|
| Inflation, consumer prices (annual %) | `FP.CPI.TOTL.ZG` |
| GDP growth (annual %) | `NY.GDP.MKTP.KD.ZG` |
| Unemployment, total (% of total labour force) (modelled ILO estimate) | `SL.UEM.TOTL.ZS` |

The dashboard displays the annual values returned by the API. Missing observations are not imputed. The latest available observation may not be for the current year because economic data can be published with a lag and revised.

- [World Bank Indicators API documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)
- [World Bank API basic call structures](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)
- [World Bank Open Data](https://data.worldbank.org/)

## Roadmap

Planned directions (not yet implemented):

- Country-to-country indicator comparisons
- A dedicated inflation and purchasing-power explainer
- GDP and labour-market analysis views
- More transparent indicator metadata, definitions and source notes
- An economic research library with carefully sourced reading material
- Automated tests and continuous integration

Features will be marked as complete only after they are implemented and tested.

## Contributing

Contributions, issue reports and suggestions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Project principles

- **Source transparency:** economic values should come from identifiable, documented sources.
- **No fabricated data:** examples and visualisations must not present invented values as real observations.
- **Clear interpretation:** explain indicators, units, coverage and limitations.
- **Accessible research:** make the tools approachable to students, educators and independent researchers.

## Disclaimer

EcoLens is an open-source learning and research-support project. It is not a forecasting tool and does not provide investment or policy advice.

## Licence

This project is licensed under the MIT Licence. See [LICENSE](LICENSE).
