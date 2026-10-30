import json
import os
from datetime import date
 
from colorama import Fore, Style, init
 
init(autoreset=True)
 
# Absolute path so the terminal app and the web app always share the same file
FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calories.json")
 
 
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}
 
 
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)
 
 
# ------------------ BMI CALCULATOR ------------------
def bmi_info(weight, height):
    """Original BMI logic, returned as values so Flask can use it too."""
    bmi = weight / (height ** 2)
    tip = ""
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
        tip = "Reduce sugary food and walk 30 min/day."
    else:
        category = "Obese"
        tip = "Consult a dietitian for a personalized plan."
    return bmi, category, tip
 
 
def calculate_bmi():
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== 🧍 BMI CALCULATOR ===")
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (meters): "))
    bmi, category, tip = bmi_info(weight, height)
    print(f"\nYour BMI is: {bmi:.2f}")
    color = {"Underweight": Fore.YELLOW, "Normal weight": Fore.GREEN,
             "Overweight": Fore.YELLOW, "Obese": Fore.RED}[category]
    print(f"{color}➡ Category: {category}")
    if tip:
        print(f"{Fore.MAGENTA}💡 Tip: {tip}")
 
 
# ------------------ CALORIE TRACKER ------------------
def add_meal(data, calories):
    """Original add logic, split out so Flask can use it too."""
    today = str(date.today())
    if today not in data:
        data[today] = []
    data[today].append(calories)
    save_data(data)
 
 
def delete_meal(data, day, index):
    data[day].pop(index)
    if not data[day]:
        del data[day]
    save_data(data)
 
 
def add_calories(data):
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== 🍎 ADD CALORIES ===")
    calories = float(input("Enter calories for this meal: "))
    add_meal(data, calories)
    print(f"{Fore.GREEN}👍 Calories added!")
 
 
def today_summary(data):
    today = str(date.today())
    meals = data.get(today, [])
    return today, meals, sum(meals)
 
 
def view_today(data):
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== 📅 TODAY'S SUMMARY ===")
    today, meals, total = today_summary(data)
    if not meals:
        print(f"{Fore.YELLOW}No entries yet!")
        return
    print(f"Meals logged: {len(meals)}")
    print(f"Total calories: {Fore.GREEN}{total} kcal")
 
 
def daily_totals(data):
    return [(day, sum(meals), len(meals)) for day, meals in data.items()]
 
 
def weekly_summary(data):
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== 📊 WEEKLY SUMMARY ===")
    if not data:
        print(f"{Fore.YELLOW}No data available.")
        return
    for day, total, count in daily_totals(data):
        print(f"{Fore.CYAN}{day}{Style.RESET_ALL}: {total} kcal ({count} meals)")
 
 
def main():
    data = load_data()
    while True:
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== 🧮 BMI & CALORIE TRACKER ===")
        print("1️⃣  Calculate BMI")
        print("2️⃣  Add Calories")
        print("3️⃣  View Today’s Calories")
        print("4️⃣  Weekly Summary")
        print("0️⃣  Exit")
        choice = input("\nEnter your choice: ")
        if choice == "1":
            calculate_bmi()
        elif choice == "2":
            add_calories(data)
        elif choice == "3":
            view_today(data)
        elif choice == "4":
            weekly_summary(data)
        elif choice == "0":
            print(f"{Fore.GREEN}👋 Stay healthy! Goodbye!")
            break
        else:
            print(f"{Fore.RED}❌ Invalid input, try again.")
 
 
if __name__ == "__main__":
    main()