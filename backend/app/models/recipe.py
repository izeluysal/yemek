from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

recipe_tags = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    ingredients = Column(JSON, nullable=False, default=list)
    instructions = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tags = relationship("Tag", secondary=recipe_tags, back_populates="recipes")

    def __repr__(self):
        return f"<Recipe(id={self.id}, title='{self.title}', slug='{self.slug}')>"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    recipes = relationship("Recipe", secondary=recipe_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"