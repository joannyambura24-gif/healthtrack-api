from flask import Flask, jsonify
from auth import auth_bp

app = Flask(__name__)

# Register authentication routes
app.register_blueprint(auth_bp)


@app.route("/")
def home():
    return jsonify({
        "message": "HealthTrack API is running successfully"
    })


@app.route("/health")
def health_check():
    return jsonify({
        "status": "OK",
        "service": "HealthTrack API"
    })


if __name__ == "__main__":
    app.run(debug=True)