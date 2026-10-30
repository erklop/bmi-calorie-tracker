# BMI & Calorie Tracker

A BMI calculator and daily calorie tracker you can use two ways: a colorful terminal app or a web app. Both run on the same Python code and share one `calories.json` data file.

## Features

- **BMI calculator** with category (underweight, normal, overweight, obese) and health tips
- **Calorie logging** per meal, with a running total for today
- **Weekly summary** of calories per day
- **Web interface** with a 7-day bar chart and full history (Flask + HTML/CSS/JavaScript)
- **Terminal interface** with colored output (`colorama`)
- Input validation on the API, with clear error messages

## Project structure

```
.
├── app.py                  # Flask app: web page + JSON API
├── bmi_calorie_tracker.py  # Core logic and terminal menu
├── templates/
│   └── index.html          # Web frontend (calls the API with fetch)
├── requirements.txt
└── calories.json           # Created automatically on first save (not tracked in Git)
```

`app.py` imports the functions from `bmi_calorie_tracker.py`, so the web app and the terminal app always behave the same way.

## Getting started

Requires Python 3.8 or newer.

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/bmi-calorie-tracker.git
cd bmi-calorie-tracker

# 2. (Optional) create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
python -m pip install -r requirements.txt
```

### Run the web app

```bash
python app.py
```

Then open <http://localhost:5000> in your browser.

### Run the terminal app

```bash
python bmi_calorie_tracker.py
```

Meals added in one version show up in the other. If the terminal app is already open when you add a meal in the browser, restart the terminal app to see it.

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/bmi` | Body: `{"weight": 70, "height": 1.75}`. Returns BMI, category and tip. Height over 3 is treated as centimeters. |
| `POST` | `/api/calories` | Body: `{"calories": 550}`. Adds a meal for today. |
| `DELETE` | `/api/calories/<date>/<index>` | Removes one meal from a given day. |
| `GET` | `/api/today` | Today's meals, count and total. |
| `GET` | `/api/weekly` | Total calories and meal count for every logged day. |

Invalid input returns HTTP 400 with `{"error": "..."}`.

## Notes

- Data is stored locally in `calories.json`. There are no accounts and nothing is sent anywhere.
- `app.py` runs with `debug=True` for local development. Turn it off before deploying to a public server.

## Possible improvements

- Daily calorie goal and progress bar
- Meal names and categories
- SQLite instead of a JSON file
- Unit tests for the BMI and summary functions
