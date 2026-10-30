from flask import Flask, jsonify, render_template, request
 
import bmi_calorie_tracker
 
app = Flask(__name__)
 
 
def number(payload, key, allow_zero=False):
    try:
        value = float(payload[key])
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"Please enter a valid number for {key}.")
    if value < 0 or (value == 0 and not allow_zero):
        raise ValueError(f"{key.capitalize()} must be a positive number.")
    return value
 
 
@app.errorhandler(ValueError)
def bad_request(e):
    return jsonify(error=str(e)), 400
 
 
def today_json(data):
    today, meals, total = bmi_calorie_tracker.today_summary(data)
    return {"date": today, "meals": meals, "count": len(meals), "total": total}
 
 
@app.get("/")
def index():
    return render_template("index.html")
 
 
@app.post("/api/bmi")
def api_bmi():
    p = request.get_json(silent=True) or {}
    weight, height = number(p, "weight"), number(p, "height")
    if height > 3:  # allow centimeters
        height /= 100
    bmi, category, tip = bmi_calorie_tracker.bmi_info(weight, height)
    return jsonify(bmi=round(bmi, 2), category=category, tip=tip)
 
 
@app.post("/api/calories")
def api_add():
    p = request.get_json(silent=True) or {}
    data = bmi_calorie_tracker.load_data()
    bmi_calorie_tracker.add_meal(data, number(p, "calories", allow_zero=True))
    return jsonify(today_json(data)), 201
 
 
@app.delete("/api/calories/<day>/<int:index>")
def api_delete(day, index):
    data = bmi_calorie_tracker.load_data()
    try:
        bmi_calorie_tracker.delete_meal(data, day, index)
    except (KeyError, IndexError):
        raise ValueError("Entry not found.")
    return jsonify(today_json(data))
 
 
@app.get("/api/today")
def api_today():
    return jsonify(today_json(bmi_calorie_tracker.load_data()))
 
 
@app.get("/api/weekly")
def api_weekly():
    rows = sorted(bmi_calorie_tracker.daily_totals(bmi_calorie_tracker.load_data()))
    return jsonify([{"date": d, "total": t, "count": c} for d, t, c in rows])
 
 
if __name__ == "__main__":
    app.run(debug=True)