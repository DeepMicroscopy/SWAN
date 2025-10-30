# User Guide

## Admin

Visit the admin dashboard by logging in at `/admin/`.

### Creating Users and Groups

If the study should be limited to a specific group of users, you first need to create a group under
`Authentication and Authorization` -> `Groups`.
Click `Add Group` and enter a name for the group. You don't need to assign any permissions.

Under `App` -> `Users` you can create accounts for known participants.
Click `Add User` and enter a username and password. Once you are done, you can edit this user to fill in more details.

Edit the user by clicking on the username and assign the desired groups, if any.

### Configuring the UI

Under `App` -> `Uis` click `Add`. There will be example / default values for the configuration.
Configure the four directions `up` / `down` / `left` / `right` by adding them as keys to the Labels.

Each direction supports these settings:

- `text`: The text to display when swiping
- `icon`: The icon to display when swiping
    - https://pictogrammers.com/library/mdi/
- `color`: The color of the icon
    - https://vuetifyjs.com/en/styles/colors/#material-colors
- `label`: The label to include in the export

You can optionally select one of the configured directions as the `postpone` direction.
Images swiped in this direction will be shown again at the end of the dataset until none are left that have been swiped
in this direction.

If you have tiny images / low resolution, you can configure image pixelation and the default zoom level in percent.

### Uploading a Dataset

Under `App` -> `Datasets` click `Add`. Select a title and the archive file.
Supported formats are `.zip` and `.tar.*`. After the upload, all file names from the archive will be collected.
You can nest directories in the archive, SWAN will accept any path to a file in the archive.

For randomizing the order for each participant, this is the list of files that is shuffled.
If you change the dataset after the study is released, the sorted list of file names must remain stable.

### Creating a Study

Under `App` -> `Studys` click `Add`. Select a title, a title image and the description in markdown.
Select your dataset and the UI configuration, set the start and end date.

If you wish to limit the study to a specific group of users, select the group.

If you want to release the study to anonymous users, check the box. The QR code will then contain an authentication tag
for this study.

### Adding a solution

Under `App` -> `Solutions` click `Add`. Select the study this solution is for and upload the solution archive.
For each file path in the original archive, this archive needs to contain the solution image.
`dataset.zip : images/001.png` -> `solution.zip : images/001.png`.

For each solution you can define a custom text that will be displayed in the frontend.
In the Config object, assign an object `{"text": "Solution text"}` to the file path key.

### Extra

If anonymous access is enabled, the QR code can be generated under `App` -> `Studys` and clicking `QR` under `Share` for the study.

To export filtered data of the last choice for each image, click `CSV` under `Export` in `App` -> `Studys` for the study.

The two classification types for known and unknown users provide filtering and raw export.

## User

Currently handled by the intro in the frontend.
