# MRS
Music recommender system for spotify songs


This music recommender system uses Doc2Vec to generate vectors of size 400 out of lyrics, and then suggests songs similar to it based  on the lyrics.

# Setup

This project uses python version 3.9.15

Once python has been installed, install the requirements using the command:

```
pip install -r requirements.txt
```
Once the packages have been installed, you can view a demo of the application by running demo.py file

# Demo
Before running the demo.py file in the <strong>the MRS</strong> folder , add the lyrics of the song you are listening to, to the 
<strong>lyrics_test.txt </strong> file in <strong>the MRS folder</strong> 

In order to change the data from which to recommend, please geenerate a fresh 'preprocessed_data.csv' file by running get_preprocessed_data function in the preprocessing.py file.

# API
in order to run the api, run the following command in the api directory:
```
flask --app app run
```
# Docker



You can also use the Dockerfile to directly build an image with all dependencies and use the web app.

To build the image:
```
docker build -t <imagename>:<tag> <rootdirectory>
```
After that just run your image as a container:

```
docker run -d -p <localport>:5000 <imagename>:<tag>
```
Then you can connect with the web app via localhost:<localport> in your browser.

# Docker
You can also use the Dockerfile to directly build an image with all dependencies and use the web app.

To build the image:

```
docker build -t <imagename>:<tag> <rootdirectory>
```
After that just run your image as a container:
```
docker run -d -p <localport>:5000 <imagename>:<tag>
```

Make sure to change the url in <strong>swagger-initialize.js</strong> to reflect the port you use in docker
Then you can connect with the web app via localhost:<localport> in your browser.
## input lyrics, and enjoy the recommendations!
