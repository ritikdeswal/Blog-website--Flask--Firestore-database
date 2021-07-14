import os
import glob
from flask import Flask, render_template, request, redirect, url_for, session , g
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key=os.urandom(24)


@app.route("/")
@app.route("/home")
def index():
    page_number=request.args.get('page',1,type=int)

    # fetch all the documents from firestore database
    every_doc = db.collection('blog_db').order_by('date',direction=firestore.Query.DESCENDING).get()
    blogAll = []
    for item in every_doc:
        blogAll.append(item.to_dict())
    # split the total number of blogs per page =10
    # for page number =2 
    # paginate=blogAll[(2-1)*10 : 10*2]
    # paginate=blogAll[10 :20]
    paginate=blogAll[(page_number-1)*10:10*page_number]
    if len(blogAll)%10==0:
        total_pages=len(blogAll)//10
    else:total_pages=len(blogAll)//10+1

    return render_template("index.html", blogall=blogAll,paginate=paginate,total_pages=total_pages)


@app.route("/<string:title>")
def blog_main(title):
    blog_title = title.replace("%20", " ")
    #  fetching all the documents from firestore database on this page
    # for the search bar so that it can search from all the titles
    every_doc = db.collection('blog_db').get()
    blogAll = []
    for item in every_doc:
        blogAll.append(item.to_dict())

    # fetching specific blog that is requested by its title name
    blog_specific = db.collection("blog_db").where("title", "==", blog_title).get()


    # if someone puts wrong title name in the URL ,it will throw error message 404 
    if blog_specific==[]:
       return (
           render_template("error.html", message="error 404 bud. Check the URL ,time to make the chimi-fuckin'-changas. "),
           404,)

    return render_template("blog.html", blog=blog_specific[0].to_dict(),blogall=blogAll, title="blogs")



@app.route("/privacy")
def privacy():
    return render_template("privacy.html", title="privacy")



# admin login page that comes before the dashboard
@app.route("/login", methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        session.pop('user',None)
        if request.form['password']=='<your_password>':
            session['user']=request.form['username']
            return redirect(url_for('admin'))

    return render_template("login-admin.html")


# admin dashboard only accessible if the login password is correct.
# cannot be accessed by only typing the URL
@app.route("/dashboard", methods=['GET', 'POST'])
def admin():
    if g.user:
        if (request.method == 'POST'):
            title = request.form.get('title')
            article = request.form.get('article')
            date = request.form.get('date')

            data = {
                "title": title,
                "article": article,
                'date': date
            }
            db.collection("blog_db").document(date).set(data)
            if request.files:
                # main blog image (neccessary)
                image = request.files["image"]

                # additional blog images
                image2 = request.files.getlist("image2")
            
                dirname = os.path.dirname(__file__)
                image.save(os.path.join(dirname, "static/img/uploads", image.filename))
                config = {
                    '<your_config_key_from_the_firebase_api_settings>'
                }


                firebase = pyrebase.initialize_app(config)

                storage = firebase.storage()
                path_cloud = date + '/' + image.filename
                path_local = "static/img/uploads/" + image.filename

                # first flask stores the image in local storage then pushes them to the firebase storage
                storage.child(path_cloud).put(path_local)

                # once image is uploaded in the Firebase Storage, it fetches the public URL of the image
                # and stores in the Firestore Database 
                # here unique Id is the date of the database
                image_url = storage.child(path_cloud).get_url("77")
                db.collection("blog_db").document(date).set({'image': image_url}, merge=True)
                img_list = []
                for img in image2:
                    if img.filename !='':
                        img.save(os.path.join(dirname, "static/img/uploads", img.filename))
                        path_cloud = date + '/' + img.filename
                        path_local = "static/img/uploads/" + img.filename
                        storage.child(path_cloud).put(path_local)
                        image_url = storage.child(path_cloud).get_url("2")
                        img_list.append(image_url)
                db.collection("blog_db").document(date).set({'image2': img_list}, merge=True)

        x = db.collection('blog_db').get()
        blogAll = []
        for item in x:
            blogAll.append(item.to_dict())

        # once the image are pushed to Firebase Storage
        # they are then removed from flask local storage
        fileList = glob.glob('static/img/uploads/*')
        for file in fileList:
                os.remove(file)

        return render_template("admin.html", title="admin", blogall=blogAll,user=session['user'])
    return redirect(url_for('login'))


# creating global user for the sessiion before accessing the admin dashboard
@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']


# it runs when we click on the logout button
@app.route('/dropsession')
def dropsession():
    session.pop('user',None)
    return redirect(url_for('login'))

# to delete the blogs, here the unique id is the date of the blog.
@app.route("/delete/<string:date>", methods=['GET', 'POST'])
def delete(date):
    db.collection('blog_db').document(date).delete()
    config = {
        '<your_config_key_from_the_firebase_api_settings>'
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    x = storage.list_files()
    for img in x:
        # img is blob object and img.name is folderName/Filename.jpg
        if date in img.name:
            storage.delete(img.name, config['apiKey'])
    return redirect(url_for('admin'))


@app.errorhandler(404)
def page_not_found(e):
    # for anyone trying different links or searching for images within the server

    return (
        render_template("error.html", message="error 404 bud. Check the URL ,time to make the chimi-fuckin'-changas. "),
        404,
    )


@app.errorhandler(400)
def bad_request(e):
    # For handling situations where the server doesn't know what to do with the browser's request

    return (
        render_template("error.html",
                        message="error 400.??.Yeah, the server couldn't understand what you asked for, Sorry"),
        400,
    )


@app.errorhandler(500)
def server_error(e):
    # error within server

    return (
        render_template("error.html", message="INTERNAL SERVER ERROR 500 ,They are just dumb machines...."),
        400,
    )


env = "dev"

if env == "dev":
    app.run(debug = True)
else:
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port='5000',debug =False)


