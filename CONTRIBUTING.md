# Contributing to EcoLens

Thank you for considering a contribution!

EcoLens is an open-source learning project that makes public economic data easier to explore and understand.

## Ways to contribute

- Report a bug or suggest an improvement through GitHub Issues.
- Improve explanations of economic indicators.
- Add a country or a carefully documented public data source.
- Improve accessibility, usability, tests, or documentation.
- Review an open issue before starting substantial work.

## Before opening a pull request

1. Open or comment on an issue describing the change.
2. Keep changes focused and explain why they are useful.
3. Use clear names and add comments where they help beginners.
4. Test the application locally.
5. Update the README if setup steps or user-facing features change.

## Run locally

```bash
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data and accuracy

EcoLens currently retrieves indicator observations from the World Bank Indicators API. Please preserve source attribution and explain definitions, units, coverage, and limitations when adding data.

Do not commit private credentials, personal data, or datasets that cannot legally be redistributed.

## Code of conduct

Be respectful, constructive, and welcoming. Assume good faith and focus feedback on the work rather than the person.
