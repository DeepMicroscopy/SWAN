# Overview Usecase Tasks

Six use cases were identified, each associated with one or more tasks.
The tasks for each use case are described below.

## UC: 1. Manage Users

The researcher creates, manages and deletes users.
UI: SWAN-Admin

| No | Task                    | Description                                                                             | View        | Status |
|----|-------------------------|-----------------------------------------------------------------------------------------|-------------|--------|
| 1  | Login as an admin       | Database, Login and show Home-View                                                      | Login, Home | done   |
| 2  | Send emails to user     | Mailing-System (Emails have to be delivered within a minute)                            | None        | open   |
| 3  | Create Role             | Authenticated as an admin, create a role,                                               | Home, User  | done   |
| 4  | Create User             | Authenticated as an admin, create a user (with email).<br/>Menu point at the app: Users | Home, User  | done   |
| 5  | Assign a Role to a User | Authenticated as an admin, assign/delete a role to/from a (new) user.                   | Home, User  | done   |
| 6  | Delete User             | Authenticated as an admin, delete a user.                                               | Home, User  | done    |
|    |                         |                                                                                         |             |        |


## UC: 2. Upload Data

The researcher uploads a dataset without labels.
UI: SWAN-Admin

| No | Task                       | Description                                          | View        | Status |
|----|----------------------------|------------------------------------------------------|-------------|--------|
| 1  | Login as a researcher      | Login and show Home-View                             | Login, Home | open   |
| 2  | Create a named dataset     | Create a named dataset at the Data-View              | Home, Data  | open   |
| 3  | Upload data to a dataset   | Choose a dataset and upload single files or archives | Home, Data  | open   |
| 4  | Delete data from a dataset | Choose a dataset and delete data                     | Home, Data  | open   |
|    |                            |                                                      |             |        |

## UC: 3. Create study

The researcher creates a study.
UI: SWAN-Admin

| No | Task               | Description                                                        | View          | Status |
|----|--------------------|--------------------------------------------------------------------|---------------|--------|
| 1  | Create a new study | Create a new Study from a dataset and set labels                   | Home, Studies | open   |
| 2  | Publish a study    | Choose a study and a group of experts (roles) to publish the study | Studies       | done   |
|    |                    |                                                                    |               |        |

## UC: 4. Manage study

The researcher changes or ends a study
UI: SWAN-Admin

| No | Task                          | Description                                                                                                                               | View    | Status |
|----|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|---------|--------|
| 1  | Manage a study                | Choose a study and change the dataset or the labels                                                                                       | Studies | open   |
| 2  | Created a QR-Code for a study | Choose a study and create a QR-Code to share the study for anonymous users<br/>One QR-Code for every study and a random id for every user | Studies | open   |
| 3  | Ended a study                 | Choose a study and ended the study                                                                                                        | Studies | open   |
| 4  | Delete a study                | Choose a study and delete the study                                                                                                       | Studies | done   |
|    |                               |                                                                                                                                           |         |        |

## UC: 5. Participate in Study

Experts label data per Smartphone
UI: SWAN-App (Browser)

| No | Task                                    | Description                                                                                        | View             | Status |
|---|-----------------------------------------|----------------------------------------------------------------------------------------------------|------------------|--------|
| 1 | Login as a User                         | Open the SWAN-App and login                                                                        | Login, Home      | open   |
| 2 | Overview                                | Shows the homepage with a overview of the studies                                                  | Home             | open   |
| 3 | Participate in study as registered user | Choose a study from the overview and start the study<br/>Remembered the last viewed picture        | Home, SwipeStudy | open   |
| 4 | Participate in study as anonymous user  | Scan the QR-Code and start the study as an anonymous user                                          | SwipeStudy       | open   |
| 5 | Analyze the picture                     | Swipe left, right, top, bottom to make a decision for the shown picture                            | SwipeStudy       | done   |
| 6 | Navigate during the study               | Navigate back to undo a decision, close the study or press help for information about the controls | SwipeStudy       | done   |
| 7 | Send Data to Database                   | The data entered by the user must be stored in a table in the database                             | None             | open   |
|   |                                         |                                                                                                    |                  |        |

## UC: 6. Export data

The researcher exports data
UI: SWAN-Admin

| No | Task                      | Description                                  | View    | Status |
|----|---------------------------|----------------------------------------------|---------|--------|
| 1  | Export data from a study  | Choose a study and export data as a download | Studies | open   |
|    |                           |                                              |         |        |