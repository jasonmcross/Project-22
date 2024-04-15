from flask import Flask, Blueprint, render_template, request, flash, session
from website.Strategy import main_dev
from database.collections import DatabaseOperations

views = Blueprint('views', __name__)
db_ops = DatabaseOperations()

@views.route('/', methods=['GET', 'POST'])
def developer_home():
    collection_names = db_ops.get_collection_names()
    
    if request.method == 'POST':
        problem = request.form.get('problem')
        collection = request.form.get('collection')

        if len(problem) < 2:
            flash('Enter a valid design problem.', category='error')
        elif len(problem) > 10000:
            flash('Enter a valid design problem.', category='error')
        elif collection == "0":
            flash('Select a digital library collection', category='error')
        else:
            patterns = main_dev.main(problem, collection)
            flash('Design problem submitted.', category='success')
            return render_template("developer-home.html", patterns=patterns, collections=collection_names)
        
    return render_template("developer-home.html", collections=collection_names)

@views.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    if 'logged_in' not in session:
        flash('Cannot view page', category='error')
        #return render_template("admin-login.html")
        collection_names = db_ops.get_collection_names()
        libraries = ["SourceMaking (Gang of Four)", "RefactoringGuru (Gang of Four)", "GeeksForGeeks (Gang of Four)"]
        return render_template("admin-home.html", collections=collection_names, libraries=libraries)
    else:
        if request.method =='POST':
            req = request.form.get('req')
        
            if req == "crawl":
                return render_template("admin-home.html")
            elif req == "update":
                return render_template("admin-home.html")
            elif req == "delete":
                return render_template("admin-home.html")

        libraries = ["SourceMaking (Gang of Four)", "RefactoringGuru (Gang of Four)", "GeeksForGeeks (Gang of Four)"]
        return render_template("admin-home.html", libraries=libraries)
