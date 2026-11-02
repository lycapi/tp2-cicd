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
