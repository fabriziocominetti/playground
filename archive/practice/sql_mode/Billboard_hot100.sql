-- logical operators with SQL

SELECT *
FROM charts;

-- The SQL LIKE operator

SELECT *
FROM charts
WHERE song LIKE 'kiss%';

-- The SQL IN operator

SELECT *
FROM charts
WHERE artist IN ('Machine Gun Kelly', 'Post Malone', 'Shawn Mendes');

-- The SQL BETWEEN operator

SELECT *
FROM charts
WHERE "peak-rank" BETWEEN 1 AND 3;

-- The IS NULL operator

SELECT *
FROM charts
WHERE "last-week" IS NULL;

-- The SQL AND operator

SELECT *
FROM charts
WHERE "peak-rank" = 1 AND "weeks-on-board" >= 10;

-- The SQL OR operator

SELECT *
FROM charts
WHERE "rank" = 1
AND (artist = 'Kanye West' OR artist = 'Eminem');

-- The SQL NOT operator

SELECT *
FROM charts
WHERE artist = 'Drake'
AND "last-week" IS NOT NULL;
