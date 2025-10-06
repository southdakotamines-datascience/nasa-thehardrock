# THE Hard Rock at NASA Space Apps
## Meteor Madness
[Link to team](https://www.spaceappschallenge.org/2025/find-a-team/the-hard-rock/?tab=details)
## Overview
This project takes a hypothetical meteorite and predicts the damages done if the meteorite hits the Earth surface. Using [NOAA's earthquake dataset from year 2000 to now](https://www.ngdc.noaa.gov/hazel/view/hazards/earthquake/event-data?minYear=2000), we can predict a variety of outcomes using XGBoost. By first taking a meteorite's mass and velocity, we can calculate the energy released by the meteorite and convert it to a value on the moment magnitude scale (Mw). Then, given a Mw magnitude, predict the consequences.

## Features
- Customize a hypothetical asteroid by changing mass and volume through a user-friendly interface of inputs and sliders
- Visualize the diameter of a crater on impact
- Get metrics of consequences such as houses destroyed, injuries, damage in millions of dollars, etc.

## Implementation
1. Data reading:
   - Read in the NOAA Earthquake data from year 2000, page by page.
   - Preprocess the data; impute NULLs with K-nearest neighbors
2. Train XGBoost model, predict consequences
3. Save and load model into the Flask web server.
4. User chooses mass, velocity, and picks a point on the map.
5. Frontend app (Vue) fetches API calls from Flask with the user's mass, velocity, longitude, latitude.
6. Flask feeds model parameters into the model and gives Vue the prediction.
7. Vue will display the data in a user-friendly way
   - Impact area is shown on a Leaflet map.
## For development purposes
### Set up the virutal environment

`cd backend`
`py -3 -m venv .venv`

### Activate the environment

`.venv\Scripts\activate`
`pip install Flask`

### Vue

`cd frontend`
`npm i`
`npm run dev`
