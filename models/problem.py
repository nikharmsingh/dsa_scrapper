from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Problem(db.Model):
    """
    Database model for storing DSA problems.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50))
    url = db.Column(db.String(200))
    points = db.Column(db.String(50))
    tags = db.Column(db.String(200))

    def __repr__(self):
        return f'<Problem {self.title}>'

    def to_dict(self):
        """
        Convert problem object to dictionary.
        """
        return {
            'id': self.id,
            'title': self.title,
            'platform': self.platform,
            'difficulty': self.difficulty,
            'url': self.url,
            'points': self.points,
            'tags': self.tags
        } 