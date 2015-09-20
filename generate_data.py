import random
from datetime import timedelta, datetime
from random import randint

def generate_datetime():
    start = datetime.now()
    return start + timedelta(
        seconds=randint(0, int((start - datetime(2014,1,1)).total_seconds())))

def generate_user_id():
    return "u_{0}".format(random.randint(1,100000))

def generate_ip():
    return "{0}.{1}.{2}.{3}".format(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    

if __name__ == "__main__":
    from giant.db import conn, sql_generate_iptable_item
    import sys
    
    try:
        c = int(sys.argv[1])
    except:
        c = 1000
        
    cur = conn.cursor()
    
    for i in range(c):
        cur.execute(sql_generate_iptable_item(generate_user_id(), generate_ip(), generate_datetime()))
