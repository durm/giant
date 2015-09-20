import itertools
from flask import Flask, request, jsonify, g
from giant.db import get_db_connection, sql_intersect_iptables
import time

def is_same_subnet(ip1, ip2):
    for p1, p2 in list(zip(ip1.split("."), ip2.split(".")))[:-1]:
        if p1 != p2:
            return False
    return True


application = Flask(__name__)
application.debug = True


@application.route("/interconnection/")
def interconnection():

    user1 = request.args["user1"]
    user2 = request.args["user2"]
    
    start = time.time()
    conn = get_db_connection()
    
    cur = conn.cursor()
    cur.execute(sql_intersect_iptables(user1, user2))
    
    ips = [ip for row in cur.fetchall() for ip in row]
    
    conn.close()
    
    resp = {
        "user1": user1,
        "user2": user2,
        "interconnection": not all(map(lambda p: is_same_subnet(*p), itertools.combinations(ips, 2))),
        "duration": time.time() - start
    }
    return jsonify(resp)


if __name__ == "__main__":
    application.run()
