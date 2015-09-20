import psycopg2

conn = psycopg2.connect("dbname='giant_db' user='giant_u' password='giant_pass'")

sql_create_table = """
    CREATE TABLE iptables 
    (
    user_id VARCHAR(12),
    ip_address VARCHAR(16),
    date timestamp,
    UNIQUE(user_id, ip_address)
    ) 
"""

def sql_iptables_by_user(user):
    return """
        SELECT ip_address 
        FROM iptables 
        WHERE user_id = {0} 
    """.format(user)

def sql_intersect_iptables(user1, user2):
    return """
        {0}
        INTERSECT 
        {1}
    """.format(sql_iptables_by_user(user1), sql_iptables_by_user(user2))

def sql_generate_iptable_item(user, ip,date):
    return """
        INSERT INTO iptables VALUES 
        (
        '{0}', '{1}', {2}
        )
    """.format(user, ip,date)
    
if __name__ == "__main__":
    cur = conn.cursor()
    cur.execute(sql_create_table)
    cur.fetchall()
    
