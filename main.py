from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)

import mysql.connector 

HOST = 'localhost'
DATATBASE = 'shop'
USER = 'root'
PASSWORD = os.environ.get('PW')

print(PASSWORD)
db_connection = mysql.connector.connect(
    host = HOST,
    database = DATATBASE,
    user = USER,
    password = PASSWORD
    )
print('connected to ', db_connection.get_server_info())

cursor = db_connection.cursor()


@app.route('/')
def main():
    print('sadfjhdsaf;lsdah')
    cursor.execute(
        """
        SELECT * FROM products;
        """
    )
    items = cursor.fetchall()
    cursor.execute(
        """
        SELECT * FROM records;
        """
    )
    records = cursor.fetchall()
    print(items, records)
    return render_template('index.html', items = items, records = records)

@app.route('/item/<product>')
def product(product):
    # show this in the page
    cursor.execute(
        f"""
        SELECT products.prod_name, products.price, SUM(records.quantity) as sold
        FROM products	
        LEFT JOIN records
        ON products.prod_id = records.prod_id
        WHERE products.prod_name = '{product}'
        GROUP BY products.prod_id ;
        """
        )
    item = cursor.fetchall()
    print('result is: ',item)
    if cursor.rowcount == 0:
        return render_template('404.html', name =product)
    else:
        return render_template('product.html', item = item[0],) 



if __name__ == "__main__":
    app.run(debug=True)