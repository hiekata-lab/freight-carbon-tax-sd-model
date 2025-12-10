# SD Modelling of Carbon Tax in Commercial Vehicle Sector

System dynamics model for analyzing the impacts of carbon taxation on Japan's commercial vehicle sector.

## Model Documentation

- **[Equations](docs/equations.md)**
- **[Parameters](docs/parameters.md)**
- **[Validation](docs/validation.md)**
- **[Settings](docs/settings.md)**

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=sd-model --display-name="Python (sd-model)"
pre-commit install

# Or
source setup.sh
```
