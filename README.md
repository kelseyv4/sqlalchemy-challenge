# sqlalchemy-challenge
In this challenge, I used the climate_starter in order to look at weather data for Hawaii. One portion was to retrieve the precipitation data for the most recent year, and the other was to look at the temperature data coming out of the most active

Using the queries from the first portion for the Flask portion was pretty tricky, but I was able to convert most of the results into a JSON in Flask. However, the 'precipitation' route still isn't formatting quite the way it should. However, the issue that took me the longest to resolve was being able to go to the other routes without restarting the code. I eventually realized it was because I was forgetting to close the sessions.
