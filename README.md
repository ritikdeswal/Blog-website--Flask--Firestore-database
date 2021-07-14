# Blog-website--Flask--Firestore-database

This web app was created in **HTML ,CSS ,Javascript ,Python ,Flask** 
which stores images in **Firebase storage** 
then puts the image URL in **Firestore Database** along with the blog contents.
This app was deployed on **Digital Ocean** cloud server using **Nginx and gunicorn**
```bash
scorpion-tech.co
```

## Software used for development
- Pycharm
- Sublime text 4
- Bootstrap Sutdio

## Python modules 
```python
import os
import glob
from flask import Flask, render_template, request, redirect, url_for, session , g
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
```

## Preview
![](https://github.com/ritikdeswal/Blog-website--Flask--Firestore-database/blob/main/fullPage.png)

## Theme toggle button
![](https://github.com/ritikdeswal/Blog-website--Flask--Firestore-database/blob/main/theme-toggle.gif)

## Dynamic calendar made in Javascript to highlight the dates on which a blog is posted
![](https://github.com/ritikdeswal/Blog-website--Flask--Firestore-database/blob/main/calendar.png)

## Searchbox which gets the matching blog title on Key up ,without reloading the page and without pressing enter key 😄
![](https://github.com/ritikdeswal/Blog-website--Flask--Firestore-database/blob/main/searchBox.png)

## Finally the main blog page
![](https://github.com/ritikdeswal/Blog-website--Flask--Firestore-database/blob/main/Blog.png)



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

 
