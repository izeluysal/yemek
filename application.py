"""Flask Application - Yemek Tarifi Defteri"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os
import json
from pathlib import Path
from sqlalchemy import func

from config import Config
from models import db, Recipe, Tag, Comment


def create_app():
    """Application Factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Create necessary folders
    with app.app_context():
        Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
        Path('data').mkdir(exist_ok=True)
        db.create_all()
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register all application routes"""
    
    # Admin login required decorator
    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'admin_logged_in' not in session:
                return redirect(url_for('admin_login'))
            return f(*args, **kwargs)
        return decorated_function
    
    # ============ PUBLIC ROUTES ============
    
    @app.route('/')
    def index():
        """Home page with latest recipes and dashboard"""
        page = request.args.get('page', 1, type=int)
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).paginate(
            page=page, per_page=app.config['RECIPES_PER_PAGE']
        )
        tags = Tag.query.all()
        
        # Gather dashboard statistics
        total_recipes = Recipe.query.count()
        total_comments = Comment.query.count()
        
        # Calculate average cooking time
        avg_cook_time = db.session.query(func.avg(Recipe.cook_time)).scalar()
        avg_cook_time = round(avg_cook_time) if avg_cook_time else 0
        
        # Get cooking time distribution for bar chart
        recipes_list = Recipe.query.all()
        time_ranges = {
            '0-30 dk': 0,
            '30-60 dk': 0,
            '60-120 dk': 0,
            '120+ dk': 0
        }
        
        for recipe in recipes_list:
            if recipe.cook_time:
                if recipe.cook_time <= 30:
                    time_ranges['0-30 dk'] += 1
                elif recipe.cook_time <= 60:
                    time_ranges['30-60 dk'] += 1
                elif recipe.cook_time <= 120:
                    time_ranges['60-120 dk'] += 1
                else:
                    time_ranges['120+ dk'] += 1
        
        # Get tag distribution for donut chart
        tag_distribution = {}
        for tag in tags:
            recipe_count = tag.recipes.count()
            if recipe_count > 0:
                tag_distribution[tag.name] = recipe_count
        
        # Prepare chart data as JSON strings
        time_chart_data = json.dumps({
            'labels': list(time_ranges.keys()),
            'datasets': [{
                'label': 'Tarif Sayısı',
                'data': list(time_ranges.values()),
                'backgroundColor': '#10b981',
                'borderColor': '#059669',
                'borderWidth': 1
            }]
        })
        
        # Only include top tags to avoid cluttering
        top_tags = sorted(tag_distribution.items(), key=lambda x: x[1], reverse=True)[:8]
        tag_chart_data = json.dumps({
            'labels': [tag[0] for tag in top_tags],
            'datasets': [{
                'data': [tag[1] for tag in top_tags],
                'backgroundColor': [
                    '#0f172a', '#1e293b', '#334155', '#475569', '#64748b', '#94a3b8', '#cbd5e1', '#e2e8f0'
                ],
                'borderColor': '#f8fafc',
                'borderWidth': 2
            }]
        })
        
        # Extract unique ingredients from all recipes
        all_ingredients_set = set()
        for recipe in recipes_list:
            if recipe.ingredients:
                # ingredients is stored as JSON list, handle both list and string formats
                if isinstance(recipe.ingredients, list):
                    ingredients_list = recipe.ingredients
                else:
                    # If it's a string, split by comma or newline
                    ingredients_list = [ing.strip() for ing in recipe.ingredients.replace('\n', ',').split(',')]
                
                all_ingredients_set.update([ing.strip() for ing in ingredients_list if ing])
        
        all_ingredients = sorted(list(all_ingredients_set))
        
        return render_template(
            'index.html', 
            recipes=recipes, 
            tags=tags,
            total_recipes=total_recipes,
            total_comments=total_comments,
            avg_cook_time=avg_cook_time,
            time_chart_data=time_chart_data,
            tag_chart_data=tag_chart_data,
            all_ingredients=all_ingredients
        )
    
    @app.route('/search')
    def search():
        """Search and filter recipes"""
        query = request.args.get('q', '', type=str).strip()
        tag_ids = request.args.getlist('tags', type=int)
        
        # Base query
        recipes_query = Recipe.query
        
        # Filter by search query
        if query:
            recipes_query = recipes_query.filter(
                (Recipe.title.ilike(f'%{query}%')) |
                (Recipe.description.ilike(f'%{query}%')) |
                (Recipe.ingredients.contains(query))
            )
        
        # Filter by tags
        if tag_ids:
            for tag_id in tag_ids:
                recipes_query = recipes_query.filter(
                    Recipe.tags.any(Tag.id == tag_id)
                )
        
        # Paginate results
        page = request.args.get('page', 1, type=int)
        recipes = recipes_query.order_by(Recipe.created_at.desc()).paginate(
            page=page, per_page=app.config['RECIPES_PER_PAGE']
        )
        
        tags = Tag.query.all()
        selected_tags = tag_ids
        
        return render_template(
            'search.html',
            recipes=recipes,
            tags=tags,
            query=query,
            selected_tags=selected_tags
        )
    
    @app.route('/tarif/<slug>', methods=['GET', 'POST'])
    def recipe_detail(slug):
        """Recipe detail page"""
        recipe = Recipe.query.filter_by(slug=slug).first_or_404()
        
        # Handle comment submission
        if request.method == 'POST':
            author_name = request.form.get('author_name', '').strip()
            author_email = request.form.get('author_email', '').strip()
            rating = request.form.get('rating', type=int)
            comment_text = request.form.get('comment_text', '').strip()
            
            if author_name and author_email and rating and comment_text:
                comment = Comment(
                    recipe_id=recipe.id,
                    author_name=author_name,
                    author_email=author_email,
                    rating=rating,
                    text=comment_text
                )
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('recipe_detail', slug=slug))
        
        # Get comments
        comments = Comment.query.filter_by(recipe_id=recipe.id).order_by(Comment.created_at.desc()).all()
        
        return render_template('recipe_detail.html', recipe=recipe, comments=comments)
    
    # ============ ADMIN ROUTES ============
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        """Admin login page"""
        if request.method == 'POST':
            password = request.form.get('password', '')
            if password == app.config['ADMIN_PASSWORD']:
                session['admin_logged_in'] = True
                return redirect(url_for('admin_panel'))
            else:
                return render_template('admin_login.html', error='Invalid password')
        return render_template('admin_login.html')
    
    @app.route('/admin/logout')
    def admin_logout():
        """Admin logout"""
        session.pop('admin_logged_in', None)
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @admin_required
    def admin_panel():
        """Admin panel dashboard"""
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
        tags = Tag.query.all()
        comments = Comment.query.order_by(Comment.created_at.desc()).all()
        stats = {
            'total_recipes': len(recipes),
            'total_tags': len(tags),
            'total_comments': len(comments),
        }
        return render_template('admin/panel.html', recipes=recipes, tags=tags, comments=comments, stats=stats)
    
    @app.route('/admin/recipe/new', methods=['GET', 'POST'])
    @admin_required
    def admin_new_recipe():
        """Add new recipe"""
        if request.method == 'POST':
            # Normalize title to proper case (capitalize each word)
            title_input = request.form.get('title', '').strip()
            title = ' '.join(word.capitalize() for word in title_input.split())
            description = request.form.get('description', '').strip()
            ingredients_text = request.form.get('ingredients', '')
            instructions = request.form.get('instructions', '').strip()
            prep_time = request.form.get('prep_time', type=int) or None
            cook_time = request.form.get('cook_time', type=int) or None
            servings = request.form.get('servings', type=int) or 4
            tag_ids = request.form.getlist('tags', type=int)
            
            # Parse ingredients
            ingredients = [ing.strip() for ing in ingredients_text.split('\n') if ing.strip()]
            
            # Generate slug
            slug = Recipe.generate_slug(title)
            
            # Check if recipe already exists
            if Recipe.query.filter_by(slug=slug).first():
                return render_template('admin/recipe_form.html', error='Recipe already exists')
            
            # Handle image
            image_url = None
            
            # Check for image URL input first
            image_url_input = request.form.get('image_url', '').strip()
            if image_url_input:
                image_url = image_url_input
            # Otherwise, check for image file upload
            elif 'image' in request.files:
                image = request.files['image']
                if image and image.filename and allowed_file(image.filename):
                    # Save image
                    filename = f"{slug}_{datetime.utcnow().timestamp()}.{image.filename.rsplit('.', 1)[1].lower()}"
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_url = f"/uploads/{filename}"
            
            # If no image uploaded or URL provided, use default Turkish food image
            if not image_url:
                image_url = Recipe.generate_image_url(title)
            
            # Create recipe
            recipe = Recipe(
                title=title,
                slug=slug,
                description=description,
                ingredients=ingredients,
                instructions=instructions,
                image_url=image_url,
                prep_time=prep_time,
                cook_time=cook_time,
                servings=servings,
            )
            
            # Add tags
            if tag_ids:
                # Add selected tags
                for tag_id in tag_ids:
                    tag = Tag.query.get(tag_id)
                    if tag:
                        recipe.tags.append(tag)
            else:
                # If no tags selected, assign default "Diğer" tag
                default_tag = Tag.query.filter_by(name='Diğer').first()
                if not default_tag:
                    default_tag = Tag(name='Diğer')
                    db.session.add(default_tag)
                    db.session.flush()  # Flush to get the ID before adding to recipe
                recipe.tags.append(default_tag)
            
            db.session.add(recipe)
            db.session.commit()
            
            return redirect(url_for('admin_panel'))
        
        tags = Tag.query.all()
        return render_template('admin/recipe_form.html', tags=tags)
    
    @app.route('/admin/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_edit_recipe(recipe_id):
        """Edit recipe"""
        recipe = Recipe.query.get_or_404(recipe_id)
        
        if request.method == 'POST':
            # Normalize title to proper case (capitalize each word)
            title_input = request.form.get('title', '').strip()
            recipe.title = ' '.join(word.capitalize() for word in title_input.split())
            recipe.description = request.form.get('description', '').strip()
            
            ingredients_text = request.form.get('ingredients', '')
            recipe.ingredients = [ing.strip() for ing in ingredients_text.split('\n') if ing.strip()]
            
            recipe.instructions = request.form.get('instructions', '').strip()
            recipe.prep_time = request.form.get('prep_time', type=int) or None
            recipe.cook_time = request.form.get('cook_time', type=int) or None
            recipe.servings = request.form.get('servings', type=int) or 4
            
            # Handle image
            # Check for image URL input first
            image_url_input = request.form.get('image_url', '').strip()
            if image_url_input:
                recipe.image_url = image_url_input
            # Otherwise, check for image file upload
            elif 'image' in request.files:
                image = request.files['image']
                if image and image.filename and allowed_file(image.filename):
                    filename = f"{recipe.slug}_{datetime.utcnow().timestamp()}.{image.filename.rsplit('.', 1)[1].lower()}"
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    recipe.image_url = f"/uploads/{filename}"
            
            # Update tags
            tag_ids = request.form.getlist('tags', type=int)
            recipe.tags.clear()
            if tag_ids:
                for tag_id in tag_ids:
                    tag = Tag.query.get(tag_id)
                    if tag:
                        recipe.tags.append(tag)
            else:
                # If no tags selected, assign default "Diğer" tag
                default_tag = Tag.query.filter_by(name='Diğer').first()
                if not default_tag:
                    default_tag = Tag(name='Diğer')
                    db.session.add(default_tag)
                    db.session.flush()
                recipe.tags.append(default_tag)
            
            db.session.commit()
            return redirect(url_for('admin_panel'))
        
        tags = Tag.query.all()
        return render_template('admin/recipe_form.html', recipe=recipe, tags=tags)
    
    @app.route('/admin/recipe/<int:recipe_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_recipe(recipe_id):
        """Delete recipe"""
        recipe = Recipe.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    @app.route('/admin/tag/new', methods=['POST'])
    @admin_required
    def admin_new_tag():
        """Add new tag"""
        name = request.form.get('name', '').strip()
        
        if not name:
            return {'error': 'Tag name required'}, 400
        
        if Tag.query.filter_by(name=name).first():
            return {'error': 'Tag already exists'}, 400
        
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        
        return redirect(url_for('admin_panel'))
    
    @app.route('/admin/tag/<int:tag_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_tag(tag_id):
        """Delete tag"""
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    # ============ UTILITY FUNCTIONS ============
    
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    # Comment management
    @app.route('/admin/comment/<int:comment_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_comment(comment_id):
        """Delete a comment"""
        comment = Comment.query.get_or_404(comment_id)
        recipe_slug = comment.recipe.slug
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    # Favicon handler (suppress browser requests)
    @app.route('/favicon.ico')
    def favicon():
        return '', 204
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return render_template('500.html'), 500


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
