from flask import Flask, render_template
from getGasPrices import GetHenryHubGasPrices

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/gas/prices", methods=['GET'] )
def gasPrices():
    henryHub = GetHenryHubGasPrices()
    return henryHub.getMeHenryHubGasPrices()

if __name__ == "__main__":
    app.run()
