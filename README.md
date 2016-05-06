# tPresent
**tPresent** is a presence web application. It replaces [Sqwiggle](https://www.sqwiggle.com/) still pictures feature.

This project targets only presence feature. It was a great feature of Sqwiggle but they announced they shutdown the service. To replace chat/audio conference, you can use [Slack](https://www.slack.com) and for video conferences you can take a look at [Zoom](https://www.zoom.us).

### Usage
---
You can use online version hosted on https://tPresent.pythonanywhere.com or run you own instance.

Simply select an name, a room and switch online. A still image is shot every minute. Interface is refreshed every minute with all members images.

![tpresent](https://cloud.githubusercontent.com/assets/3621529/15069064/d9e2ceb2-13ad-11e6-90c8-faca729c53aa.jpg)

### Self-hosted installation / development
---
```bash
> git clone --recursive https://github.com/gpailler/tPresent.git
> cd tPresent

> pip install virtualenv
> virtualenv venv --python=python3.4
> source venv/bin/activate

> pip install -r requirements.txt

> python flask_app.py
```
You may have to change some constants in `flask_app.py` to match your needs (bind address, refresh delay...)

### Limitations
---
Tested on Chrome and Firefox on Windows/Mac.
Image capture uses [webcamjs](https://github.com/jhuckaby/webcamjs) library and all major browsers should be supported (an Adobe Flash fallback is provided by webcamjs).

### Donations :gift:
---
Donations are always welcomed :smile:
https://www.paypal.me/gpailler
