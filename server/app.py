from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class DB_Connection:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/xulyanh'
        self.db = SQLAlchemy(self.app)

        class Parking(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            license = self.db.Column(self.db.String(20))
            check_in = self.db.Column(self.db.String(120))
            check_out = self.db.Column(self.db.String(120))
            cost = self.db.Column(self.db.Integer)
            series_number = self.db.Column(self.db.String(120))

        class Card(self.db.Model):
            series_number = self.db.Column(self.db.String(120), primary_key=True)
            status = self.db.Column(self.db.Boolean)

    def create_card(self, series_number, status):
        new_card = self.Card(series_number=series_number, status=status)
        self.db.session.add(new_card)
        self.db.session.commit()
        print("Card created successfully")

    def create_license(self, license, check_in, check_out, series_number):
        with self.app.app_context():
            new_license = self.Parking(license=license, check_in=check_in, check_out=check_out, series_number=series_number)
            self.db.session.add(new_license)
            self.db.session.commit()
            print("License created successfully")

    def get_all_licenses(self):
        with self.app.app_context():
            all_licenses = self.Parking.query.all()
            for license in all_licenses:
                print(f"License ID: {license.id}, License: {license.license}")

    def get_licenses_by_series(self, series_number):
        with self.app.app_context():
            licenses = self.Parking.query.filter_by(series_number=series_number).all()
            for license in licenses:
                print(f"License ID: {license.id}, License: {license.license}")

if __name__ == '__main__':
    db_connection = DB_Connection()
    with db_connection.app.app_context():
        db_connection.db.create_all()

        db_connection.create_card("XYZ456", False)

        # Test your functions
        db_connection.create_license("ABC123", "2024-05-04 08:00:00", "2024-05-04 18:00:00", "XYZ456")
        db_connection.create_license("DEF456", "2024-05-05 08:00:00", "2024-05-05 18:00:00", "XYZ456")
        db_connection.get_all_licenses()
        db_connection.get_licenses_by_series("XYZ456")
