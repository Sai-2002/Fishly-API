from flask import Blueprint, request, jsonify
from bson import ObjectId
import razorpay

from src.db.orders_db import placeOrder

payment = Blueprint("payment", __name__)
        
# Razorpay credentials (get them from your Razorpay dashboard)
RAZORPAY_KEY_ID = "rzp_test_NRt7i3dJar0Fqq"
RAZORPAY_KEY_SECRET = "0LuGqW0Oj5VV7qfdfyi1OWEf"

# Create Razorpay client instance
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@payment.route('/create_order', methods=['POST'])
def create_order():
    try:
        # Get the payment amount and currency from the request body
        data = request.json

        print(type(data.get('cost')))

        amount = str(int(data.get('cost'))*100)  # Amount in smallest currency unit (e.g., paise for INR)
        currency = data.get('currency', 'INR')  # Default currency is INR

        # Razorpay order payload
        order_data = {
            "amount": amount,
            "currency": currency,
            "payment_capture": 1  # Auto capture after payment success
        }

        # Create an order in Razorpay
        order = razorpay_client.order.create(order_data)

        return jsonify({
            "order_id": order['id'],
            "amount": order['amount'],
            "currency": order['currency'],
            "status": "Order created"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@payment.route("/paymentSuccess", methods = ["POST"])
def paymentSuccess():

    order = request.get_json()

    order['customer_id'] = ObjectId(order["customer_id"])

    return placeOrder(order)
