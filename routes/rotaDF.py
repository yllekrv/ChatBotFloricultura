from flask import Blueprint, request
from controller.DFCtrl import DFCtrl
from flask import Flask
from routes.df import rota_df 


df_ctrl = DFCtrl()
rota_df = Blueprint('rota_df', __name__)

@rota_df.route('/', methods=['POST'])
def processar_intencoes():
    return df_ctrl.processar_intencoes(request)


app = Flask(__name__)
app.register_blueprint(rota_df, url_prefix='/df')

if __name__ == '__main__':
    app.run(debug=True)
