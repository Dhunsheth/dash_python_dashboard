# Chicago Bike Sharing Dash App

[Bike Sharing App Link](https://bike-sharing-py-dashapp-44627a5faee5.herokuapp.com/)

The Bike Share Dashboard addresses the crucial challenge of maintaining an optimal bike inventory for profitability in bike-sharing businesses. Commissioned by a Bike Sharing Organization (e.g., NABSA), the dashboard aims to provide insightful visualizations on key aspects, answering vital questions for effective operational management.     

Motivation and Purpose:      
The primary objective of the dashboard is to visualize the most popular times for bike rentals, categorized by hour of the day and month. Understanding the duration of rentals based on bike type (classic/electric) and identifying popular rental locations are integral components. The dashboard is designed to ensure the Bike Sharing Organization can meet the demand adequately, enhancing operational efficiency.    

Research Questions:    
The dashboard addresses three critical research questions:     

1. **Peak Usage Times:** Identifying the most popular timeframes during the day and year for bike shares, anticipating commuting peaks and seasonal trends.    
2. **Duration Analysis:** Investigating the duration of trips based on ride type (electric/classic) to determine user preferences.     
3. **Station Popularity:** Analyzing the popularity of stations for both starting and ending bike shares, facilitating inventory management and relocation strategies to meet demand effectively.        

The Bike Sharing Dashboard serves as a valuable tool for the Bike Sharing Organization to make data-driven decisions, optimize inventory management, and enhance user experience in the dynamic and competitive bike-sharing industry. Finally, a sketch of the proposed dashboard can be seen in the image below. 

### Challenges
The biggest challenge faced with the project was dealing with 1 year's worth of data (more than 3 million rows). Some techniques used to reduce the memory load included pre-calculating metrics for plotting, multi-indexing, and storing data as parquet files for efficient storage. In addition, with Heroku deployment, storing files on GitHub in LFS format, and reading them directly helped speed up app deployment. However, ultimately, due to the sheer size, rather than using 1 years worth of data, a reduced amount of 4 months had to be used to stay under the Heroku 512mb memory limit to prevent the app from crashing.

In the future, either better resources can be used on Heroku to increase the memory limit, or a cloud data warehouse to store the data from which the necessary rows/columns can be retrieved as needed.

![Deployed Dash App](dashapp.jpg)    
       
         
![Initial Idea](sketch.jpg)
