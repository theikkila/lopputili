from flask import Flask
import markdown2

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/esittelysivu')
def introduction():
    return markdown2.markdown_path('doc/generated/documentation.md')

if __name__ == '__main__':
    app.run()