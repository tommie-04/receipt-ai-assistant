from database import init_db, save_transaction, get_user_transactions

# Step 1: Initialize the database (creates the table if it doesn't exist)
init_db()
print("Database initialized.")

# Step 2: Save a fake transaction for testing
save_transaction(
    username="testuser",
    merchant="Test Coffee Shop",
    total="$5.50",
    date="2026-07-16",
    category="food",
    items=[
        {"name": "Latte", "price": "$5.50"}
    ]
)
print("Test transaction saved.")

# Step 3: Retrieve transactions for that user and print them
transactions = get_user_transactions("testuser")
print(f"\nFound {len(transactions)} transaction(s) for 'testuser':")
for t in transactions:
    print(t)