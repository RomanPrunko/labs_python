from app import db

class Telephone(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    release_year = db.Column(db.Integer)

    def __repr__(self):
        return f"Telephone {self.name} {self.model}"
