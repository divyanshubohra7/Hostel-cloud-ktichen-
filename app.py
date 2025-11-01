from flask import Flask, render_template, request, redirect, url_for, session
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = "secretkey"

# Menu items
MENU = {
    "Maggi": 50,
    "Yippee": 40,
    "Chips Chat": 60,
    "Soya Bean Chat (20g Protein)": 80
}

@app.route('/')
def index():
    return render_template('index.html', menu=MENU)

@app.route('/add_to_cart/<item>')
def add_to_cart(item):
    cart = session.get('cart', {})
    cart[item] = cart.get(item, 0) + 1
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route("/remove/<item>")
def remove_from_cart(item):
    cart = session.get("cart", {})
    if item in cart:
        del cart[item]
        session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    total = sum(MENU.get(item, 0) * qty for item, qty in cart.items())
    return render_template("cart.html", cart=cart, menu=MENU, total=total)

# -----------------------------
# ✅ Payment Route (UPI Redirect)
# -----------------------------
UPI_ID = "7727974976@ibl"
UPI_PNAME = "Hostel Cloud Kitchen"

@app.route("/pay")
def pay():
    cart = session.get("cart", {})
    total = sum(MENU.get(item, 0) * qty for item, qty in cart.items())
    if total <= 0:
        return redirect(url_for("index"))

    params = {
        "pa": UPI_ID,
        "pn": UPI_PNAME,
        "am": f"{total:.2f}",
        "tn": "HostelFoodOrder",
        "cu": "INR"
    }
    upi_uri = "upi://pay?" + urlencode(params)
    return redirect(upi_uri)

if __name__ == "__main__":
    app.run(debug=True, port=1290)