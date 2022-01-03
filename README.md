# steam-data-dashboard

### Intro
This streamlit dashboard provides visualization on the daily max user count for the top-100 video games on the Steam platform.

This application uses the following GCP services:
  - Cloud Scheduler (Sends a message to a Cloud Pub/Sub topic at 9 pm)
  - Cloud Pub/Sub
  - Cloud Function (Pulls a message from the topic and run the scraping code, then store the data into Cloud storage)
  - Cloud Run (Deploys the containeraized streamlit application)
  - Cloud Storage
  - Container Registry (Manages Docker images)

---

### GCP Architecture
The whole architecture is like the picture below.

![architecture](gcp_architecture.png)
---

### App Display
![pic1](app_1.png)
![pic2](app_2.png)
