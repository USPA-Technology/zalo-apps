from core.db import sys_db


# Get the API wrapper for "students" collection
profile_collection = sys_db.collection('profile')

# Insert a new document. This return the document metadata

