"""
11COS Hackathon 2026 - [Your Name Here]
"""

from flask import Flask, render_template, request, redirect, url_for
import json

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
    """homepage — show a welcome message and link to the shop."""
    # TODO: render the home page
    return render_template("index.html")


@app.route("/products")
def products_page():
    """show all products, optionally grouped by category."""
    # TODO: render the product listing page
    return render_template("products.html")


@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    """view and manage the shopping cart."""
    if request.method == "POST":
        # TODO: handle other cart actions (e.g. clear cart)
        return redirect(url_for("cart_page"))
    # TODO: render the cart page
    return render_template("cart.html")


@app.route("/invoice", methods=["GET", "POST"])
def invoice_page():
    """generate and display an invoice from the cart."""
    if request.method == "POST":
        # TODO: save cart as an invoice, then clear the cart
        return redirect(url_for("invoice_page"))
    # TODO: render the invoice page
    return render_template("invoice.html")


@app.route("/add", methods=["POST"])
def add_to_cart():
    """add a specific product to the cart via form submission."""
    product_id = request.form.get('product_id', type=int)
    # TODO: find the product by ID and add it to cart JSON
    return redirect(url_for("cart_page"))


@app.route("/remove", methods=["POST"])
def remove_from_cart():
    """remove an item from the cart by its index."""
    item_index = request.form.get('item_index', type=int)
    # TODO: remove the item at the given index from cart JSON
    return redirect(url_for("cart_page"))


@app.route("/add-category", methods=["POST"])
def add_category():
    """add a new category to the categories JSON file."""
    # TODO: read category name from form and append to categories JSON
    return redirect(url_for("products_page"))


@app.route("/delete-category", methods=["POST"])
def delete_category():
    """delete an existing category from the categories JSON file."""
    # TODO: read category name from form and remove from categories JSON
    return redirect(url_for("products_page"))


# ------------------------------------------------------------------
# Run the application
# ------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5075)
