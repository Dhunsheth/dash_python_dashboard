# Reflection for Milestone 2

Currently we have completed the following tasks:
1. Dataframes containing the numbers for plotting all plots have been created and saved. 
2. Layout/headings/positining is complete. 
3. Color and styles have been synced so visuals flow seamlessly. 
4. Created a new github repo to host Heroku deployment files and connected Heroku account to that Github repo instead of a Heroku repo. 

**Challenges**   
Our dataset contains a years worth of Chicago ride sharing data which a little more than 3.2 million rows. To reduce the load on memory several techniques were attempted:

1. Data for the plots was pre-calculated. 
2. Dataframes were stored in Parquet format to reduce file sizes. 
3. Files are hosted on github and read directly using Github API. 

Locally, we can run the app with the full dataset, however, due to the basic plan memory limits of Heroku which limits the memory usage to 512mb, when the data is read in the app, it exceeds this limit (goes over 1500mb) and causes the Heroku deployment to crash. As a result, instead of using the full years worth of data, we have currently opted to use the first 4 months worth of data.

In addition, the memory usage is also quite close to the 512mb limit and so sometimes performance is a little slow, however, all interactions are working and relative fast and user-friendly. 

In the future, would like to be able to use the full dataset. 