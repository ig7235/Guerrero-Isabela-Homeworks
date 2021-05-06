from hotqueue import HotQueue
import json
import os
import redis
import matplotlib.pyplot as plt
import subprocess


redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()


rd = redis.StrictRedis(host=redis_ip, port=6379, db=1, decode_responses=True)
rd_dataset = redis.StrictRedis(host=redis_ip, port=6379, db=0, decode_responses=True)
q = HotQueue('queue', host=redis_ip, port=6379, db=2)


@q.worker
def run_job(job):

    subprocess.run(["sleep 1"], shell=True, check=True)
    
    # change job status in db=1 to 'creating'
    rd.hset(job, 'status', 'creating')

    # get data from job info in db=1
    data_byte= rd.hgetall(job)
    this_stats = ''
    this_specific_stat = ''
    for key, value in data_byte.items():
        if key == 'stats':
            this_stats = value
        elif key == 'specific stat':
            this_specific_stat = value
    
    # get requested data from data set
    years = [2016,2017,2018,2019]
    # loop through dataset to find desired stats and after look through 
    # stats to find value of 'Total Unduplicated Clients' of specific stat  
    total_count_stat = []
    for i in years:
        dataset_byte = json.loads(rd_dataset.get(str(i)))
        for key, value in dataset_byte.items():
            if key == this_stats:
               for key2, value2 in value.items():
                   if key2 == this_specific_stat:
                       for key3, value3 in value2.items():        
                           if key3  == 'Total Unduplicated Clients':
                               total_count_stat.append(value3)
    
    # verify that all members of total_count_stat list are ints                  
    for i in range(len(total_count_stat)):
        total_count_stat[i] = int(total_count_stat[i])
    ylabel = f'Total count of homeless {this_specific_stat} '
    title = f'Change of Count In {this_specific_stat} Sheltered Homeless'
    
    # create plot with gathered data
    plt.plot(years,total_count_stat)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.title(title) 
     
    plt.savefig('/output_image.png')
    with open('/output_image.png', 'rb') as f:
       img = f.read()

    rd.hset(job, 'image', img)
    rd.hset(job, 'status', 'finished')
    

    
    return


run_job()
