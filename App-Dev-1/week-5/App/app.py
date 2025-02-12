from flask import Flask, render_template

appp = Flask(__name__)

@appp.route('/') #base url 
def hello_world():
    return 'Hello World! hi wo'

@appp.route('/hello') #
def hello():
    users =[
        {'username': "hi",'password': "123"}, #row 1
            {'username': "world"}, 
            {'username': "hello"}
            ]
    return render_template('happy.html', users=users )

if __name__ == '__main__':
    appp.run(debug=True)
