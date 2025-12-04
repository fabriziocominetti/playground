-- First check

-- SELECT *
-- FROM covidDeaths

-- SELECT *
-- FROM covidVaccinations

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM covidDeaths
ORDER BY 1

-- total cases vs total deaths

SELECT location, date, total_cases, total_deaths, ((total_deaths * 1.0) / total_cases)*100 as deathPercentage
FROM covidDeaths
WHERE location = 'Italy'
ORDER BY 1, 2

-- total cases vs population

SELECT location, date, total_cases, population, ((total_cases * 1.0) / population)*100 as casesPopulation
FROM covidDeaths
WHERE location = 'Italy'
ORDER BY 1, 2

-- countries with highest infection rate compared to population
SELECT location, population, MAX(total_cases) AS highestInfection, MAX((total_cases * 1.0 / population))*100 AS percentagePopInfected
FROM covidDeaths
GROUP BY location, population
ORDER BY percentagePopInfected DESC

-- countries with highest death count per population
SELECT location, population, MAX(total_deaths) AS highestDeaths, MAX((total_deaths * 1.0 / population))*100 AS percentagePopDeath
FROM covidDeaths
GROUP BY location, population
ORDER BY percentagePopDeath DESC

-- countries with highest death count
SELECT location, MAX(total_deaths)
FROM covidDeaths
GROUP BY location
ORDER BY MAX(total_deaths) DESC

-- remove continents from result
SELECT location, MAX(total_deaths)
FROM covidDeaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY MAX(total_deaths) DESC

-- continents with highest death count per population
SELECT continent, MAX(total_deaths) as totalDeathsCount
FROM covidDeaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY totalDeathsCount DESC

-- global numbers
SELECT date, SUM(new_cases), SUM(new_deaths), SUM(new_deaths * 1.0)/SUM(new_cases) AS deathPercentage
FROM covidDeaths
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1, 2

-- total
SELECT SUM(new_cases), SUM(new_deaths), SUM(new_deaths * 1.0)/SUM(new_cases) AS deathPercentage
FROM covidDeaths
WHERE continent IS NOT NULL

-- join the two tables
SELECT *
FROM covidDeaths AS cD
JOIN covidVaccinations AS cV
ON cD.location = cV.location AND cD.date = cV.date

-- total population vs vaccinations
SELECT cD.continent, cD.location, cD.date, cD.population, cV.new_vaccinations
FROM covidDeaths AS cD
JOIN covidVaccinations AS cV
ON cD.location = cV.location AND cD.date = cV.date
WHERE cD.continent IS NOT NULL
ORDER BY 2, 3

SELECT cD.continent, cD.location, cD.date, cD.population, cV.new_vaccinations,
SUM(cV.new_vaccinations) OVER (PARTITION BY cD.location ORDER BY cD.location) AS rollingPeopleVaccinated
FROM covidDeaths AS cD
JOIN covidVaccinations AS cV
ON cD.location = cV.location AND cD.date = cV.date
WHERE cD.continent IS NOT NULL
ORDER BY 2, 3

-- common table expression
WITH popVSvac (continent, location, date, population, new_vaccinations, rollingPeopleVaccinated)
AS
(
SELECT cD.continent, cD.location, cD.date, cD.population, cV.new_vaccinations,
SUM(cV.new_vaccinations) OVER (PARTITION BY cD.location ORDER BY cD.location, cD.date) AS rollingPeopleVaccinated
FROM covidDeaths AS cD
JOIN covidVaccinations AS cV
ON cD.location = cV.location AND cD.date = cV.date
WHERE cD.continent IS NOT NULL
)
SELECT *, (rollingPeopleVaccinated * 1.0 / population) * 100
FROM popVSvac

-- create view for later viz
CREATE VIEW percPopVaccinated AS
SELECT cD.continent, cD.location, cD.date, cD.population, cV.new_vaccinations,
SUM(cV.new_vaccinations) OVER (PARTITION BY cD.location ORDER BY cD.location, cD.date) AS rollingPeopleVaccinated
FROM covidDeaths AS cD
JOIN covidVaccinations AS cV
ON cD.location = cV.location AND cD.date = cV.date
WHERE cD.continent IS NOT NULL

SELECT *
FROM percPopVaccinated