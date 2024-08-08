import requests

def get_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    res = requests.get(url)
    
    if res.status_code == 200:
        data = res.json()

        if 'main' in data and 'weather' in data and 'wind' in data:
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            description = data['weather'][0]['description']
            temp = data['main']['temp']

            return description
        else:
            return ("Error: Unexpected response structure:", data)
    else:
        return ("Error: Unable to fetch data, HTTP Status code:", res.status_code)

# Replace 'your_api_key' with your actual API key
api_key = "584dda13b490011db77924b4e8efc730"
city = "Kumamoto"

print(get_weather(city, api_key))
