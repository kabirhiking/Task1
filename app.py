
import string
import random
from flask import Flask, request, render_template, jsonify, redirect
from models import db, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Generate a random 6-character string for the short URL
def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        if original_url:
            # Generate a unique short_id
            short_id = generate_short_id()
            while URL.query.filter_by(short_id=short_id).first() is not None:
                short_id = generate_short_id()

            # Save the URL and short ID to the database
            new_url = URL(original_url=original_url, short_id=short_id)
            db.session.add(new_url)
            db.session.commit()

            # Return JSON with the short URL
            short_url = request.host_url + short_id
            return jsonify({"original_url": original_url, "short_url": short_url})
        else:
            # Return error if original_url is not provided
            return jsonify({"error": "No URL provided"}), 400

    # For GET requests, render the main HTML form
    return render_template('index.html')

# Redirect route to handle the shortened URL
@app.route('/<short_id>')
def redirect_to_url(short_id):
    url = URL.query.filter_by(short_id=short_id).first_or_404()
    return redirect(url.original_url)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
