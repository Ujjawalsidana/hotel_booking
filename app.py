from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'hotelbooking535@gmail.com'
app.config['MAIL_PASSWORD'] = 'dteddvmyotwpyytx'
app.config['MAIL_DEFAULT_SENDER'] = 'hotelbooking535.com'

mail = Mail(app)

HOTELS = {
    "Dubai": [
        {
            "name": "Jumeirah Al Burj",
            "image": "https://via.placeholder.com/400x300",
            "rooms": [
                {"type": "Single Room", "image": "https://via.placeholder.com/200x150"},
                {"type": "Double Room", "image": "https://via.placeholder.com/200x150"}
            ]
        }
    ]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hotels", methods=["POST"])
def search_hotels():
    city = request.form.get("city")
    date = request.form.get("date")
    hotels = HOTELS.get(city, [])
    return render_template("hotels.html", city=city, date=date, hotels=hotels)

@app.route("/hotel/<city>/<hotel_name>")
def hotel_details(city, hotel_name):
    hotels = HOTELS.get(city, [])
    hotel = next((h for h in hotels if h["name"] == hotel_name), None)
    if hotel:
        return render_template("rooms.html", hotel=hotel)
    return redirect(url_for("index"))
@app.route("/book/<hotel_name>/<room_type>", methods=["GET", "POST"])
def book_room(hotel_name, room_type):
    if request.method == "POST":
        # Handle booking form submission
        guest_names = request.form.getlist("guest_name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        booking_date = request.form.get("date")
        payment_mode = request.form.get("payment_mode")  
        subject = "Congratulations! Your Room is Booked"
        body = f"""
        Dear {guest_names[0]},
        
        Your room at {hotel_name} ({room_type}) has been successfully booked.
        
        Booking Details:
        - Guests: {', '.join(guest_names)}
        - Phone: {phone}
        - Email: {email}
        - Payment:  {payment_mode}

        
        We look forward to hosting you!

        Best regards,
        The Hotel Booking Team
        """
        send_email(subject, body, email)

        flash("Booking successful! A confirmation email has been sent.", "success")
        


        # Process booking (e.g., save to a database, send confirmation email, etc.)
        flash(f"Booking confirmed for {len(guest_names)} guest(s) at {hotel_name} - {room_type} on {booking_date}.", "success")
        return redirect(url_for("index"))

    # Render booking page on GET request
    return render_template("book.html", hotel_name=hotel_name, room_type=room_type)
def send_email(subject, body, recipient):
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    app.run(debug=True)
