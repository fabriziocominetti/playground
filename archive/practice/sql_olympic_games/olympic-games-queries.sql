--- How many olympics games have been held?

SELECT COUNT(DISTINCT Games) as total_olympic_games
FROM athlete_events;

--- How many athletes have participated in each olympic game?

SELECT Games, Year, COUNT(*) as total_athletes
FROM athlete_events
GROUP BY Games, Year;

SELECT *
FROM athlete_events
WHERE Games = '1896 Summer';

--- List down all the olympic games held so far

SELECT DISTINCT Games, Year, Season, City
FROM athlete_events
ORDER BY Year;

--- Mention the total number of nations who participated in each olympics game

SELECT Games, COUNT(DISTINCT NOC) AS number_of_nations
FROM athlete_events
GROUP BY Games
ORDER BY Games;

SELECT DISTINCT NOC
FROM athlete_events
WHERE Games = '1896 Summer';

--- Which year saw the highest and lowest number of countries participating in olympics?

SELECT Games, COUNT(DISTINCT NOC) AS number_of_nations, MIN(number_of_nations) AS lowest, MAX(number_of_nations) AS highest
FROM athlete_events
GROUP BY Games;

--- Which nation has participated in all of the olympic games?
--- Identify the sport which was played in all summer olympics.
--- Which Sports were just played only once in the olympics?
--- Fetch the total no of sports played in each olympic games.
--- Fetch details of the oldest athletes to win a gold medal.
--- Find the Ratio of male and female athletes participated in all olympic games.
--- Fetch the top 5 athletes who have won the most gold medals.
--- Fetch the top 5 athletes who have won the most medals (gold/silver/bronze).
--- Fetch the top 5 most successful countries in olympics. Success is defined by no of medals won.
--- List down total gold, silver and broze medals won by each country.
--- List down total gold, silver and broze medals won by each country corresponding to each olympic games.
--- Identify which country won the most gold, most silver and most bronze medals in each olympic games.
--- Identify which country won the most gold, most silver, most bronze medals and the most medals in each olympic games.
--- Which countries have never won gold medal but have won silver/bronze medals?
--- In which Sport/event, India has won highest medals.
--- Break down all olympic games where india won medal for Hockey and how many medals in each olympic games.