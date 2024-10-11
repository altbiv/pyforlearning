import time
import requests

API_KEY = 'api key'
APP_ID = 'app id'

def validate_api_keys(api_key, app_id):
    if not api_key or not app_id:
        print("Error: API Key or App ID is missing!")
        return False

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
        return True
    else:
        print(f"Error: Invalid API Key or App ID! Status code: {response.status_code}")
        return False

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
        for food in food_data['foods']:
            calories = food['nf_calories']
            protein = food['nf_protein']
            carbs = food['nf_total_carbohydrate']
            fat = food['nf_total_fat']
            
            print(f"\nMacros for {food_name}:")
            print(f"Calories: {calories}")
            print(f"Protein: {protein}g")
            print(f"Carbs: {carbs}g")
            print(f"Fat: {fat}g")
            
            # Generate a Google search link for the food
            google_link = f"https://www.google.com/search?q={food_name.replace(' ', '+')}"
            print(f"\nSearch more about {food_name}: {google_link}")

            # Analyze if it's healthy
            health_analysis(calories, protein, carbs, fat)
    else:
        print("Food not found or API request failed.")

def health_analysis(calories, protein, carbs, fat):
    print("\nHealth Analysis:")
    
    if calories < 150:
        print("- This is low in calories.")
    elif 150 <= calories <= 500:
        print("- This has a moderate calorie content.")
    else:
        print("- This is high in calories.")

    if protein > 15:
        print("- High in protein, great for muscle-building.")
    elif protein < 5:
        print("- Low in protein.")
    
    if carbs < 20:
        print("- Low in carbs, suitable for low-carb diets.")
    elif carbs > 50:
        print("- High in carbs, be mindful if on a low-carb diet.")
    
    if fat < 5:
        print("- Low in fat.")
    elif fat > 20:
        print("- High in fat, should be eaten in moderation.")

def main():
    print("Welcome to the Macro Calculator!")

    # Check if API credentials are available and valid
    if validate_api_keys(API_KEY, APP_ID):
        time.sleep(1)  
        print("Booting Complete")

        while True:
            food_name = input("\nEnter the food you've eaten: ")
            get_food_macros(food_name)

            cont = input("\nDo you want to enter another food item? (Y/N): ").strip().lower()
            if cont != 'y':
                print("Goodbye!")
                break
    else:
        print("Please provide valid API credentials.")

if __name__ == "__main__":
    main()
