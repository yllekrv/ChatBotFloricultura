from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'  # ou o IP do seu banco de dados
app.config['MYSQL_USER'] = 'root'      # seu usuário do MySQL
app.config['MYSQL_PASSWORD'] = 'root'      # sua senha do MySQL
app.config['MYSQL_DB'] = 'floricultura'  # nome do banco de dados

mysql = MySQL(app)

@app.route('/')
def index():
    
    cur = mysql.connection.cursor()

    
    cur.execute('SELECT * FROM servico')

    
    produtos = cur.fetchall()

    # Passando os resultados para o template
    return render_template('index.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
