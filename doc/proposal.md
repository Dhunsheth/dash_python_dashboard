# Bike Share Dashboard    
     
By: Tim Pulfer, Jacob Rosen, Dhun Sheth   

### Section 1: Motivation and Purpose    

**Our Role:** Data science consultancy firm

**Stakeholder:** Bike Sharing Organization (ex. NABSA)

A critical part of running a profitable bike sharing business is ensuring approriate bike inventory is available at all times. To this end, we have been hired to create a dashboard which helps the company visualize the most popular times (by hour of day and month) for bike rentals, duration of the rental based on type of bike (classic/electric), and popular rental locations to ensure sufficient demand is met. 

### Section 2: Description and Data     

We will be using a dataset containing 5,719,877 rows, where each row corresponds to a bike share taking place. Each row has the following parameters: 
1. ride_id
2. rideable_type - electric_bike/classic_bike
3. started_at - ride start date/time
4. ended_at - ride end data/time
    - We will calculate the duration of the rental but taking the difference in start and end datetimes.
5. start_station_name
6. start_station_id
7. end_station_name
8. end_station_id
9. start_lat
10. start_lng
11. end_lat
12. end_lng
13. member_casual - member/casual

### Section 3: Research Questions    

Below are the research questions our dashboard will aim to answer.

1. What are the most popular timeframes during the day when the most bike shares take place? What are the most popular times during the year? 
    - We anticipate bike shares to peak during the morning/afternoons when bikers are commuting to/from work and in the afternoon on the weekends.
    - We also anticipate bike sharing would be reduced during the colder months and be higher during the summer months. 
2. The duration of the trip based on ride type - to understand if users have a certain preference for electric vs. classic bikes. 
    - We are interested to learn if electric bikes are being used less (perhaps due to battery contraints or because riders can go faster on electric bikes to reach their desired locations quicker over classic bikes).
3. Which stations are the most popular to start a bike share vs. ending it? This would help the company adjust their inventory to ensure popular starting locations are stocked with enough bikes and neccessary relocation services are deployed to move bikes from popular ending locations. 
 


