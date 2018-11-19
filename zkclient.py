from kazoo import client as kz_client
from collections import defaultdict

zkserver = 'host5:12181'
#'ubuntu202:2182'
my_client = kz_client.KazooClient(hosts=zkserver)


def getValue(instance, parent_path, zk_client):
    temp_p = parent_path + '/' + str(instance)
    if zk_client.exists(temp_p):
        job_instance = zk_client.get(temp_p + '/instance')
        print "===> ", job_instance[0]
        return job_instance[0]
    else:
        return ""


def my_listener(state):
    if state == kz_client.KazooState.CONNECTED:
        print("Client connected !")


my_client.add_listener(my_listener)
my_client.start(timeout=5)

#job-v1  (job in yoo)
#job  (job in yoo-job)
job_node = "job-v1"
data = my_client.get_children("/" + job_node)

ip_job_dict = defaultdict(list)


for job in data:
    print job
    #construct path
    p = '/' + job_node + '/' + job + '/' + 'sharding'
    if my_client.exists(p):
        ip_instance = getValue(0, p, my_client)
        if ip_instance: ip_job_dict[ip_instance].append(job)

        ip_instance = getValue(1, p, my_client)
        if ip_instance: ip_job_dict[ip_instance].append(job)

        ip_instance = getValue(2, p, my_client)
        if ip_instance: ip_job_dict[ip_instance].append(job)

print ip_job_dict
print {k: len(v) for (k, v) in ip_job_dict.items()}


