from flask import Flask, Blueprint, render_template, request, flash, session, redirect
from website.Strategy import main_dev, main_admin
from website.crawler.src import dig_lib_crawler
from database.designPatterns import DatabaseOperations

views = Blueprint('views', __name__)
db_ops = DatabaseOperations()

@views.route('/', methods=['GET', 'POST'])
def developer_home():
    collection_names = db_ops.get_unique_collections()
    
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
            db_ops.export_collection_to_csv(collection)
            patterns = main_dev.main(problem, collection)
            flash('Design problem submitted.', category='success')
            return render_template("developer-home.html", patterns=patterns, collections=collection_names)
        
    return render_template("developer-home.html", collections=collection_names)

@views.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    if 'logged_in' not in session:
        flash('Cannot view page', category='error')
        return redirect('/login')
    else:
        # Get current collections in database and their sources
        collection_names = db_ops.get_unique_collections()
        sources = db_ops.get_unique_combinations()#["SourceMaking (Gang of Four)", "RefactoringGuru (Gang of Four)", "GeeksForGeeks (Gang of Four)"]
        
        if request.method =='POST':
            req = request.form.get('req')
        
            if req == "crawler":
                # Run new web crawlers                
                dig_lib_crawler.run()
                flash('All new web crawlers have been run.', category='success')
                
            elif req == "update":
                # Get collection and model to use
                collection = request.form.get('collection')
                db_ops.export_collection_to_csv(collection)
                model = request.form.get('model')
                
                # Update collection using selected model
                main_admin.main(collection, model)
                flash('Collection updated with new model.', category='success')
                
            elif req == "delete":
                source = request.form.get('s')
                index = source.find('(')
                if index !=-1: 
                    libraryName = source[:index-1].strip()
                    collectionName= source[index+1:].split(')')[0].strip()
                db_ops.delete_rows_by_combination(libraryName, collectionName)
                return render_template("admin-home.html", collections=collection_names, sources=sources)


        return render_template("admin-home.html", collections=collection_names, sources=sources)
