from flask import Flask, request, jsonify

app = Flask(__name__)

user_data = {}

@app.route('/progress', methods=['POST'])
def save_progress():
    data = request.json
    user_data[data['username']] = data['completedCourses']
    return jsonify({"message": "Progress saved successfully!"})

@app.route('/progress/<username>', methods=['GET'])
def get_progress(username):
    return jsonify(user_data.get(username, []))

if __name__ == '__main__':
    app.run(debug=True)
