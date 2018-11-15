# elucidata-assignment
Data analytics assignment

#### Steps to run the project.

1. Clone the repository
2. `python3 manage.py migrate`
3. `python3 manage.py runserver`

### Endpoints:

**1. Upload the test data:**

**_Request_:**

POST `localhost:8000/api/v1/analytics/upload`

BODY  `form-data containing two fields name and file`

**_Response_:**
```
{
    "id": 4,
    "name": "analytics_data",
    "created": "2018-11-13T04:53:55.832983Z",
    "modified": "2018-11-13T04:53:55.833049Z",
    "file": "media/mass_spec_data_assgnmnt_ccshVgE.xlsx"
}
```



**2. Perform task 1:**

**_Request_:**

GET `localhost:8000/api/v1/analytics/process/task1`

**_Response_:**
```
File containing processed output.
```


**2. Perform task 2:**

**_Request_:**

GET `localhost:8000/api/v1/analytics/process/task2`

**_Response_:**
```
File containing processed output.
```
