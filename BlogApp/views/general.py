import json, os
from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from BlogApp.forms import *
from BlogApp.models import *
from BlogApp import cache
#from BlogApp import gpt_125M, gpt_13B, gpt_27B
import readtime

def count_likes(blog_id):
    likers = liked_blog.query.filter_by(blog_id=blog_id).all()
    likes = len(likers)
    return likes

general = Blueprint('general', __name__)


@general.route("/", methods=['GET','POST'])
#@cache.cached(timeout=50)          #uncomment in final version
def root():
    if current_user.is_authenticated and current_user.id == 1:
        admin = True
    else:
        admin=False
    return render_template('general/home.html', admin=admin)
        

@general.route("/our_journey", methods=['GET','POST'])
#@cache.cached(timeout=50)          #uncomment in final version
def our_journey():
    readers = Profile.query.count()
    blogs = blog_data.query.count()
    writers = 0
    for i in Profile.query.all():
        if i.blogs.count() != 0:
            writers+=1
    return render_template('general/our_journey.html', readers=readers, blogs=blogs, writers=writers)  
 
 
@general.route("/tbfy", methods=['GET','POST'])
#@cache.cached(timeout=300)          #uncomment in final version
def tbfy():
    return render_template('general/tbfy.html')    


@general.route("/our_people", methods=['GET','POST'])  
#@cache.cached(timeout=50)   
def our_people():
    return render_template('general/our_people.html')

@general.route("/our_mission", methods=['GET','POST'])  
#@cache.cached(timeout=50)   
def our_mission():
    return render_template('general/our_mission.html')

@general.route("/our_history", methods=['GET','POST'])  
#@cache.cached(timeout=50)   
def our_history():
    return render_template('general/our_history.html')

@general.route("/your_role", methods=['GET','POST'])  
#@cache.cached(timeout=50)   
def your_role():
    return render_template('general/your_role.html')


  
@general.route("/featured_blogs", methods=['GET', 'POST']) 
@general.route("/featured_blogs/<int:limit>", methods=['GET', 'POST'])  
def featured_blogs(limit=5): 
    records = blog_data.query.order_by(blog_data.views.desc()).limit(limit).all()
    return render_template('general/featured_blogs.html', posts=records, reading_time=reading_time, count_likes=count_likes)


def reading_time(text): 
    return readtime.of_text(str(text)).text

ROWS_PER_PAGE=2
@general.route("/your_blogs", methods=['GET', 'POST'])  
def your_blogs(): 
    tags = Tag.query.with_entities(Tag.name).order_by(Tag.name).group_by(Tag.name).all()
    page = request.args.get('page', 1, type=int)
    records = blog_data.query.order_by(blog_data.category).paginate(page=page, per_page=ROWS_PER_PAGE)
    print(records.items)
    all_blogs = blog_data.query.order_by(blog_data.category).all()
    return render_template('general/your_blogs.html', title='All Blogs', posts=records, tags=tags,reading_time=reading_time, count_likes=count_likes, all_blogs = all_blogs)  


@general.route('/topic/<tag>')
@login_required
def topic(tag):
    try:
        topic = Tag.query.filter_by(name=tag).first()
    except:
        flash('Topic not found!','yellow')
        return redirect(url_for('general.your_blogs'))
    page = request.args.get('page', 1, type=int)
    records = topic.blogs.order_by(blog_data.category).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('general/your_blogs.html', title="#"+tag, posts=records,reading_time=reading_time, count_likes=count_likes) 


@general.route("/contact_us", methods=['GET','POST'])  
#@cache.cached(timeout=50)  
def contact_us():
    if request.method == 'POST':
        data = contact_us_data(name=request.form['name'], email=request.form['email'], message=request.form['message'])
        db.session.add(data)
        db.session.commit()
        return render_template('general/contact_us.html', thank=True)
    return render_template('general/contact_us.html', thank=False)


@general.route('/your_mates')
def writers():
    users = Profile.query.all()
    return render_template('/general/users.html',users=users)

@general.errorhandler(404)    #404 errorhandler
@cache.cached(timeout=300) 
def not_found(error):
  return render_template("404.html") 




  