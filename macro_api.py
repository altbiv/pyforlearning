from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

API_KEY = 'your_nutritionix_api_key'
APP_ID = 'your_nutritionix_app_id'

# Validate API keys
def validate_api_keys(api_key, app_id):
    if not api_key or not app_id:
        return {"error": "API Key or App ID is missing!"}, 400

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'x-app-id': app_id,
        'x-app-key': api_key,
        'Content-Type': 'application/json'
    }
    test_data = {
        "query": "apple",
        "timezone": "US/Eastern"
    }
    
    response = requests.post(url, headers=headers, json=test_data)
    
    if response.status_code == 200:
        return True, 200
    else:
        return {"error": "Invalid API Key or App ID!"}, response.status_code

# Fetch macros for a specific food
def get_food_macros(food_name):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'x-app-id': APP_ID,
        'x-app-key': API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "query": food_name,
        "timezone": "US/Eastern"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        food_data = response.json()
        result = []
        for food in food_data['foods']:
            calories = food['nf_calories']
            protein = food['nf_protein']
            carbs = food['nf_total_carbohydrate']
            fat = food['nf_total_fat']
            
            # Generate a Google search link for the food
            google_link = f"https://www.google.com/search?q={food_name.replace(' ', '+')}"
            
            # Health analysis
            health = health_analysis(calories, protein, carbs, fat)

            result.append({
                "food_name": food_name,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fat": fat,
                "google_search_link": google_link,
                "health_analysis": health
            })
        
        return jsonify(result), 200
    else:
        return {"error": "Food not found or API request failed."}, response.status_code

# Perform a health analysis
def health_analysis(calories, protein, carbs, fat):
    analysis = []
    
    if calories < 150:
        analysis.append("Low in calories.")
    elif 150 <= calories <= 500:
        analysis.append("Moderate calorie content.")
    else:
        analysis.append("High in calories.")
        
    if protein > 15:
        analysis.append("High in protein, great for muscle-building.")
    elif protein < 5:
        analysis.append("Low in protein.")
        
    if carbs < 20:
        analysis.append("Low in carbs, suitable for low-carb diets.")
    elif carbs > 50:
        analysis.append("High in carbs, be mindful if on a low-carb diet.")
        
    if fat < 5:
        analysis.append("Low in fat.")
    elif fat > 20:
        analysis.append("High in fat, should be eaten in moderation.")
        
    return analysis

# Define the Flask API routes
@app.route('/')
def index():
    return "Welcome to the Macro Calculator API!"

@app.route('/validate', methods=['GET'])
def validate():
    result, status = validate_api_keys(API_KEY, APP_ID)
    return result, status

@app.route('/macros', methods=['GET'])
def macros():
    food_name = request.args.get('food_name')
    if not food_name:
        return {"error": "Please provide a valid food name!"}, 400
    
    result, status = get_food_macros(food_name)
    return result, status

if __name__ == '__main__':
    app.run(debug=True)
