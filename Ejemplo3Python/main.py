from flask import Flask, redirect, url_for, render_template, request
from gramatica import parse
app = Flask(__name__)

@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"]
        inpt=inpt.replace("/","aa11a223")
        return redirect(url_for("output", inpt=inpt))
    else:
        return render_template('analyze.html', initial="3*2*(2+5)==15|2+3*4/(3+1)==10 & 6*7/(8+1)==10")

@app.route('/output/<inpt>')
def output(inpt):
    inpt=inpt.replace("aa11a223","/")
    result = parse(inpt)
    return render_template('output.html', input=result)

if __name__ == "__main__":
    app.run(debug=True)#para que se actualice al detectar cambios