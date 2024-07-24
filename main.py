from flask import Flask, render_template, request

app = Flask(__name__)

def valida_cpf(cpf_enviado_usuario):
    cpf_enviado_usuario = ''.join(filter(str.isdigit, cpf_enviado_usuario))
    if len(cpf_enviado_usuario) != 11:
        return False
    if cpf_enviado_usuario == cpf_enviado_usuario[0] * 11:
        return False

    nove_digitos = cpf_enviado_usuario[:9]
    contador_regressivo_1 = 10

    resultado_digito_1 = 0
    for digito in nove_digitos:
        resultado_digito_1 += int(digito) * contador_regressivo_1
        contador_regressivo_1 -= 1

    digito_1 = (resultado_digito_1 * 10) % 11
    digito_1 = digito_1 if digito_1 <= 9 else 0

    dez_digitos = nove_digitos + str(digito_1)
    contador_regressivo_2 = 11

    resultado_digito_2 = 0
    for digito in dez_digitos:
        resultado_digito_2 += int(digito) * contador_regressivo_2
        contador_regressivo_2 -= 1

    digito_2 = (resultado_digito_2 * 10) % 11
    digito_2 = digito_2 if digito_2 <= 9 else 0

    cpf_gerado_pelo_calculo = f'{nove_digitos}{digito_1}{digito_2}'
    return cpf_enviado_usuario == cpf_gerado_pelo_calculo

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    cpf = None
    msg = ""
    color = ""
    if request.method == "POST":
        cpf = request.form.get("cpf")
        if cpf:
            result = valida_cpf(cpf)
            if result:
                msg = f"{cpf} é válido"
                color = "success"
            else:
                msg = "CPF inválido"
                color = "error"
    return render_template("index.html", result=result, cpf=cpf, msg=msg, color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
