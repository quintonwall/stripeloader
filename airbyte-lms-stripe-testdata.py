import stripe
import random
from google.colab import userdata


stripe.api_key = userdata.get('STRIPE_TEST_KEY')


# Sample data for generating random names
first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack", "Quinton", "Akriti", "Justin", "Marcos"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Wall", "Chau", "Keswani", "Marx"]
# Sample clothing product names
clothing_names = [
    "T-Shirt", "Jeans", "Jacket", "Sweater", "Hoodie",
    "Shorts", "Dress", "Blouse", "Skirt", "Pants",
    "Shoes", "Sandals", "Sneakers", "Socks", "Hat",
    "Scarf", "Gloves", "Coat", "Belt", "Tie",
    "Tank Top", "Cardigan", "Overalls", "Tracksuit", "Polo Shirt",
    "Cargo Pants", "Capris", "Dungarees", "Boots", "Cufflinks",
    "Raincoat", "Peacoat", "Blazer", "Slippers", "Underwear",
    "Leggings", "Windbreaker", "Tracksuit Bottoms", "Beanie", "Bikini"
]
# List of random colors
colors = [
    "Red", "Blue", "Green", "Yellow", "Black", "White", "Gray",
    "Pink", "Purple", "Orange", "Brown", "Teal", "Navy", "Maroon",
    "Gold", "Silver", "Beige", "Lavender", "Turquoise", "Coral"
]

# Function to create sample customers with random names
def create_customers(count=5):
    customers = []
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"

        customer = stripe.Customer.create(
            name=name,
            email=email,
            description="Sample customer for testing"
        )
        customers.append(customer)
        print(f"Created Customer: {customer['name']} (ID: {customer['id']})")
    return customers

# Function to create sample products with random clothing names and colors
def create_products(count=3):
    products = []
    for _ in range(count):
        color = random.choice(colors)
        product_name = random.choice(clothing_names)
        full_name = f"{color} {product_name}"
        product = stripe.Product.create(
            name=full_name,
            description=f"This is a {color.lower()} {product_name.lower()}"
        )
        products.append(product)
        print(f"Created Product: {product['name']} (ID: {product['id']})")
    return products

# Function to create prices for the products with random unit_amount
def create_prices(products, min_price=500, max_price=5000):
    prices = []
    for product in products:
        unit_amount = random.randint(min_price, max_price)  # Random amount in cents
        price = stripe.Price.create(
            unit_amount=unit_amount,
            currency="usd",
            product=product['id']
        )
        prices.append(price)
        print(f"Created Price: ${unit_amount / 100:.2f} for Product {product['name']} (ID: {price['id']})")
    return prices

# Function to create random purchases for each customer
def create_purchases(customers, prices, max_purchases_per_customer=5):
    purchases = []
    for customer in customers:
        num_purchases = random.randint(1, max_purchases_per_customer)  # Random number of purchases per customer
        for _ in range(num_purchases):
            price = random.choice(prices)  # Randomly select a product's price
            purchase = stripe.PaymentIntent.create(
                amount=price['unit_amount'],  # Amount in cents
                currency=price['currency'],
                customer=customer['id'],
                payment_method_types=["card"],  # Simulate card payment
                description=f"Purchase of {price['product']} by {customer['name']}"
            )
            purchases.append(purchase)
            print(f"Created Purchase for Customer {customer['name']} (Amount: ${price['unit_amount'] / 100:.2f})")
    return purchases

# Main function to create sample data
def main():
    print("Creating sample customers with random names...")
    customers = create_customers(count=20)

    print("\nCreating sample products with random clothing names and colors...")
    products = create_products(count=30)

    print("\nCreating prices for products with random amounts...")
    prices = create_prices(products, min_price=500, max_price=5000)

    print("\nCreating random purchases for each customer...")
    purchases = create_purchases(customers, prices, max_purchases_per_customer=10)

    print("\nSample data creation complete!")
    print(f"Created {len(customers)} customers, {len(products)} products, and {len(purchases)} purchases.")

if __name__ == "__main__":
    main()
