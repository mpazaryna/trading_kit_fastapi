# Trading Kit FastAPI

This project provides a FastAPI wrapper for the trading_kit analysis functions.

## Setup

1. Ensure you have Python 3.9+ and Poetry installed.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/trading_kit_fastapi.git
   cd trading_kit_fastapi
   ```
3. Install dependencies:
   ```
   poetry install
   ```

## Running the Application

To run the FastAPI application:

```
poetry run uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### POST /analyze_stock_trends

Analyze stock trends based on provided historical data.

Request body:
```json
{
  "company_name": "Acme Corp",
  "dates": ["2023-01-01", "2023-01-02", "2023-01-03"],
  "prices": [100.0, 101.5, 99.8],
  "short_window": 10,
  "long_window": 30,
  "precision": 2
}
```

Response:
```json
{
  "company_name": "Acme Corp",
  "short_wma": {"2023-01-01": 100.0, "2023-01-02": 100.75, "2023-01-03": 100.43},
  "long_wma": {"2023-01-01": 100.0, "2023-01-02": 100.75, "2023-01-03": 100.43},
  "signals": {"2023-01-01": 0, "2023-01-02": 1, "2023-01-03": -1},
  "summary": {"0": 1, "1": 1, "-1": 1}
}
```

## Testing

To run tests (once implemented):

```
poetry run pytest
```

## Contributing

Please refer to the CONTRIBUTING.md file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.