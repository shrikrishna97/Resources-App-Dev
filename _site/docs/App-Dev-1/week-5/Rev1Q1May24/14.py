from flask import Flask, request
app = Flask(__name__)
@app.route('/get_value/<int:val2>')
def get_value(val2):
    val1 = request.args.get("val1")
    # val1 = request.args.get("val1","20")
    return "The value is "+ str(val2)
app.run(port= 5000,debug=True)