from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    result = {
        'status': 'ok',
        'data': "data"
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run()
