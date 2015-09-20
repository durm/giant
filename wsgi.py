import itertools
from flask import Flask, request, jsonify, g
from giant.db import get_db_connection, sql_intersect_iptables

def is_same_subnet(ip1, ip2):
    for p1, p2 in list(zip(ip1.split("."), ip2.split(".")))[:-1]:
        if p1 != p2:
            return False
    return True


def is_different_subnet(ip1, ip2):
    return not is_same_subnet(ip1, ip2)


application = Flask(__name__)
application.debug = True


@application.route("/interconnection/")
def interconnection():
    assert "user1" in request.args and "user2" in request.args, "Set users"
    conn = get_db_connection()
    user1 = request.args["user1"]
    user2 = request.args["user2"]
    
    cur = conn.cursor()
    cur.execute(sql_intersect_iptables(user1, user2))
    
    ips = [ip for ip in row for row in cur.fetchall()]
    conn.close()
    c = 0
    
    for ip1, ip2 in itertools.combinations(ips, 2):
        if is_different_subnet(ip1, ip2):
            c += 1
            if c == 2:
                return jsonify(user1=user1, user2=user2, interconnection=True)
    return jsonify(user1=user1, user2=user2, interconnection=False)


if __name__ == "__main__":
    application.run()
