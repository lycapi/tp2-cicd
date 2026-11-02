from datetime import datetime


def calculate_delivery_fee(distance, weight):
    if distance is None or weight is None or distance < 0 or weight < 0:
        raise ValueError("La distance et le poids doivent être positifs")
    if distance > 10:
        raise ValueError("Livraison impossible au-delà de 10 km")

    fee = 2.00
    if distance > 3:
        fee += (distance - 3) * 0.50
    if weight > 5:
        fee += 1.50

    return round(fee, 2)


PROMO_CODES_DB = {
    "BIENVENUE20": {
        "code": "BIENVENUE20",
        "type": "percentage",
        "value": 20,
        "minOrder": 15.00,
        "expiresAt": "2026-12-31",
    },
    "REDUC5": {
        "code": "REDUC5",
        "type": "fixed",
        "value": 5.0,
        "minOrder": 10.00,
        "expiresAt": "2026-12-31",
    },
    "EXPIRE10": {
        "code": "EXPIRE10",
        "type": "percentage",
        "value": 10,
        "minOrder": 5.00,
        "expiresAt": "2020-01-01",
    },
}


def apply_promo_code(subtotal, promo_code, promo_codes_db=None):
    """Applique un code promo au sous-total d'une commande."""
    if promo_codes_db is None:
        promo_codes_db = PROMO_CODES_DB

    if subtotal is None or subtotal < 0:
        raise ValueError("Le sous-total doit être positif")

    if not promo_code:
        return {"discount": 0.0, "new_subtotal": round(subtotal, 2)}

    if promo_code not in promo_codes_db:
        raise ValueError(f"Code promo '{promo_code}' invalide ou inconnu")

    promo = promo_codes_db[promo_code]

    if subtotal < promo["minOrder"]:
        raise ValueError(f"Commande minimum de {promo['minOrder']}€ requise")

    expiry_date = datetime.strptime(promo["expiresAt"], "%Y-%m-%d")
    if datetime.now() > expiry_date:
        raise ValueError("Ce code promo a expiré")

    if promo["type"] == "percentage":
        discount = subtotal * (promo["value"] / 100.0)
    elif promo["type"] == "fixed":
        discount = float(promo["value"])
    else:
        discount = 0.0

    discount = min(discount, subtotal)
    new_subtotal = max(0.0, subtotal - discount)

    return {"discount": round(discount, 2), "new_subtotal": round(new_subtotal, 2)}


def calculate_surge(hour, day_of_week):
    """Calcule le multiplicateur de livraison (surge) selon le jour et l'heure."""
    day = day_of_week.lower().strip()

    if hour < 10 or hour >= 22:
        return 0.0

    if day in ["vendredi", "samedi"] and 19 <= hour < 22:
        return 1.8
    elif day == "dimanche":
        return 1.2
    elif day in ["lundi", "mardi", "mercredi", "jeudi"]:
        if 12 <= hour < 14:
            return 1.3
        elif 19 <= hour < 21:
            return 1.5

    return 1.0


def calculate_order_total(items, distance, weight, promo_code=None, hour=12, day_of_week="mardi"):
    """Calcule le total complet d'une commande."""
    if not items:
        raise ValueError("La liste des articles ne peut pas être vide")

    subtotal = 0.0
    for item in items:
        price = item.get("price", 0)
        qty = item.get("quantity", 0)
        if price < 0 or qty <= 0:
            raise ValueError("Prix ou quantité d'article invalide")
        subtotal += price * qty

    subtotal = round(subtotal, 2)

    promo_res = apply_promo_code(subtotal, promo_code)
    discount = promo_res["discount"]
    subtotal_after_discount = promo_res["new_subtotal"]

    delivery_fee = calculate_delivery_fee(distance, weight)
    surge = calculate_surge(hour, day_of_week)

    if surge == 0.0:
        raise ValueError("Le service de livraison est fermé à cette heure")

    final_delivery_fee = round(delivery_fee * surge, 2)
    total = round(subtotal_after_discount + final_delivery_fee, 2)

    return {
        "subtotal": subtotal,
        "discount": discount,
        "deliveryFee": final_delivery_fee,
        "surge": surge,
        "total": total,
    }
