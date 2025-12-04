Texas Death Row

--- Run this query to find the first 3 rows of the 'executions' table
SELECT *
FROM executions
LIMIT 3;

--- Find the first and last names and ages (ex_age) of inmates 25 or younger at time of execution
SELECT first_name, last_name, ex_age
FROM executions
WHERE ex_age <= 25;

--- Find Napoleon Beazley's last statement
SELECT last_statement
FROM executions
WHERE first_name = 'Napoleon' AND last_name = 'Beazley';

--- Edit the query to find how many inmates provided last statements
SELECT COUNT(first_name)
FROM executions
WHERE last_statement IS NOT NULL;

--- Find the total number of executions in the dataset
SELECT COUNT(first_name)
FROM executions;

SELECT COUNT(*) FROM executions;

--- Find how many inmates were over the age of 50 at execution time
SELECT COUNT(*)
FROM executions
WHERE ex_age > 50;

--- Find the number of inmates who have declined to give a last statement
SELECT COUNT(*)
FROM executions
WHERE last_statement IS NULL;

SELECT
	COUNT(CASE WHEN last_statement IS NULL
		  THEN 1 ELSE NULL END)
FROM executions;

--- Find the minimum, maximum and average age of inmates at the time of execution
SELECT MIN(ex_age), MAX(ex_age), AVG(ex_age)
FROM executions;

--- Find the average length (based on character count) of last statements in the dataset
SELECT AVG(LENGTH(last_statement))
FROM executions;

--- List all the counties in the dataset without duplication
SELECT DISTINCT county
FROM executions;

-- Find the proportion of inmates with claims of innocence in their last statements

SELECT
1.0 * COUNT(CASE WHEN last_statement LIKE '%innocent%'
    THEN 1 ELSE NULL END) / COUNT(*)
FROM executions;

--- Pulls the execution counts per county
SELECT county, COUNT(*) AS county_executions
FROM executions
GROUP BY county;

--- This query counts the executions with and without last statements
SELECT
  last_statement IS NOT NULL AS has_last_statement,
  county, COUNT(*)
FROM executions
GROUP BY has_last_statement, county;

--- Count the number of inmates aged 50 or older that were executed in each county
SELECT county, COUNT(*)
FROM executions
WHERE ex_age >= 50
GROUP BY county;

--- List the counties in which more than 2 inmates aged 50 or older have been executed
SELECT county
FROM executions
WHERE ex_age >= 50
GROUP BY county
HAVING COUNT(*) > 2;

--- Find the first and last name of the inmate with the longest last statement (by character count)
SELECT first_name, last_name
FROM executions
WHERE LENGTH(last_statement) =
    (SELECT MAX(LENGTH(last_statement))
	 FROM executions);

--- Insert the <count-of-all-rows> query to find the percentage of executions from each county
SELECT
  county,
  100.0 * COUNT(*) / (SELECT COUNT(*) FROM executions)
    AS percentage
FROM executions
GROUP BY county
ORDER BY percentage DESC;

--- Write a query to produce the previous table
SELECT
  ex_number + 1 AS ex_number,
  ex_date AS last_ex_date
FROM executions
WHERE ex_number < 553;