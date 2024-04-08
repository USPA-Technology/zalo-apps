from arango import ArangoClient
from app.core.config import (ARANGODB_USERNAME, ARANGODB_PASSWORD)
# Initialize the ArangoDB client.
client = ArangoClient()

# Connect to "_system" database as root user.
# This returns an API wrapper for "_system" database.
sys_db = client.db('cdp', username=ARANGODB_USERNAME, password=ARANGODB_PASSWORD)

# Get the API wrapper for "students" collection.
db_profile = sys_db.collection('profile_zalo')

