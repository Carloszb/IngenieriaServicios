from app import db

class Amigo(db.Model):
    __tablename__ = "amigos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    longi = db.Column(db.String(32))
    lati = db.Column(db.String(32))
    device = db.Column(db.String(512))

    def __repr__(self):
        return "<Amigo[{}]: {}>".format(self.id, self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'lati': self.lati,
            'longi': self.longi,
            'device': self.device
        }

def get_all_devices():
    amigos = Amigo.query.filter(Amigo.device != None, Amigo.device != "").all()
    return [amigo.device for amigo in amigos]
