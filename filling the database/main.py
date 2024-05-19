import psycopg2
from faker import Faker
import random
from datetime import datetime

DEFAULT_COUNT = 50

def get_ids(cursor, table_name, id_name):
    cursor.execute(f"select {id_name} from {table_name}")
    ids = cursor.fetchall()
    ids = [id[0] for id in ids]
    return ids

def get_ids_student(cursor):
    cursor.execute(f'''select user_id from users where status = 'student' ''')
    ids = cursor.fetchall()
    ids = [id[0] for id in ids]
    return ids

def get_ids_teacher(cursor):
    cursor.execute(f'''select user_id from users where status = 'teacher' ''')
    ids = cursor.fetchall()
    ids = [id[0] for id in ids]
    return ids

def get_ids_admin(cursor):
    cursor.execute(f'''select user_id from users where status = 'admin' ''')
    ids = cursor.fetchall()
    ids = [id[0] for id in ids]
    return ids
    
def get_status():
    status = ["student", "teacher"]
    i = random.randint(0,1)
    return status[i]

def get_group():
    i = random.randint(0,1)
    year = random.randint(19,24)
    group = random.randint(200, 545)
    res = "Б" + str(year) + "-" + str(group)
    return res

def fill_users(cursor):
    fake = Faker("ru_RU")
    users_count = 1120
    for i in range(users_count):
        user_id = str(i+1)
        if (i%10==0):
            status = "admin"
        else:
            status = get_status()
        mail = fake.unique.ascii_company_email()
        phone_number = (fake.country_calling_code() + fake.unique.msisdn())[:12]
        first_name = fake.name()
        passwrd = random.randint(10, 20)
        cursor.execute("""insert into users (
                        user_id,
                        passwrd,
                        status,
                        first_name,
                        phone_number,
                        mail
                        ) values (%s, %s, %s, %s, %s, %s)""",
                    (
                        user_id,
                        passwrd,
                        status,
                        first_name,
                        phone_number,
                        mail
                    ))
        
def fill_teacher(cursor):
    fake = Faker("ru_RU")
    users_count = 100
    ids = get_ids_teacher(cursor)
    for i in range(users_count):
        teacher_id = str(i+1)
        user_id = ids[random.randint(0, len(ids) - 1)]
        cursor.execute("""insert into teacher (
                        teacher_id,
                        user_id
                        ) values (%s, %s)""",
                    (
                        teacher_id,
                        user_id
                    ))
        
def fill_global_mark(cursor):
    fake = Faker("ru_RU")
    users_count = 1000
    for i in range(users_count):
        global_mark_id = str(i+1)
        mark = random.randint(0, 100)
        dates = fake.date_this_year()
        cursor.execute("""insert into global_mark (
                        global_mark_id,
                        mark,
                        dates
                        ) values (%s, %s, %s)""",
                    (
                        global_mark_id,
                        mark,
                        dates
                    ))

def fill_pz(cursor):
    fake = Faker("ru_RU")
    users_count = 1000
    for i in range(users_count):
        pz_id = str(i+1)
        state = fake.text()
        cursor.execute("""insert into pz (
                        pz_id,
                        state
                        ) values (%s, %s)""",
                    (
                        pz_id,
                        state
                    ))
        
def fill_rspz(cursor):
    fake = Faker("ru_RU")
    users_count = 1000
    for i in range(users_count):
        rspz_id = str(i+1)
        state = fake.text()
        cursor.execute("""insert into rspz (
                        rspz_id,
                        state
                        ) values (%s, %s)""",
                    (
                        rspz_id,
                        state
                    ))
        
def fill_works(cursor):
    fake = Faker("ru_RU")
    users_count = 1000
    ids_pz = get_ids(cursor, "pz", "pz_id")
    ids_rspz = get_ids(cursor, "rspz", "rspz_id")
    for i in range(users_count):
        work_id = str(i+1)
        pz_id = ids_pz[random.randint(0, len(ids_pz) - 1)]
        rspz_id = ids_rspz[random.randint(0, len(ids_rspz) - 1)]
        comm = fake.text()
        mark = random.randint(0, 100)
        cursor.execute("""insert into works (
                        work_id,
                        pz_id,
                        rspz_id,
                        comm,
                        mark
                        ) values (%s, %s, %s, %s, %s)""",
                    (
                        work_id,
                        pz_id,
                        rspz_id,
                        comm,
                        mark
                    ))

def fill_task(cursor):
    fake = Faker("ru_RU")
    users_count = 1000
    ids_mark = get_ids(cursor, "global_mark", "global_mark_id")
    ids_work = get_ids(cursor, "works", "work_id")
    for i in range(users_count):
        task_id = str(i+1)
        global_mark_id = ids_mark[random.randint(0, len(ids_mark) - 1)]
        work_id = ids_work[random.randint(0, len(ids_work) - 1)]
        state = fake.text()
        cursor.execute("""insert into task (
                        task_id,
                        global_mark_id,
                        work_id,
                        state
                        ) values (%s, %s, %s, %s)""",
                    (
                        task_id,
                        global_mark_id,
                        work_id,
                        state
                    ))
        
def fill_student(cursor):
    fake = Faker("ru_RU")
    users_count = 1000
    ids_user = get_ids_student(cursor)
    ids_teacher = get_ids(cursor, "teacher", "teacher_id")
    ids_task = get_ids(cursor, "task", "task_id")
    for i in range(users_count):
        student_id = str(i+1)
        user_id = ids_user[random.randint(0, len(ids_user) - 1)]
        teacher_id = ids_teacher[random.randint(0, len(ids_teacher) - 1)]
        task_id = ids_task[random.randint(0, len(ids_task) - 1)]
        number_group = get_group()
        
        cursor.execute("""insert into student (
                        student_id,
                        user_id,
                        teacher_id,
                        task_id,
                        number_group
                        ) values (%s, %s, %s, %s, %s)""",
                    (
                        student_id,
                        user_id,
                        teacher_id,
                        task_id,
                        number_group
                    ))
        
def fill_admin(cursor):
    fake = Faker("ru_RU")
    users_count = 20
    ids_user = get_ids_admin(cursor)
    for i in range(users_count):
        admin_id = str(i+1)
        user_id = ids_user[random.randint(0, len(ids_user) - 1)]
        cursor.execute("""insert into admins (
                        admin_id,
                        user_id
                        ) values (%s, %s)""",
                    (
                        admin_id,
                        user_id
                    ))

try:
    # connect to exist database
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="",
        database="postgres",
        port="5434"
    )
    
    connection.autocommit = True
    k = False
    i = 0
    with connection.cursor() as cursor:
        if (k == False):
            print (i); i+=1; fill_users(cursor)
            print (i); i+=1; fill_teacher(cursor)
            print (i); i+=1; fill_global_mark(cursor)
            print (i); i+=1; fill_pz(cursor)
            print (i); i+=1; fill_rspz(cursor)
            print (i); i+=1; fill_works(cursor)
            print (i); i+=1; fill_task(cursor)
            print (i); i+=1; fill_student(cursor)
            print (i); i+=1; fill_admin(cursor)
        else:
            #TODO 
            print()
            

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
else:
    if connection:
        # cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")