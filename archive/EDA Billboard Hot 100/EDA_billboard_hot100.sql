-- https://medium.com/dataseries/exploring-hot-100-billboards-weekly-charts-with-sql-c6f832a50ca8

SELECT *
FROM charts;

SELECT *
FROM charts
WHERE artist IN ('Machine Gun Kelly', 'Shawn Mendes', 'blackbear');

SELECT DISTINCT song, artist
FROM charts
WHERE artist IN ('Machine Gun Kelly', 'Shawn Mendes', 'blackbear');

SELECT DISTINCT song, artist
FROM charts
WHERE song LIKE 'kiss%';

SELECT *FROM charts
WHERE "last-week" IS NULL;

SELECT DISTINCT song, artist
FROM charts
WHERE "peak-rank" = 1 AND "weeks-on-board" >= 50;

SELECT DISTINCT song, artist, "rank"
FROM charts
WHERE "rank" = 1
AND (artist = 'Kanye West' OR artist = 'Eminem');

SELECT DISTINCT song, artist 
FROM charts
WHERE artist = 'The Weeknd'
ORDER BY song ASC;

SELECT DISTINCT song, artist 
FROM charts
WHERE artist = 'The Weeknd'
ORDER BY song DESC;

SELECT DISTINCT song, artist
FROM charts
WHERE artist = 'Drake'
GROUP BY "date"
HAVING "peak-rank" BETWEEN 1 AND 3;

SELECT artist, song, MAX("peak-rank")
FROM charts
WHERE artist = 'Giveon';

SELECT artist, song, MIN("peak-rank")
FROM charts
WHERE artist = 'Giveon';

SELECT COUNT(*)
FROM charts
WHERE (artist = 'Dua Lipa') AND ("rank" BETWEEN 1 AND 10);

SELECT AVG("weeks-on-board")
FROM charts
WHERE artist = 'Halsey';

SELECT song, artist
FROM charts
WHERE EXISTS
 (SELECT "date"
  FROM charts
  WHERE artist = 'Maneskin' AND "date" = '2021-07-17');

