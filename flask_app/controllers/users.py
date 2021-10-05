from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import friendship
from flask_app.models import user

@app.route("/")
@app.route("/friendships")
def form():
    users = user.User.get_all_with_friendships()
    
    return render_template("main.html", users=users)

@app.route("/save_user", methods=["POST"])
def save_user():
    if user.User.validate_user(request.form):
        newUser = user.User.save(request.form)
        if newUser:
            return redirect('/')
        else:
            flash(f"There was an error saving the data")
            return redirect('/')
    else:
        return redirect('/')

@app.route("/save_friendship", methods=["POST"])
def save_friendship():
    user1= user.User.get_user_info(data={'id': int(request.form['user_id'])})
    user2= user.User.get_user_info(data={'id': int(request.form['friend_id'])})
    newFriendship = friendship.Friendship.save(user1,user2)
    if newFriendship:
        return redirect('/')
    else:
        flash(f"The friendship requested already exists or is not valid","friendship")
        return redirect('/')