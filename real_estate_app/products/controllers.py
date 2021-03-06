from flask import Flask,Blueprint,render_template,flash,redirect,request,session
from real_estate_app.products.models import User,Product,City,Status,Type,Images
from real_estate_app.products.forms import RegisterForm,LoginForm,RegisterProduct
from real_estate_app import db
from flask_login import login_user,logout_user,login_required,current_user
products = Blueprint(__name__,'products')
from real_estate_app.products.utils import save_file

@products.route('/')
def all_products():
    all_types = Type.query.all()
    all_status = Status.query.all()
    all_cities = City.query.all()
    # if session.get("user_id"):
    #     user =User.query.filter_by(id=session.get("user_id")).first()
    all_products=Product.query.filter_by(is_published=True).all()
    users_id = session.get("user_id")
    if session.get("user_id") is None:
        auth_user = 'False'
    else:
        auth_user = 'True'
    context = {
        'auth_user':auth_user,
        'users_id':users_id,
        'all_products':all_products,
        'all_cities':all_cities,
        'all_types':all_types,
        'all_status':all_status

    }
    return render_template('core/main.html',**context)

@products.route('/register',methods=['GET','POST'])
def register():
    forms = RegisterForm()
    if forms.validate_on_submit():
        user = User(username=forms.username.data,email=forms.email.data,first_name = forms.first_name.data,
                    last_name=forms.last_name.data,phone_number=forms.phone_number.data,password=forms.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Succesfully registered,sign in please.')
        return redirect('/sign')
    context = {
        'forms': forms
    }
    return render_template('core/register.html',**context)

@products.route('/sign',methods=['GET','POST'])
def sign_in():
    forms = LoginForm()
    next_page = request.args.get('next','/')
    all_types = Type.query.all()
    all_status = Status.query.all()
    all_cities = City.query.all()
    all_products = Product.query.all()
    if request.method == 'POST' and forms.validate_on_submit():
        user = User.query.filter_by(username=forms.username.data).first()
        if user and user.check_password(forms.password.data):
            login_user(user)
            session['user_id']=user.id
            users_id = user.id
            flash('Logged in succesfully.')
            if user is None:
                auth_user='False'
            else:
                auth_user='True'
            context = {
                'all_types':all_types,
                'all_status':all_status,
                'all_cities':all_cities,
                'auth_user':auth_user,
                'users_id':users_id,
                'all_products':all_products
            }
            return render_template('core/main.html',**context)
        else:
            flash('User not found.')
    context = {
        'forms':forms,
    }
    return render_template('core/sign.html',**context)

@products.route('/logout')
@login_required
def logout():
    # user = User.query.filter_by(id=user_id).first()
    logout_user()
    if session.get('user_id'):
        del session['user_id']
    all_products = Product.query.all()
    all_types = Type.query.all()
    all_status = Status.query.all()
    all_cities = City.query.all()
    context = {
        'all_products':all_products,
        'all_types':all_types,
        'all_status':all_status,
        'all_cities': all_cities,
    }
    return render_template('core/main.html',**context)


ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@products.route('/create_product',methods=['GET','POST'])
@login_required
def create():
    forms = RegisterProduct()
    user_id=session.get("user_id")
    if session.get("user_id") is None:
        auth_user = 'False'
    else:
        auth_user = 'True'
    if request.method=='POST' and forms.validate_on_submit():
        if 'files[]' not in request.files:
            flash('No images loaded')
            return redirect(request.url)
        files = request.files.getlist('files[]')

        f = forms.image.data
        file_path = save_file(f)
        city_id=City.query.filter_by(title=forms.city_id.data.title).first().id
        type_id=Type.query.filter_by(title=forms.type_id.data.title).first().id
        status_id=Status.query.filter_by(title=forms.status_id.data.title).first().id
        product = Product(title=forms.title.data,description=forms.description.data,short_description = forms.short_description.data,
                    image=file_path,price=forms.price.data,is_published=forms.is_published.data,user_id=current_user.id,
                          city_id=city_id,type_id=type_id,status_id=status_id)
        for file in files:
            if file and allowed_file(file.filename):
                continue
            else:
                context = {
                    'image_error':'Format of images not supported',
                    'forms': forms
                }
                return render_template('core/create_product.html',**context)
        db.session.add(product)
        db.session.commit()
        for file in files:
            if file and allowed_file(file.filename):
                image_path = save_file(file)
                obj = Product.query.order_by(Product.id.desc()).first().id
                saved_image=Images(image=image_path,product_id=obj)
                db.session.add(saved_image)
                db.session.commit()
        flash('Succesfully created.')
        context={
            'users_id':user_id,
            'auth_user':auth_user
        }
        return redirect(f'/user_page/{user_id}')
    context = {
        'forms': forms,
        'auth_user':auth_user,
        'users_id':user_id
    }
    return render_template('core/create_product.html',**context)

@products.route('/user_page/<int:user_id>')
@login_required
def users_products(user_id):
    all_products = Product.query.filter_by(user_id=user_id)
    if session.get("user_id") is None:
        auth_user = 'False'
    else:
        auth_user = 'True'
    context = {
        'all_products':all_products,
        'auth_user':auth_user,
        'users_id':user_id
    }

    return render_template('core/user_page.html',**context)

@products.route('/detail/<int:id>')
def detail_view(id):
    user_id=session.get("user_id")
    product = Product.query.filter_by(id=id).first()
    images = Images.query.filter_by(product_id=product.id)[:6]
    if session.get("user_id") is None:
        auth_user = 'False'
    else:
        auth_user = 'True'
    context = {
        'product':product,
        'auth_user': auth_user,
        'users_id': user_id,
        'images':images
    }
    return render_template('core/detail.html',**context)

@products.route('/delete/<int:id>')
@login_required
def remove_product(id):
    user_id = session.get("user_id")
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted')
    return redirect(f'/user_page/{user_id}')

@products.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def change_product(id):
    product_info = Product.query.filter_by(id=id).first()
    forms = RegisterProduct(obj=product_info)

    user_id = session.get("user_id")
    if request.method=='GET':
        if session.get("user_id") is None:
            auth_user = 'False'
        else:
            auth_user = 'True'
        context = {
            'forms': forms,
            'product_id':product_info.id,
            'auth_user': auth_user,
            'users_id': user_id
        }
        return render_template('core/update.html', **context)
    else:
        files = request.files.getlist('files[]')
        f = forms.image.data
        file_path = save_file(f)
        city_id = City.query.filter_by(title=forms.city_id.data.title).first().id
        type_id = Type.query.filter_by(title=forms.type_id.data.title).first().id
        status_id = Status.query.filter_by(title=forms.status_id.data.title).first().id
        product_info.title=forms.title.data
        product_info.description=forms.description.data
        product_info.short_description=forms.short_description.data,
        product_info.image=file_path
        product_info.price=forms.price.data
        product_info.is_published=forms.is_published.data
        product_info.user_id=current_user.id
        product_info.city_id=city_id
        product_info.type_id=type_id
        product_info.status_id=status_id
        db.session.add(product_info)
        db.session.commit()
        for file in files:
            if file and allowed_file(file.filename):
                image_path = save_file(file)
                obj = product_info.id
                saved_image=Images(image=image_path,product_id=obj)
                db.session.add(saved_image)
                db.session.commit()
        # db.session.commit()
        return redirect(f'/user_page/{user_id}')


@products.route('/about')
def about_us():
    return render_template('core/about.html')

@products.route('/contacts')
def contacts():
    return render_template('core/contact.html')