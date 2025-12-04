----- YouTube tutorial

--- look at the data

SELECT *
FROM vehicle_coupon_recommendation;

--- limit the amount of data

SELECT *
FROM vehicle_coupon_recommendation
LIMIT 10;

--- look at the passengers

SELECT DISTINCT passanger
FROM vehicle_coupon_recommendation;

--- where passanger travelled Alone

SELECT *
FROM vehicle_coupon_recommendation
WHERE passanger = 'Alone';

--- And, Or

SELECT *
FROM vehicle_coupon_recommendation
WHERE passanger = 'Alone' AND weather = 'Sunny' AND destination = 'Home';

SELECT *
FROM vehicle_coupon_recommendation
WHERE passanger = 'Alone' OR time = '2PM';

--- Ordering

SELECT *
FROM vehicle_coupon_recommendation
WHERE passanger = 'Alone' OR time = '2PM'
ORDER BY time ASC;

--- Aliasing

SELECT destination, time AS 'The Time'
FROM vehicle_coupon_recommendation AS vcr
WHERE passanger = 'Alone';

--- Aggregation

SELECT destination, AVG(temperature)
FROM vehicle_coupon_recommendation
GROUP BY destination;

SELECT destination, AVG(temperature), COUNT(temperature)
FROM vehicle_coupon_recommendation
GROUP BY destination;

SELECT destination, time, AVG(temperature), COUNT(temperature)
FROM vehicle_coupon_recommendation
GROUP BY destination, time;

SELECT destination, time, AVG(temperature), COUNT(temperature)
FROM vehicle_coupon_recommendation
WHERE time != '10PM' 
GROUP BY destination, time;

SELECT destination, time, AVG(temperature), COUNT(temperature)
FROM vehicle_coupon_recommendation
GROUP BY destination, time
HAVING occupation != 'unemployed';

--- Union

SELECT *
FROM table 1 AS t1
UNION
SELECT *
FROM table2 AS t2

--- Joins (A and B tables)

-- Inner Join = A + B in common
-- Left Join = all A + B in common
-- Right Join = all B + A in common
-- Outer Join = all A + all B

--- Like

SELECT *
FROM vehicle_coupon_recommendation
WHERE weather LIKE 'Sun%';

SELECT *
FROM vehicle_coupon_recommendation
WHERE time LIKE '%PM';

--- Between

SELECT DISTINCT temperature
FROM vehicle_coupon_recommendation
WHERE temperature BETWEEN 50 AND 70;

--- In

SELECT occupation
FROM vehicle_coupon_recommendation
WHERE occupation IN ('Management', 'Sales & Related');

--- Over, Partition By

SELECT destination, weather, AVG(temperature)
OVER (PARTITION BY weather) AS 'avg_temp_by_weather'
FROM vehicle_coupon_recommendation;

--- Row Number

SELECT destination, weather, ROW_NUMBER()
OVER (PARTITION BY weather ORDER BY destination) AS 'avg_temp_by_weather'
FROM vehicle_coupon_recommendation;

--- Rank

SELECT destination, weather, RANK()
OVER (PARTITION BY weather ORDER BY destination) AS 'avg_temp_by_weather'
FROM vehicle_coupon_recommendation;

SELECT destination, weather, DENSE_RANK()
OVER (PARTITION BY weather ORDER BY destination) AS 'avg_temp_by_weather'
FROM vehicle_coupon_recommendation;

--- Ntile

SELECT time, NTILE(50) OVER (ORDER BY time)
FROM vehicle_coupon_recommendation;

--- Lag

SELECT destination, time, LAG(row_count, 1, '99999') OVER (ORDER BY row_count) AS 'lagged_count'
FROM vehicle_coupon_recommendation;

----- ChatGPT questions

--- What are the distinct values of the "destination" column in the dataset?

SELECT DISTINCT destination
FROM vehicle_coupon_recommendation;

--- Which weather condition had the highest number of coupons of the category Coffee House?

SELECT weather, COUNT(weather) AS 'conteggio'
FROM vehicle_coupon_recommendation
WHERE coupon = 'Coffee House'
GROUP BY weather
ORDER BY conteggio DESC;

--- What is the average temperature for each combination of weather and time?

SELECT weather, time, AVG(temperature)
FROM vehicle_coupon_recommendation
GROUP BY weather, time;

--- Among individuals who have children, what is the count of coupons categories by gender?

SELECT coupon, COUNT(coupon) AS 'conteggio'
FROM vehicle_coupon_recommendation
WHERE has_children = 1
GROUP BY coupon;

--- What is the average age of individuals for coupon category, grouped by marital status and education level?

SELECT coupon, maritalStatus, education, AVG(age)
FROM vehicle_coupon_recommendation
GROUP BY coupon, maritalStatus, education;

--- For each occupation, what is the sum of coupons categories by individuals with an income equal to a certain threshold (e.g., "high income")?

SELECT occupation, coupon, COUNT(*) AS 'conteggio'
FROM vehicle_coupon_recommendation
GROUP BY occupation, coupon
HAVING income = '$62500 - $74999';