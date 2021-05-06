from datetime import datetime
from flask import Flask, request, send_file
import json
from hotqueue import HotQueue
import redis
import os
from uuid import uuid4


redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()


app = Flask(__name__)
rd = redis.StrictRedis(host=redis_ip, port=6379, db=1)
rd_dataset = redis.StrictRedis(host=redis_ip, port=6379, db=0, decode_responses=True)
q = HotQueue('queue', host=redis_ip, port=6379, db=2)


@app.route('/', methods=['GET'])
def instructions():
    return """
    Try these routes:
    
    /                                       informational
    /run                                    (GET) job instructions
    /run/<stats>/<specific_stat>            (POST) submit job
    /jobs                                   get list of past jobs
    /jobs/<UUID>                            get job status
    /delete                                 (GET) delete instructions
    /delete                                 (DELETE) delete job
    /download/<UUID>                        download img from job 
    /reset                                  resets data in dataset
    /get_data                               get all data in dataset
    /update/<UUID>/<stats>/<specific_stat>  update iputs in job           
"""

@app.route('/run', methods=['GET'])
def run_job():
    return """
    This is a route for posting a job.
    Job will requiere inputs:
     - <stats>: may be any of the following stats: 
                   - Race
                   - Ethnicity
                   - Gender
                   - Veteran_Status
                   - Age_Category
                   - Disability_Status
     
     - <specific_stat>: depending on the chosen stats variable, specific_stat maybe any of the following: 
                   - For Race:
                     - American_Indian_or_Alaskan_Native
                     - Asian
                     - Black_or_African_American
                     - Native_Hawaiian_or_Other_Pacific_Islander
                     - White
                     - Unknown
                   - For Ethnicity:
                     - Hispanic_Latino
                     - Non-Hispanic_Non-Latino
                     - Unknown
                   - For Gender:
                     - Female
                     - Male
                     - Trans_Female
                     - Trans_Male
                     - Gender_Non-Conforming
                     - Unknown
                   - For Veteran_Status:
                     - Veteran
                     - Not_a_Veteran
                     - Unknown
                   - For Age Category:
                     - Adult_25-61                     
                     - Adult_18-24
                     - Elder_Adult_62+
                     - Children
                     - Unknown                  
                   - For Disability_Status:
                     - Has_a_Disabling_Condition
                     - Does_Not_Have_a_Disabling_Condition
                     - Unknown

    Use the form:
    curl -X POST localhost:5011/run/<stats>/<specific_stats>
    The once completed the job will return a graphic interpretation of how the total count of 
    homeless clients that where categorized in the chosen specif_stat changed from 2016-2019 
"""


@app.route('/run/<stats>/<specific_stat>', methods=['POST'])
def run_job_stats(stats,specific_stat):
   this_uuid = str(uuid4()) 
   
   this_specific_stat = str(specific_stat)
   if(this_specific_stat == 'Hispanic_Latino' or this_specific_stat == 'Non-Hispanic_Non-Latino' ):
      this_specific_stat = this_specific_stat.replace('_', '/')
   else:
     this_specific_stat = this_specific_stat.replace('_', ' ')
   
   this_stats = str(stats)
   this_stats = this_stats.replace('_', ' ')
   
   data = { 'datetime': str(datetime.now()),
            'status': 'submitted',
            'stats': this_stats,
            'specific stat': this_specific_stat}
   rd.hmset(this_uuid, data)
   q.put(this_uuid)
   return f'Job {this_uuid} submitted to the queue\n'


@app.route('/delete', methods=['GET', 'DELETE'])
def delete_job():

    if request.method == 'DELETE':
        this_jobid = str(request.form['jobid'])
        rd.delete(this_jobid)
        return f'Job {this_jobid} deleted\n'

    else:
        return """
    This is a route for DELETE-ing former jobs. Use the form:
    curl -X DELETE -d "jobid=asdf1234" localhost:5011/delete
    Where the jobid "asdf1234" is what you want to delete.
"""


@app.route('/jobs', methods=['GET'])
def get_jobs():
    redis_job_dict = {}
    for key in rd.keys():
        redis_job_dict[str(key.decode('utf-8'))] = {}
        redis_job_dict[str(key.decode('utf-8'))]['datetime'] = rd.hget(key, 'datetime').decode('utf-8')
        redis_job_dict[str(key.decode('utf-8'))]['stats'] = rd.hget(key, 'stats').decode('utf-8')
        redis_job_dict[str(key.decode('utf-8'))]['specific stat'] = rd.hget(key,'specific stat').decode('utf-8')
        redis_job_dict[str(key.decode('utf-8'))]['status'] = rd.hget(key, 'status').decode('utf-8')
    return json.dumps(redis_job_dict, indent=4)


@app.route('/jobs/<jobuuid>', methods=['GET'])
def get_job_status(jobuuid):
    bytes_job_dict = rd.hgetall(jobuuid)
    final_dict = {}
    for key, value in bytes_job_dict.items():
        if key.decode('utf-8') == 'status':
            final_dict[key.decode('utf-8')] = value.decode('utf-8')   
        if key.decode('utf-8') == 'image':
            final_dict[key.decode('utf-8')] = 'ready'
    return json.dumps(final_dict, indent=4)


@app.route('/download/<jobuuid>', methods=['GET'])
def download(jobuuid):
    path = f'/app/{jobuuid}.png'
    with open(path, 'wb') as f:
        f.write(rd.hget(jobuuid, 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)

@app.route('/reset', methods =['GET'])
def reset():
   with open('dataset.json', 'r') as data:
      years_data = json.load(data)
   
   for key, value in years_data.items():
      rd_dataset.set(key, json.dumps(value))
   return('data base reset')

@app.route('/get_data', methods=['GET'])
def get_data():
   data_dict= {}
   years = ['2016','2017','2018','2019']
   for i in years:
       dataset_byte = json.loads(rd_dataset.get(i))
       data_dict[i] = dataset_byte

   return data_dict

@app.route('/update/<UUID>/<stats>/<specific_stat>', methods=['GET'])
def update_job(UUID,stats,specific_stat):
   specific_stat = str(specific_stat)
   if(specific_stat == 'Hispanic_Latino' or specific_stat == 'Non-Hispanic_Non-Latino' ):
      specific_stat = specific_stat.replace('_', '/')
   else:
     specific_stat = specific_stat.replace('_', ' ')

   stats = str(stats)
   stats = stats.replace('_', ' ')
   UUID = str(UUID)
   if(rd.hget(UUID, 'status').decode('utf-8') == 'submitted'):
      rd.hset(UUID,'stats', stats)
      rd.hset(UUID, 'specific stat', specific_stat)
      rd.hset(UUID,'status', 'resubmitted')
      q.put(UUID)  
      return f'job {UUID} updated and resubmitted\n'

   else: 
      return f'job {UUID} has already been processed or is being processed, delete job and request a new job with desired inputs\n'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
