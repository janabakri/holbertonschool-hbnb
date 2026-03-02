from app.extensions import db

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id")),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"))
)
