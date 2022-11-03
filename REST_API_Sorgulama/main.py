from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)


class MeshurYemekler(Resource):
    def get(self):
        data = pd.read_csv('yemekler.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        yemekAdi = request.args['yemekAdi']
        plakaNo = request.args['plakaNo']
        sehirAdi = request.args['sehirAdi']

        data = pd.read_csv('yemekler.csv')

        new_data = pd.DataFrame({
            'yemekAdi': [yemekAdi],
            'plakaNo': [plakaNo],
            'sehirAdi': [sehirAdi]
        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('yemekler.csv', index=False)
        return {'data': new_data.to_dict('records')}, 200

    def delete(self):
        yemekAdi = request.args['yemekAdi']
        data = pd.read_csv('yemekler.csv')
        data = data[data['yemekAdi'] != yemekAdi]

        data.to_csv('yemekler.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200


class Sehirler(Resource):
    def get(self):
        data = pd.read_csv('yemekler.csv', usecols=[2])
        data = data.to_dict('records')

        return {'data': data}, 200


class Yemekler(Resource):
    def get(self, sehirAdi):
        data = pd.read_csv('yemekler.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['yemekAdi'] == sehirAdi:
                return {'data': entry}, 200
        return {'message': 'No entry found with this name !'}, 404


# Add URL endpoints
api.add_resource(MeshurYemekler, '/meshur')
api.add_resource(Sehirler, '/sehirler')
api.add_resource(Yemekler, '/<string:yemekler>')

if __name__ == '__main__':
    #     app.run(host="0.0.0.0", port=5000)
    app.run()