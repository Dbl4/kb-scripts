import requests

def is_palindrome(s: str) -> bool:
    return s == s[::-1]


def write_data(filename, data):
    with open(filename, "w") as f:
        f.write(data)

def get_user_data(user_id):
    url = f"https://api.example.com/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None