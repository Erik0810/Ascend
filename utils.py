from flask import flash, redirect, session, url_for

#Ensure user is logged in before proceeding with sql queries etc
def get_user_id():
    
    user_id = session.get('user_id')  

    #Redirect to login if issue is encountered
    if not user_id:
        flash("User not found or session expired.", "error")
        return redirect(url_for('loginSys.home'))  

    return int(user_id)