from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, User, Post
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

# Create a Blueprint for our routes
main = Blueprint('main', __name__)

# Helper function for validation
def validate_request_data(data, required_fields):
    errors = {}
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f"{field} is required"
    return errors

###---------------- Homepage ----------------###
@main.route('/api/home', methods=['GET'])
def home():
    return render_template('home.html')

###---------------- User Routes ----------------###
@main.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)
    
    # users_pagination = User.query.paginate(page=page, per_page=per_page)

    # Set error_out=False to prevent 404 errors
    users_pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # If the page is out of range, redirect to the last available page
    if users_pagination.pages > 0 and page > users_pagination.pages:
        return redirect(url_for('main.get_users', page=users_pagination.pages, per_page=per_page))


    return render_template(
        'users.html',
        users=users_pagination.items,
        pagination=users_pagination,
        page=page
    )

@main.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "posts": [
            {
                "id": post.id,
                "title": post.title
            } for post in user.posts
        ]
    })


# Display form to create a new user
@main.route('/api/create_user_form', methods=['GET'])
def create_user_form():
    return render_template('create_user.html')

@main.route('/api/users', methods=['POST'])
def create_user():
    username = request.form.get('username')
    email = request.form.get('Email')

    data = { "username": username,
             "email": email
    }
    
    # Validate required fields
    errors = validate_request_data(data, ['username', 'email'])
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        db.session.add(new_user)
        db.session.commit()
        

        # Flash a success message that will be displayed after redirect
        flash("User created successfully")        
        return redirect(url_for('main.get_users'))

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/api/update_user_form', methods=['GET'])
def update_user_form():
    return render_template('update_user.html')

@main.route('/api/users/update_u', methods=['POST'])
def update_user():
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    user = User.query.get_or_404(user_id)

    data = { "user_id": user_id,
             "username": username
    }  

    try:
        if 'username' in data:
            user.username = data['username']
        # if 'email' in data:
        #     user.email = data['email']
            
        db.session.commit()
        flash("User updated successfully")        
        return redirect(url_for('main.get_users'))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
        
# @main.route('/api/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     user = User.query.get_or_404(user_id)
#     data = request.get_json()
    
#     try:
#         if 'username' in data:
#             user.username = data['username']
#         if 'email' in data:
#             user.email = data['email']
            
#         db.session.commit()
        
#         return jsonify({
#             "message": "User updated successfully",
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email
#             }
#         })
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400
#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({"error": "Username or email already exists"}), 400
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

@main.route('/api/delete_user_form', methods=['GET'])
def delete_user_form():
    return render_template('delete_user.html')

@main.route('/api/users/delete_u', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash("Post deleted successfully")        
        return redirect(url_for('main.get_users'))

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# @main.route('/api/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get_or_404(user_id)
    
#     try:
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({"message": "User deleted successfully"})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

###---------------- Post Routes ----------------###
@main.route('/api/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)
    
    # posts_pagination = Post.query.paginate(page=page, per_page=per_page)

    # Set error_out=False to prevent 404 errors
    posts_pagination = Post.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # If the page is out of range, redirect to the last available page
    if posts_pagination.pages > 0 and page > posts_pagination.pages:
        return redirect(url_for('main.get_posts', page=posts_pagination.pages, per_page=per_page))


    return render_template(
        'posts.html',
        posts=posts_pagination.items,
        pagination=posts_pagination,
        page=page
    )

@main.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at.isoformat(),
        "author": {
            "id": post.author.id,
            "username": post.author.username
        }
    })


# Display form to create a new post
@main.route('/api/create_post_form', methods=['GET'])
def create_post_form():
    return render_template('create_post.html')

@main.route('/api/posts', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = request.form.get('user_id')

    data = { "title": title,
             "content": content,
             "user_id": user_id
    }

    # Validate required fields
    errors = validate_request_data(data, ['title', 'content', 'user_id'])
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        new_post = Post(
            title=data['title'],
            content=data['content'],
            user_id=data['user_id']
        )
        db.session.add(new_post)
        db.session.commit()

        # Flash a success message that will be displayed after redirect
        flash("Post created successfully")        
        return redirect(url_for('main.get_posts'))

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/api/update_post_form', methods=['GET'])
def update_post_form():
    return render_template('update_post.html')

@main.route('/api/posts/update_p', methods=['POST'])
def update_post():
    post_id = request.form.get('post_id')
    title = request.form.get('title')
    title = title.strip()
    content = request.form.get('content')
    content = content.strip()

    data = { "title": title,
             "content": content,
             "post_id": post_id
    }

    try:
        post = Post.query.get_or_404(post_id)
    except Exception as e:
        return jsonify({"error": str(e)})
        
    try:
        if 'title' in data:
            if title:
                post.title = data['title']
        if 'content' in data:
            if content:
                post.content = data['content']
            
        db.session.commit()
        flash("Post updated successfully")        
        return redirect(url_for('main.get_posts'))

        # return jsonify({
        #     "message": "Post updated successfully",
        #     "post": {
        #         "id": post.id,
        #         "title": post.title,
        #         "content": post.content,
        #         "user_id": post.user_id
        #     }
        # })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/api/delete_post_form', methods=['GET'])
def delete_post_form():
    return render_template('delete_post.html')

@main.route('/api/posts/delete_p', methods=['POST'])
def delete_post():
    post_id = request.form.get('post_id')
    post = Post.query.get_or_404(post_id)
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully")        
        return redirect(url_for('main.get_posts'))

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# @main.route('/api/posts/<int:post_id>', methods=['DELETE'])
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
    
#     try:
#         db.session.delete(post)
#         db.session.commit()
#         return jsonify({"message": "Post deleted successfully"})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

# ---- Delete Duplicate Records In Posts Table
@main.route('/api/deleteDuplicates', methods=['DELETE'])
def deduplicate():
    delete_stmt = text("""
        DELETE FROM posts 
        WHERE id IN (
            SELECT p1.id
            FROM posts p1
            JOIN posts p2 ON p1.title = p2.title AND p1.content = p2.content
            WHERE p1.created_at > p2.created_at
        )
    """)

    result = db.session.execute(delete_stmt)
    db.session.commit()
    #print(f"Deleted {result.rowcount} duplicate rows.")
    return redirect(url_for('main.get_posts'))
    #return jsonify({"Deleted duplicate rows count":result.rowcount})


####-----------------------------------------------------------------------------------------
# Autocomplete routes
@main.route('/api/users/autocomplete', methods=['GET'])
def autocomplete_users():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    users = User.query.filter(User.username.like(f'%{query}%')).limit(10).all()
    return jsonify([{"id": user.id, "username": user.username} for user in users])

@main.route('/api/posts/autocomplete', methods=['GET'])
def autocomplete_posts():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    posts = Post.query.filter(Post.title.like(f'%{query}%')).limit(10).all()
    return jsonify([{"id": post.id, "title": post.title} for post in posts])

#---------------------------------------------------------------------------------------------------
# Display form to create a both new user and post!!!
@main.route('/api/create_user_post_form', methods=['GET'])
def create_user_post_form():
    return render_template('create_user_post.html')

@main.route('/api/user_and_post', methods=['POST'])
def create_user_and_post():
    username = request.form.get('username')
    email = request.form.get('email')
    title = request.form.get('title')
    content = request.form.get('content')

    data = { "username": username,
        "email": email,
        "title": title,
        "content": content
    }

    # Validate required fields
    errors = validate_request_data(data, ['username','email', 'title', 'content'])
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        db.session.add(new_user)
        db.session.flush()
        
        # Flash a success message that will be displayed after redirect
        flash("User created successfully")        

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    try:
        # # Check if user exists
        # user = User.query.get(new_user.id)
        # if not user:
        #     return jsonify({"error": "User not found"}), 404
        new_post = Post(
            title=data['title'],
            content=data['content'],
            user_id=new_user.id
        )
        db.session.add(new_post)
        db.session.commit()

        # Flash a success message that will be displayed after redirect
        flash("User and Post created successfully")        
        return redirect(url_for('main.get_posts'))

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Complex route for creating a user with multiple posts
@main.route('/api/users/with-posts', methods=['POST'])
def create_user_with_posts():
    data = request.get_json()
    
    if 'user' not in data or 'posts' not in data:
        return jsonify({"error": "Both user and posts data are required"}), 400
    
    # Validate user data
    user_errors = validate_request_data(data['user'], ['username', 'email'])
    if user_errors:
        return jsonify({"errors": {"user": user_errors}}), 400
    
    try:
        # Create the user
        new_user = User(
            username=data['user']['username'],
            email=data['user']['email']
        )
        db.session.add(new_user)
        db.session.flush()  # Assign ID without committing
        
        # Process posts
        created_posts = []
        for post_data in data['posts']:
            # Validate post data
            post_errors = validate_request_data(post_data, ['title', 'content'])
            if post_errors:
                db.session.rollback()
                return jsonify({"errors": {"posts": post_errors}}), 400
            
            # Create the post
            new_post = Post(
                title=post_data['title'],
                content=post_data['content'],
                user_id=new_user.id
            )
            db.session.add(new_post)
            created_posts.append(new_post)
        
        # Commit the transaction
        db.session.commit()
        
        return jsonify({
            "message": "User and posts created successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            },
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content
                } for post in created_posts
            ]
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
