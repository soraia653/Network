# Network
This repository contains a Twitter-like social network website for making posts and following users.

This is part of CS50's Web Programming with Python and JavaScript and corresponds to the Week 7 assignment.

## API explanation
You are able to  fetch all posts by using this applications' API.

This application supports the following API routes:

```GET /posts```
Sending a ```GET``` request to ```/posts``` will return (in JSON form) a list of all existing posts, in reverse chronological order. A JSON response will look like this:

```
[
    {
        "user": "pipocaDourada",
        "post: "This is my 1st post!",
        "date": "Jan 2 2020, 12:00 AM",
        "num_likes": 12
    },
    {
        "user": "atumCaro",
        "post: "Mine too!",
        "date": "Jan 1 2022, 12:03 AM",
        "num_likes": 81
    }
]
```