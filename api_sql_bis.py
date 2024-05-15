from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime
from flask import Flask,jsonify

db_string = "postgresql://root:root@localhost:5432/postgres"


app = Flask(__name__)
fake = Faker()
engine = create_engine(db_string)



@app.route("/user", methods=["GET"])
def get_users():
    users = run_sql_with_results("SELECT * FROM users")
    data=[]
    for row in users:
        user={
            "id":row[0],
            "firstname":row[1],
            "lastname":row[2],
            "age":row[3],
            "email":row[4],
            "job":row[5]

        }
        data.append(user)
    return jsonify(data)
    #return users

#CREATION DES TABLES

create_user_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    age INTEGER,
    email VARCHAR(200) ,
    job VARCHAR(100)
);
"""

create_application_table_sql = """
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(100),
    username VARCHAR(100),
    lastconnection TIMESTAMP WITH TIME ZONE,
    user_id INTEGER REFERENCES users(id)
);
"""

#FONCTIONS

def run_sql(query:str): #elle ne renvoie rien 
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(text(query))
        trans.commit() 

def run_sql_with_results(query:str): #elle renvoie un resultat, on utilise si on veut le résultat de la requete 
    with engine.connect() as connection:
        trans = connection.begin()
        result=connection.execute(text(query))
        trans.commit() 
        return result 

def populate_tables():
    apps=['Instagram', 'Facebook','TikTok','Twitter']
    for _ in range(100):
            firstname = fake.first_name() #valeur generer grace a faker
            lastname = fake.last_name()
            age = random.randrange(18, 50)
            email = fake.email()
            job = fake.job().replace("'","")
            #print(firstname, lastname, age, email, job)

            insert_user_query = f"""
                INSERT INTO users (firstname, lastname, age, email, job)
                VALUES ('{firstname}', '{lastname}', '{age}', '{email}', '{job}')
                RETURNING id
             """
            user_id = run_sql_with_results(insert_user_query).scalar()#bien utiliser la fonction avec with results
            #print(user_id) 
        
            #Create 1 up to 5 apps from the app list 
            num_apps = random.randint(1,5)
            for i in range(num_apps):
                username = fake.user_name()
                lastconnection = datetime.now()
                app_name= random.choice(apps)
                sql_insert_app = f"""
                    INSERT INTO applications (appname, username, lastconnection, user_id)
                    VALUES ('{app_name}','{username}','{lastconnection}','{user_id}')
                """

                run_sql(sql_insert_app)


            
if __name__ == '__main__':
    #create user table
    #run_sql(create_user_table_sql)
    #create application table
    #run_sql(create_application_table_sql)
    #populate_tables()

    app.run(host="0.0.0.0", port=8081, debug=True)




