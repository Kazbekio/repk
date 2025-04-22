import psycopg2
import csv
conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "postgres123",
    host = "127.0.0.1",
    port = "5432"
)
curr = conn.cursor()

menu = '''
1. Inserting data from file: 
2. Entering user name, phone from console: 
3. Update:  
4. Search: 
5. Delete: 
'''
print(menu)
n = int(input("Введите номер запроса: "))

if n == 1:
    st = str(input("Which file: "))
    with open(f"{st}.csv", 'r') as f:
        rd = csv.DictReader(f)
        for row in rd:
            try:
                print(row)
                curr.execute(
                    "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                    (row['first_name'], row['last_name'], row['phone_number'])
                )
                conn.commit()
            except Exception as m:
                print(f"Ошибка: {m}")

elif n == 2:
    name = input("Enter first name: ")
    last_name = input("last name: ")
    phone = input("Enter phone number: ")   
    try:
        curr.execute(
            "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
            (name, last_name , phone)
        )
        conn.commit()
        print("OK!!!")
    except Exception as m:
        print(f"Ошибка: {m}")
elif n == 3:
    choice = '''
        1. Имя по номеру телефона
        2. Номер телефона по имени
    '''
    print(choice)
    q = int(input("Введите номер запроса: "))
    if q == 1:
        ph = input("Ваш номер телефона: ")
        n_name = input("Новое имя: ")
        curr.execute(
            "UPDATE phonebook SET first_name = %s WHERE phone_number = %s", (n_name, ph)
        )
        conn.commit()
    elif q == 2:
        name = input("Введите имя: ")
        ph = input("Введите новый номер телефона: ")
        curr.execute(
            "UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (ph, name)
        )
        conn.commit()
    else:
        print("Ошибка!")
elif n == 4:
    pt = input("Введиту имя или же номер: ")
    curr.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone_number ILIKE %s", (f"%{pt}%", f"%{pt}%")
    )
    rw = curr.fetchall()
    if rw:
        for row in rw:
            print(row)
    else:
        print("Ничего не найдено")
elif n == 5:
    choice = '''
        1. Удалить по имени
        2. Удалить по номеру телефонa
    '''
    print(choice)
    q = int(input("Введите свой выбор: "))
    if q == 1:
        name = input("Введите имя: ")
        curr.execute(
            "DELETE FROM phonebook WHERE first_name = %s", (name,)
        )
    elif q == 2:
        ph = input("Введите номер телефона: ")
        curr.execute(
            "DELETE FROM phonebook WHERE phone_number = %s", (ph,)
        )
    conn.commit()
    print("OK!")
curr.close()
conn.close()


# curr.execute("create table phonebook(""id SERIAL PRIMARY KEY, first_name VARCHAR(50) NOT NULL, last_name VARCHAR(50) NOT NULL, phone_number INT NOT NULL)")
# conn.commit()