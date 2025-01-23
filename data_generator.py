import pandas as pd
import random
from datetime import datetime
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker()
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:6432/analytics_db")

# generate customers data
def generate_customers(n):
    customers = []
    print(f"generating customers...")
    for i in range(n):
        customers.append({
            "customer_id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "city": random.choice(["Jakarta", "Bogor", "Depok", "Tangerang", "Bekasi"]),
            "age": random.randint(18, 70),
            "gender": random.choice(["Male", "Female"]),
        })
    return pd.DataFrame(customers)

# generate product data
def generate_product(n):
    product = []
    print(f"generating product...")
    for i in range(n):
        category = random.choice(["food", "beverage", "fruit"])
        sub_category = random.choice([f"{category} lite", f"{category} medium", f"{category} super"])
        product.append({
            "product_id": i + 1,
            "name": f"item_{i}",
            "category": category,
            "subcategory": sub_category,
            "price": random.randint(50000, 1000000),
        })
    return pd.DataFrame(product)

# generate inventory data
def generate_inventory(n):
    inventory = []
    print(f"generating inventory...")
    for i in range(n):
        inventory.append({
            "product_id": i + 1,
            "stock": random.randint(1, 2000)
        })
    return pd.DataFrame(inventory)

# generate transaction data
def generate_transaction(n):
    transaction = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 1, 23)
    print(f"generating transaction...")
    for i in range(n):
        random_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
        product_id = random.randint(1, 1000)
        product_price = product.loc[product["product_id"] == product_id, "price"].values.item()
        quantity = random.randint(1,10)
        transaction.append({
            "order_id": i + 1,
            "product_id": product_id,
            "customer_id": random.randint(1, 1000),
            "order_date": random_date,
            "revenue": quantity * product_price,
            "quantity": quantity,
        })
    return pd.DataFrame(transaction)

def create_schema(engine):
    print("creating db schema...")
    schema = ["staging", "warehouse"]
    
    for s in schema:
        with engine.connect() as connection:
            query = text(f"create schema if not exists {s};")
            connection.execute(query)
            connection.commit()

def data_modelling(engine):
    print('creating fact n dimension tables...')
    with open("query/dwh_table_creation.sql", "r") as file:
        query = file.read()
        query = text(query)
    
    with engine.connect() as connection:
        connection.execute(query)
        connection.commit()


# Create schema
create_schema(engine)

# Generate data
customers = generate_customers(1000)
customers.to_sql('customer', engine, if_exists='replace', index=False, schema='staging')

product = generate_product(1000)
product.to_csv("product.csv", index=False)

inventory = generate_inventory(1000)
inventory.to_csv("inventory.csv", index=False)

transaction = generate_transaction(1000000)
transaction.to_sql('transaction', engine, if_exists='replace', index=False, schema='staging', chunksize=100000)

# Build Datawarehouse
data_modelling(engine)

