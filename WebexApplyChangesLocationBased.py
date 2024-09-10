import requests

# Replace with your Webex API token
API_TOKEN = 'REDACTED'
LOCATION_NAME = '233 Main'

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# Get location ID by name
def get_location_id(location_name):
    url = 'https://webexapis.com/v1/locations'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    locations = response.json()['items']
    for location in locations:
        if location['name'].lower() == location_name.lower():
            print(f'Found location: {location_name} with ID: {location["id"]}')
            return location['id']
    print(f'Location "{location_name}" not found.')
    return None

# Get devices matching the location
def get_devices(location_id):
    url = 'https://webexapis.com/v1/devices'
    params = {'max': 500}  # Adjust 'max' as needed
    devices = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        devices.extend(data['items'])
        url = data.get('nextPage', None)  # Handle pagination
        params = {}  # Clear params for subsequent requests
    print(f'Found {len(devices)} devices in total.')
    # Filter devices by location ID
    filtered_devices = [device for device in devices if device.get('locationId', '') == location_id]
    print(f'Filtered devices count: {len(filtered_devices)}')
    return filtered_devices

# Apply changes to a device
def apply_changes(device_id):
    url = f'https://webexapis.com/v1/devices/{device_id}/actions/applyChanges'
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Main function
def main():
    location_id = get_location_id(LOCATION_NAME)
    if not location_id:
        print(f'Location "{LOCATION_NAME}" not found.')
        return
    devices = get_devices(location_id)
    if not devices:
        print(f'No devices found for location "{LOCATION_NAME}".')
        return
    for device in devices:
        device_id = device['id']
        # Apply changes to the device
        apply_changes(device_id)
        print(f'Changes applied to device {device_id}')

if __name__ == '__main__':
    main()
