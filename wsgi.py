import itertools

def is_same_subnet(ip1, ip2):
    for p1, p2 in zip(ip1.split("."), ip2.split("."))[:-1]:
        if p1 != p2:
            return False
    return True

def is_different_subnet(ip1, ip2):
    return not is_same_subnet(ip1, ip2)

def get_interconnections(ips1, ips2):
    return filter(is_different_subnet, itertools.combinations(set(ips1).intersection(set(ips2)), 2))

def is_interconnected(interconnections):
    return len(interconnections) >= 2

def get_speed(ips):
    return ips[0] == ips[1]

def get_max_speed(interconnections):
    return max(map(get_speed, interconnections))

print (is_one_subnet("1.2.4.4","1.2.4.5"))
