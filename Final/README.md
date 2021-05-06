# Shelttered Homeless App

The API allows for user to get specific data perteining to individuals experiencing sheltered homelessness in the Austin/Travis County Continuum of Care from 2016 to 29019. 

## User documentation


## Deploying Kubernetes
Kuberenetes was made available in two enviorments, test and production (prod). To launch everything from your isp machine the following commands need to be made. It is important that they are done in the following order as the api and worker deployment, need the redis service IP adress to properly run. 

To launch the test enviorment run the following commands: 
 
`kubectl apply -f shelttered-homeless-test-db-service.yml`

`kubectl apply -f shelttered-homeless-test-db-deployment.yml`

`kubectl apply -f shelttered-homeless-test-db-pvc.yml`

You must find the `shelttered-homeless-test-db-service` `CLUSTER-IP` to hardcode into the api and worker deployment. To do  so run the following command: 

`kubectl get services`

Copy the `CLUSTER-IP` of the `shelttered-homeless-test-db-service`, vim into `shelttered-homeless-test-api-deployment.yml` and `shelttered-homeless-test-wrk-deployment.yml` yml files. Paste IP address in the `value` of the `name: REDIS_IP` variable.

To finalize launch of the test enviorment run the following comnads:

`kubectl apply -f shelttered-homeless-test-api-deployment.yml`

`kubectl apply -f shelttered-homeless-test-api-service.yml`

`kubectl apply -f shelttered-homeless-test-wrk-deployment.yml`

Follow the same steps for the production enviorment this time `kubectl apply -f` the following yml files:

`shelttered-homeless-prod-db-service.yml`

`shelttered-homeless-prod-db-deployment.yml`

`shelttered-homeless-prod-db-pvc.yml`


`shelttered-homeless-prod-api-deployment.yml`

`shelttered-homeless-prod-api-service.yml`

`shelttered-homeless-prod-wrk-deployment.yml`



## Interacting With Routes
Once the enviorments have been launch you must exec into the api pod. To do so, run the following commands: 

`kubeclt get pods`

Find the production api  pod `shelttered-homeless-prod-api-deployment-649554dbc7-678hm` and exec into the pod.

`kubectl exec -it  shelttered-homeless-prod-api-deployment-649554dbc7-678hm  -- /bin/bash`

Keep in mind that the numbers at the end of the pod name will differ. 

Once you are inside the 'shelttered-homeless-prod-api-deployment' pod, you can curl each of the following routes and get a requested result.

# Available Routes 

```
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
```

When interacting with the API, these are the routes available do the following command:

- For `/`
  `curl localhost:5000/`
  The route will return the different routes avilable, displayed like thyhave been displayed above.

- For `/reset`
  `curl localhost:5000/reset`
  This route will populate the redis database with the data from the Austin/Travis County Continuum of Care dataset. IT IS EXTREMELY IMPORTANT that this route is run before posting a job. If not done so, posted job will remain in 'status: creating' forever.    

- For `/run`
  `curl localhost:5000/run`
  The route will return instructions on how to POST a command to the queue. It will provide correct sintax for each of the variables and how to curl the jobs post. It is importnat that the variables inputed for the job post are exactly as provided in the instructions, as the program will not work if done otherwise.

The way the dataset is set up is too complex to add routes that can CREATE DELETE or UPDATE information of the dataset. Therefore, I have chosen for created deleted or updated modifications to be done on my jobs database. ie. Instead of adding a count of a homeless person for a given year to the County Continuum of Care data set. I will add a job to the database of jobs. Consequently deleting or being able to update it. (To fullfil the CRUD requierment)

- For `/run/<stats>/<specific_stat>` (CREATE A JOB)
  `curl -X POST localhost:5000/run/Race/Black_or_African_American`
  The route will submit to the queue the requested job and returnthe following statement.
  `Job 8386a0f4-a40c-4385-a9ed-bac995016590 submitted to the queue`

- For  `/get_data` (READ DATASET)
  `curl localhost:5000/get_data`
  The route will return a JSON with the complete dataset of the County Continuum of Care.

- For `/jobs` (READ ALL JOBS)
  `curl localhost:5000/jobs`
  The route will return a jSON with all the jobs previously submitted, the date created and their status.
  ```
   {
    "8386a0f4-a40c-4385-a9ed-bac995016590": {
        "datetime": "2021-05-06 10:33:34.782900",
        "stats": "Race",
        "specific stat": "BlCack or African American",
        "status": "creating"
    },
    "99f1fe2d-ccfa-4b35-acbb-6e3a15c05595": {
        "datetime": "2021-05-06 10:46:02.866560",
        "stats": "Race",
        "specific stat": "BlCack or African American",
        "status": "creating"
    } ```

- For `/update/<UUID>/<stats>/<specific_stat>` (UPDATE A JOB)  
  `curl localhost:5000/update/99f1fe2d-ccfa-4b35-acbb-6e3a15c05595/Race/Asian`
  The route will update a spcific job. If the job has already been finished or is being created, it will not be updated as doing so will cause errors in the worker.py code. Instead the user is asked to delete and post another job with the new parameters.

- For `/delete` (DELETE A JOB)
  `curl -X DELETE -d "jobid=99f1fe2d-ccfa-4b35-acbb-6e3a15c05595" localhost:5000/delete`
  The route will delete a requested job from the jobs database ie. db=1
  `Job 99f1fe2d-ccfa-4b35-acbb-6e3a15c05595 deleted`

- For `/jobs/<UUID>`
  `curl localhost:5000/jobs/99f1fe2d-ccfa-4b35-acbb-6e3a15c05595`
  The route will return the job status and if it is ready for the image to download.
  ```
  {
    "status": "finished",
    "image": "ready"
  }
  ```

- For `/download/<UUID>`
  `curl localhost:5000/download/99f1fe2d-ccfa-4b35-acbb-6e3a15c05595`
  Route will return an image that graphically represents the change in count of shelttered homeless people assited by Austin/Travis County Continuum of Care from 2016 to 2019, for the given parameter. 




