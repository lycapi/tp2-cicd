from flask import Flask, request, jsonify
from src.pricing import calculate_order_total, apply_promo_code

app = Flask(__name__)
orders_db = {}
order_counter = 1


@app.route("/orders/simulate", methods=["POST"])
def simulate_order():
    data = request.get_json() or {}
    try:
        res = calculate_order_total(
            items=data.get("items", []),
            distance=data.get("distance"),
            weight=data.get("weight"),
            promo_code=data.get("promoCode"),
            hour=data.get("hour", 12),
            day_of_week=data.get("dayOfWeek", "mardi"),
        )
        return jsonify(res), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/orders", methods=["POST"])
def create_order():
    global order_counter
    data = request.get_json() or {}
    try:
        pricing = calculate_order_total(
            items=data.get("items", []),
            distance=data.get("distance"),
            weight=data.get("weight"),
            promo_code=data.get("promoCode"),
            hour=data.get("hour", 12),
            day_of_week=data.get("dayOfWeek", "mardi"),
        )
        order = {"id": order_counter, "items": data.get("items"), "pricing": pricing}
        orders_db[order_counter] = order
        order_counter += 1
        return jsonify(order), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = orders_db.get(order_id)
    if not order:
        return jsonify({"error": "Commande non trouvée"}), 404
    return jsonify(order), 200
