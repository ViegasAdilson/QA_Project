from flask import Flask, render_template, redirect, url_for, flash, session, request
import mysql.connector
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '300922'
mydb = mysql.connector.connect(
    host="localhost",
    user="own",
    password="ownroot",
    database="agenda"
)

conn = mydb.cursor()


def save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(
        app.root_path, 'static/picture_files', picture_name)
    picture_file.save(picture_path)
    return picture_name


##################################### Forms #################################################


@app.route('/', methods=['GET', 'POST'])
def sign_page():
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['passwd']
        conn.execute(
            "SELECT * FROM users WHERE email = %s ", (email,))
        user_found = conn.fetchone()
        if user_found[3] == passwd:
            session['loggedin'] = True
            session['id'] = user_found[0]
            session['username'] = user_found[1]

            flash(
                f'Success! You are logged in as: {user_found[1]}', category='success')
            return redirect(url_for('list_page'))
        else:
            flash(
                f'Usename or password does not match', category='danger')
    if 'loggedin' in session:
        logged = True
    else:
        logged = False
    return render_template('index.html', logged=logged)


@app.route('/contacts', methods=['POST', 'GET'])
def list_page():
    conn.execute("SELECT * FROM contacts WHERE id_user = %s", (session['id'],))
    all_user = conn.fetchall()
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        description = request.form['description']
        image = request.files.get('picture', '')
        print(f'imagem {image}')
        conn.execute(
            "SELECT * FROM contacts WHERE email = %s or phone = %s", (email, phone,))
        fund_email = conn.fetchall()
        for existent in fund_email:
            if email in existent:
                email_found = True
            elif phone in existent:
                found_phone = True
        if email_found:
            flash(
                f'There is a contact with {email}, please try another email', category='danger')
        elif found_phone:
            flash(
                f'There is a contact with {phone}, please try another Phone Number', category='danger')
        else:
            if image != None:
                image_name = save_image(image)
            else:
                image_name = 'default.png'
            conn.execute("INSERT INTO contacts (name, surname, phone, email, address, description, picture, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                         (name, surname, phone, email, address, description, image_name, session['id']))
            mydb.commit()
            flash(f'User added successfuly', category='success')
            conn.execute(
                "SELECT * FROM contacts WHERE id_user = %s", (session['id'],))
            all_user = conn.fetchall()
            return redirect(url_for('list_page'))

    return render_template('list_page.html', name_user=session['username'], all_user=all_user)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        passwd = request.form['passwd']
        conn.execute(
            "INSERT INTO users (username, email, passwd) VALUES (%s, %s, %s)", (username, email, passwd))
        mydb.commit()

        return redirect(url_for('sign_page'))
    return render_template('register_page.html')


@app.route('/contacts/edit/<name_send>', methods=['GET', 'POST'])
def edit_contact(name_send):
    print(f'nome= {name_send}')
    conn.execute("SELECT * FROM contacts WHERE name = %s", (name_send,))
    user_fund = conn.fetchone()
    print(f'userencontrado {type(user_fund)}')
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        description = request.form['description']
        image = request.files.get('picture', '')

        if image != None:
            image_name = save_image(image)
        else:
            user_fund[7] = image_name
        conn.execute(
            "UPDATE contacts SET name = %s, surname = %s, phone = %s, email=%s, address=%s, description=%s, picture=%s WHERE id = %s", (name, surname, phone, email, address, description, image_name, user_fund[0]))
        mydb.commit()
        return redirect(url_for('list_page'))
    return render_template('edit_contact.html', user_fund=user_fund)


@app.route('/delete/<int:id>')
def delete_page(id):

    conn.execute("DELETE FROM contacts WHERE id = %s", (id,))
    mydb.commit()
    conn.execute(
        "SELECT * FROM contacts WHERE id_user = %s", (session['id'],))
    all_user = conn.fetchall()
    return render_template('list_page.html', all_user=all_user)


@app.route('/logout')
def logout_page():
    session.pop('loggedin', False)
    session.pop('id', None)
    session.pop('username', None)
    print(session)
    return redirect(url_for("sign_page"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
