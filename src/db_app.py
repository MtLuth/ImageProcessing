from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class DBManager:
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

        self.Parking = Parking
        self.Card = Card

    def create_card(self, series_number, status):
        with self.app.app_context():
            new_card = self.Card(series_number=series_number, status=status)
            self.db.session.add(new_card)
            self.db.session.commit()
            print("Card created successfully")

    def get_all_card(self):
        cards = []
        with self.app.app_context():
            all_cards = self.Card.query.all()
            for card in all_cards:
                cards.append((card.series_number, card.status))
        return cards
    
    def get_card_by_status(self, status):
        cards = []
        with self.app.app_context():
            all_cards = self.Card.query.filter_by(status=status)
            for card in all_cards:
                cards.append((card.series_number, card.status))
        return cards

    def update_card_status(self, series_number, new_status):
        with self.app.app_context():
            card = self.Card.query.filter_by(series_number=series_number).first()
            if card:
                card.status = new_status
                self.db.session.commit()
                print("Card status updated successfully")
            else:
                print("Card not found")

    def create_parking(self, license, check_in, check_out, series_number):
        with self.app.app_context():
            new_license = self.Parking(license=license, check_in=check_in, check_out=check_out, series_number=series_number)
            self.db.session.add(new_license)
            self.db.session.commit()
            print("License created successfully")

    def get_all_parkings(self):
        with self.app.app_context():
            all_parkings = self.Parking.query.all()


    def get_parkings_by_series(self, series_number):
        with self.app.app_context():
            parkings = self.Parking.query.filter_by(series_number=series_number).all()
            for parking in parkings:
                print(f"Parking ID: {parking.id}, License: {parking.license}")

if __name__ == '__main__':
    db_manager = DBManager()
    with db_manager.app.app_context():
        db_manager.db.create_all()

        # Test your functions
        db_manager.get_all_parkings()
