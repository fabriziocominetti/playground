-- aggregate functions

-- Counting all rows

SELECT COUNT(*)
FROM HistoricalQuotes AS "apple_stockPrice";

-- Counting individual columns

SELECT COUNT(High)
FROM HistoricalQuotes AS "apple_stockPrice";

-- Counting non-numerical columns

SELECT COUNT("Date")
FROM HistoricalQuotes AS "apple_stockPrice";

-- The SQL SUM function

SELECT SUM(Volume)
FROM HistoricalQuotes;

-- The SQL MIN and MAX functions

SELECT MIN(Volume) AS min_volume, MAX(Volume) AS max_volume
FROM HistoricalQuotes;

-- The SQL AVG function

SELECT AVG(High)
FROM HistoricalQuotes;

-- The SQL GROUP BY clause

SELECT year, COUNT(*) AS count
FROM HistoricalQuotes
GROUP BY year;

SELECT year, month, COUNT(*) AS count
FROM HistoricalQuotes
GROUP BY year, month;

-- Using GROUP BY with ORDER BY

SELECT year, month, COUNT(*) AS count
FROM HistoricalQuotes
GROUP BY year, month
ORDER BY month, year;

-- The SQL HAVING clause

SELECT year,
       month,
       MAX(High) AS month_high
FROM HistoricalQuotes
GROUP BY year, month
HAVING MAX(High) > 400
ORDER BY year, month;
