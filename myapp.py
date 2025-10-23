from flask import Flask, render_template, session, request, redirect, url_for
request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask (__name__)

app.secret_key = '!@#$%'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'

mysql = MySQL(app)

#set route default dan http method yang diizinkan
@app.route('/', methods=['GET', 'POST'])
# function login
def login():
    #cek jika method POST dan ada form data maka proses login
    if request.method == 'POST' and 'inpEmail' in request.form \
    and 'inpPass' in request.form:
        #buat variabel untuk memudahkan pengolahan data
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        # cursor koneksi mysql
        cur = mysql.connection.cursor()
        #eksekusi kueri
        cur.execute("SELECT * FROM users where email = %s and \
        password = %s", (email, passwd))
        #fetch hasil kueri
        result = cur.fetchone()
        #cek hasil kueri
        if result:
            #jika login valid buat data session
            session['is_logged_in'] = True
            session['username'] = result[1]
            #Redirect ke halaman home
            return redirect(url_for('home'))
        else:
            #jika login invalid kembalikan ke login form
            return render_template('login.html')
    else:
        #jika method selain POST tampilkan form login
        return render_template('login.html')
    
@app.route('/home')
def home():
    # cek session apakah sudah login
    if 'is_logged_in' in session:
        # cursor koneksi mysql
        cur = mysql.connection.cursor()
        # eksekusi kueri
        cur.execute("SELECT * FROM users")
        # fetch hasil kueri
        data = cur.fetchall()
        # tutup koneksi
        cur.close()
        # render data bersama template
        return render_template('home.html', users=data)
    else:
        # jika belum login, redirect ke halaman login
        return redirect(url_for('login'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'inpUser' in request.form and 'inpEmail' in request.form and 'inpPass' in request.form:
        username = request.form['inpUser']
        email = request.form['inpEmail']
        passwd = request.form['inpPass']

        # Simpan ke database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, passwd))
        mysql.connection.commit()
        cur.close()

        # Setelah berhasil daftar, kembali ke halaman login
        return redirect(url_for('login'))

    # Kalau bukan POST, tampilkan form register
    return render_template('register.html')




# route logout
@app.route('/logout')
def logout():
    # hapus data session
    session.pop('is_logged_in', None)
    session.pop('username', None)
    # redirect ke halaman login
    return redirect(url_for('login'))

# debug dan auto reload
if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)