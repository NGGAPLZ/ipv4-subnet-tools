# Preparation notes

Kept the manual calculator and the improved planner. Corrected whole-octet block reporting; rejected non-ASCII numeric input. Added direct-function validation, exact integer prefix calculation, explicit IPv4 bounds and a 100,000-row limit. Avoided constructing a nonexistent next subnet after the final row. Added overwrite confirmation and deferred pandas import to export time. Renamed requirements.txt.txt.

Original source locations:

- `3.zip/projects_for_github/portfolio_ready/ip_cidr_calculator/ip_cidr_calculator.py` → `ip_cidr_calculator.py`
- `1.zip/subbnet_app.py` → `ip_cidr_calculator.py`
- `3.zip/projects_for_github/portfolio_ready/subnet_excel_generator/subnet_excel_generator.py` → `subnet_excel_generator.py`
- `3.zip/ip_subnet_calc/ip_calculator.py` → `subnet_excel_generator.py`
- `3.zip/projects_for_github/portfolio_ready/subnet_excel_generator/requirements.txt.txt` → `requirements.txt`

Added README, ignore rules, line-ending rules, and regression tests. No license or authorship claims were invented.
