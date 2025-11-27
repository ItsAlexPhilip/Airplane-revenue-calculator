from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_revenue(economy, business, first_class, distance, aircraft_type):
    rates = {"Economy": 5, "Business": 8, "First": 15}
    conditions_met = []

    # Calculate revenue for each class
    economy_revenue = economy * distance * rates["Economy"]
    business_revenue = business * distance * rates["Business"]
    first_revenue = first_class * distance * rates["First"]

    base_revenue = economy_revenue + business_revenue + first_revenue
    total_passengers = economy + business + first_class

    surcharge = 0
    discount = 0
    bonus = 0

    # Passenger surcharge
    if total_passengers > 300:
        surcharge = base_revenue * 0.10
        base_revenue += surcharge
        conditions_met.append(f"Passenger count over 300 → 10% surcharge applied: ₹{round(surcharge, 2)}")

    # Long-haul discount
    if distance > 5000:
        discount = base_revenue * 0.05
        base_revenue -= discount
        conditions_met.append(f"Flight distance over 5000 km → 5% discount applied: ₹{round(discount, 2)}")

    # A380 bonus
    if aircraft_type == "A380" and total_passengers > 250:
        bonus = 100000
        base_revenue += bonus
        conditions_met.append("A380 with more than 250 passengers → ₹100,000 bonus added")

    breakdown = {
        "economy_revenue": economy_revenue,
        "business_revenue": business_revenue,
        "first_revenue": first_revenue,
        "surcharge": surcharge,
        "discount": discount,
        "bonus": bonus
    }

    return base_revenue, conditions_met, breakdown


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            economy = int(request.form["economy"])
            business = int(request.form["business"])
            first_class = int(request.form["first_class"])
            distance = float(request.form["distance"])
            aircraft_type = request.form["aircraft"]

            if economy < 0 or business < 0 or first_class < 0 or distance <= 0:
                return render_template("index.html", error="Enter valid positive numbers")

            total_revenue, conditions_met, breakdown = calculate_revenue(
                economy, business, first_class, distance, aircraft_type
            )

            return render_template(
                "result.html",
                economy=economy,
                business=business,
                first_class=first_class,
                distance=distance,
                aircraft_type=aircraft_type,
                total_revenue=round(total_revenue, 2),
                conditions_met=conditions_met,
                breakdown=breakdown
            )
        except ValueError:
            return render_template("index.html", error="Invalid input. Enter numbers only.")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
