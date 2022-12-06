# Replace with your TooGoodToGo API key
from tgtg import TgtgClient

API_KEY = "your-api-key"

# Replace with the store name or ID you want to check
STORE_NAME = "store-name"

# Create a TooGoodToGo client using your API key

client = TgtgClient(email="<your_email>")
credentials = client.get_credentials()

# Get the list of stores from the API
stores = client.get_partners()

# Find the store with the given name or ID
store = None
for s in stores:
    if s.name == STORE_NAME or s.id == STORE_NAME:
        store = s
        break

# Check if the store was found
if store is None:
    print(f"Error: store with name or ID '{STORE_NAME}' not found.")
    exit(1)

# Get the availability of magic bags at the store
magic_bag_data = client.get_magic_bag(store.id)

# Check if magic bags are available
if magic_bag_data.available:
    print("Magic bags are available at the store.")
else:
    print("Magic bags are not available at the store.")