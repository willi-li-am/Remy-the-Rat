import requests

def move_robot(time):
    # The URL to which the POST request will be sent
    url = 'http://127.0.0.1:5000/move_remy'

    # The data you want to send in the POST request (as a dictionary)
    data = {
        'time': time
    }

    # Send the POST request and get the response
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 201:
        print('POST request successful!')
        print('Response JSON:', response.json())
    else:
        print(f'Failed to send POST request. Status code: {response.status_code}')