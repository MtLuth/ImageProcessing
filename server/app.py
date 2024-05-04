from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usename:password@localhost/xulyanh'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    license = db.Column(db.String(20))
    gioVao = db.Column(db.String(120))
    gioRa = db.Column(db.String(120))
    maThe = db.Column(db.String(120))

class LicenseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'license')

license_schema = LicenseSchema()
licenses_schema = LicenseSchema(many=True)


@app.route('/license', methods=['POST'])
def add_license():
    data = request.get_json()
    new_license = License(username=data['username'], license=data['license'], gioVao=data['gioVao'], gioRa=data['gioRa'], maThe=data['maThe'])
    db.session.add(new_license)
    db.session.commit()
    return jsonify({'message': 'License created successfully'}), 201



@app.route('/licenses', methods=['GET'])
def get_licenses():
    all_licenses = License.query.all()
    result = licenses_schema.dump(all_licenses)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)