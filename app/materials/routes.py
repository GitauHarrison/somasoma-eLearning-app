from app.materials import bp
from flask import render_template

@bp.route('/materials')
def materials():
    example_materials = [
        {'title': 'Introduction to Python', 'description': 'Learn the basics of Python programming.'},
        {'title': 'Flask Web Development', 'description': 'Build web apps using Flask.'},
        {'title': 'Data Science with Python', 'description': 'Explore data analysis and visualization.'}
    ]
    return render_template('materials/materials.html', materials=example_materials)
