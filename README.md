# flask_sample_apis
 Python/ Flask - Create Article API's:
 - API to create an article with the title, article content and author name.
 - API to up vote the existing article using article id
 - API to list the articles which are ordered by a number of votes in descending order(higher votes at the top).
 
 
 Javascript- Create UI for the above Article API's.
 - two screens, one for creating the articles and one for listing the articles.
 - in the articles list page, itself user should be able to vote for a particular article and should be updated on the back end.
 - minimal UI would be sufficient and can use any CSS framework of your choice if required.

 
 Create DB and run the app.
 - enter into python interactive shell
 - import db object and generate SQLite database
 
  >>> from app import db
  
  >>> db.create_all()

 - And article.sqlite will be generated inside your flask_sample_apis folder.

 Run frontend and backend:
  >>> python app.py

 You can see the url up at :
 
 http://127.0.0.1:5000/
