"""
11COS Hackathon 2026 - [Hayden Parkes]
"""

from flask import Flask, render_template, request, redirect, url_for
import json
import datetime

app = Flask(__name__)

# ------------------------------------------------------------------
# Helper functions — load and save JSON
# ------------------------------------------------------------------

def load_json(filename):
    """load data from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)


def save_json(filename, data):
    """save data to a JSON file with indentation for readability."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ------------------------------------------------------------------
# Routes — fill in the missing logic
# ------------------------------------------------------------------

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/products", methods=["POST", "GET"])
def products_page():
    cart = load_json("cart.json")
    products = load_json("products.json")
    electronics = []
    stationary = []
    clothing = []
    for product in products:
        if product["category"] == "electronics":
            electronics.append(product)
        elif product["category"] == "stationary":
            stationary.append(product)
        elif product["category"] == "clothing":
            clothing.append(product)
    #to get info for the different catagories in the shop

    if request.method == "POST":
        item_id = int(request.form.get("item"))
        new = True
        for item in cart:
            if item["product_id"] == item_id:
                item["quantity"] += 1
                new = False
                break
        if new == True: 
            for item in products:
                if item["id"] == item_id:
                    add_item = {   
                        "product_id": item["id"],
                        "name": item["name"],
                        "price": item["price"],
                        "quantity": 1
                        }
                    cart.append(add_item)
        save_json("cart.json", cart)
        #algorithm to check either add a new item or add quantity

    
    return render_template("products.html", products=products, electronics=electronics, stationary=stationary, clothing=clothing)


@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    cart_items = load_json("cart.json")
    total = 0
    for item in cart_items:
        total += item["price"] * item["quantity"]
        #math to get total price

    if request.method == "POST" and cart_items != []:
        return redirect(url_for("invoice_page"))
    
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/invoice", methods=["GET", "POST"])
def invoice_page():
    cart_items = load_json("cart.json")
    invoices = load_json("invoices.json")
    total = 0
    count = 1
    for item in cart_items:
        total += item["price"] * item["quantity"]
    print(total)
    date = datetime.datetime.now()
    new_date = date.strftime("%Y")+"-"+date.strftime("%m")+"-"+date.strftime("%d"),
    #to get the date and time as per standard invoice
    for invoice in invoices:
        count += 1

    
    invoice = {
        "invoice_id": count,
        "date": new_date,
        "items": cart_items,
        "total": total
    }
    invoices.append(invoice)
    save_json("invoices.json", invoices)
    save_json("cart.json", [])


    
        
        
    return render_template("invoice.html", invoice=invoice, cart_items=cart_items)


@app.route("/add", methods=["POST"])
def add_to_cart():
    products = load_json("products.json")
    product_id = request.form.get('product_id', type=int)
    return redirect(url_for("cart_page"))
    #simple route to get data for cart


@app.route("/remove/<int:id>", methods=["POST", "GET"])
#url variable used to get 
def remove_from_cart(id):
    cart = load_json("cart.json")
    new = []
    for item in cart:
        if item["product_id"] != id:
            new.append(item)
        elif item["product_id"] == id and item["quantity"] > 1:
            item["quantity"] -= 1
            new.append(item)
    save_json("cart.json", new)
        
    return redirect(url_for("cart_page"))


@app.route("/admin", methods=["POST", "GET"])
def add_category():
    catagories = load_json("categories.json")
    if request.method == "POST" and request.form.get("type") == "delete":
        id = request.form.get("catagory")
        new = []
        for catagory in catagories:
            if catagory != id:
                new.append(catagory)
                catagories = new
        save_json("categories.json", catagories)
    if request.method == "POST"  and request.form.get("type") == "add":
        catagories.append(request.form.get("catagory"))
        save_json("categories.json", catagories)
    return render_template("admin.html", catagories=catagories,)



# ------------------------------------------------------------------
# Run the application
# ------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5075)
