from flask import Flask, render_template, request

from scraping import scrape

app = Flask(__name__)


@app.route('/')
def redirect():
    return hello_world()


@app.route('/homepage/')
def hello_world():
    return search()


@app.route('/offline/')
def offline():
    return render_template('offline.html')


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/Search/', methods=["GET"])
def search():
    if request.method == "GET":
        return render_template('search.html')


@app.route('/Search_result', methods=["POST", "GET"])
def search_result():
    if request.method == 'POST':
        productname = request.form.get('username')
        global data
        data = scrape(productname)
        return render_template('search_result.html', message=data)
    if request.method == 'GET':
        data = []
        return render_template('search_result.html', message=data)


@app.route('/thulo', methods=["get"])
def thulo():
    if request.method == 'GET':
        return render_template("thulo.html", message=data)


@app.route('/sastodeal', methods=["get"])
def sasto():
    if request.method == 'GET':
        return render_template("sastodeal.html", message=data)


@app.route('/loading', methods=["get"])
def loading():
    if request.method == 'GET':
        return render_template("load.html")


if __name__ == "__main__":
    data = ''
    print("PROJECT DONE BY KIRAN ")
    app.run(debug=True,host='0.0.0.0')
