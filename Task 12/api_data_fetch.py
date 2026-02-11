import requests
import json

# API Configuration

API_URL = "https://randomuser.me/api/"

# Function to Fetch Data from API

def fetch_user_data():
    try:
        response = requests.get(API_URL, timeout=10)

        # 4. Inspect response status code
        if response.status_code == 200:
            print("✅ API Request Successful\n")
            return response.json()
        else:
            print(f"❌ API Error: Status Code {response.status_code}")
            return None

    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check internet.")
    except requests.exceptions.RequestException as e:
        print("❌ Unexpected API error:", e)

    return None


# Function to Extract Required Fields

def extract_user_details(data):
    try:
        user = data["results"][0]

        name = f"{user['name']['title']} {user['name']['first']} {user['name']['last']}"
        email = user["email"]
        country = user["location"]["country"]
        phone = user["phone"]

        return {
            "Name": name,
            "Email": email,
            "Country": country,
            "Phone": phone
        }

    except (KeyError, IndexError):
        print("❌ Error parsing API response.")
        return None

# Function to Save JSON to Local File

def save_to_file(data):
    with open("api_response.json", "w") as file:
        json.dump(data, file, indent=4)
    print(" Full API response saved to api_response.json")


# Main Program

def main():
    print("=== API Data Fetch Program ===\n")

    data = fetch_user_data()

    if data:
        user_details = extract_user_details(data)

        if user_details:
            print("📌 User Details:\n")
            for key, value in user_details.items():
                print(f"{key:<10}: {value}")

        save_to_file(data)


if __name__ == "__main__":
    main()
