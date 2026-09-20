"""Database Models for Recipe Application"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON

db = SQLAlchemy()


# Association Table for Many-to-Many relationship between Recipes and Tags
recipe_tags = db.Table(
    'recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Recipe(db.Model):
    """Recipe Model"""
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True, index=True)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(JSON, nullable=False, default=list)  # JSON array
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    prep_time = db.Column(db.Integer, nullable=True)  # minutes
    cook_time = db.Column(db.Integer, nullable=True)  # minutes
    servings = db.Column(db.Integer, nullable=True, default=4)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tags = db.relationship(
        'Tag',
        secondary=recipe_tags,
        backref=db.backref('recipes', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<Recipe {self.title}>'
    
    def to_dict(self):
        """Convert recipe to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'image_url': self.image_url,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
    
    @staticmethod
    def generate_slug(title):
        """Generate URL-friendly slug from title"""
        import re
        # Convert to lowercase
        slug = title.lower()
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        # Remove special characters except hyphens
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        # Remove multiple consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug


class Tag(db.Model):
    """Tag Model"""
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    def to_dict(self):
        """Convert tag to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'recipe_count': self.recipes.count(),
        }


class Comment(db.Model):
    """Comment Model"""
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False, index=True)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    text = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationship
    recipe = db.relationship('Recipe', backref=db.backref('comments', lazy='dynamic', cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<Comment by {self.author_name} on Recipe {self.recipe_id}>'
    
    def to_dict(self):
        """Convert comment to dictionary"""
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'author_name': self.author_name,
            'author_email': self.author_email,
            'rating': self.rating,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
        }
