import itertools
from flask import Flask, request, jsonify
from giant.db import conn

def is_same_subnet(ip1, ip2):
    for p1, p2 in zip(ip1.split("."), ip2.split("."))[:-1]:
        if p1 != p2:
            return False
    return True


def is_different_subnet(ip1, ip2):
    return not is_same_subnet(ip1, ip2)


application = Flask(__name__)


@application.route("/")
def interconnections():
    assert "user1" in request.args and "user2" in request.args, "Set users"
    user1 = request.args["user1"]
    user2 = request.args["user2"]
    ip1 = None
    cur = conn.cursor()
    cur.execute(db.sql_intersect_iptables(user1, user2))
    for row in cur.fetchall():
        nip = row[0]
        if ip1 is not None:
            if is_different_subnet(ip1, nip):
                return jsonify(user1=user1, user2=user2, interconnection=True)
        else:
            ip1 = nip
    return jsonify(user1=user1, user2=user2, interconnection=False)


if __naime__ == "__main__":
    application.run()
