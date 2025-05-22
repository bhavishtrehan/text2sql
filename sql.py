import sqlite3

connection = sqlite3.connect('inventory.db')

cursor = connection.cursor()

table_info = '''
CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    supplier_name VARCHAR(100),
    stock_quantity INT,
    purchase_price DECIMAL(10, 2)
);
'''

cursor.execute(table_info)


cursor.execute('''
INSERT INTO inventory (product_id, product_name, category, supplier_name, stock_quantity, purchase_price)
VALUES
(1, 'Rice', 'Food', 'XYZ Suppliers', 50, 40.00),
(2, 'Toothpaste', 'Toiletries', 'ABC Goods', 150, 30.00),
(3, 'Sugar', 'Food', 'Sweet Suppliers', 75, 25.00),
(4, 'Salt', 'Food', 'Salty Co.', 60, 12.00),
(5, 'Milk Powder', 'Beverages', 'Milk Corp', 80, 200.00),
(6, 'Tea', 'Beverages', 'Tea Traders', 100, 50.00),
(7, 'Cooking Oil', 'Food', 'Oil Suppliers', 40, 120.00),
(8, 'Biscuits', 'Food', 'Snacky Foods', 120, 30.00),
(9, 'Shampoo', 'Toiletries', 'Beauty Care Ltd.', 90, 60.00),
(10, 'Detergent', 'Toiletries', 'Clean Solutions', 110, 80.00);
''')


print('the inserted records are')

data = cursor.execute('''SELECT * FROM inventory''')

for row in data:
    print(row)

connection.commit()
connection.close()