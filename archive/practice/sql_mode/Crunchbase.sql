-- SQL Outer Joins

SELECT *
FROM organizations;

SELECT *
FROM acquisitions;

SELECT organizations.permalink AS companies_permalink,
	   organizations.name AS companies_name,
	   acquisitions.permalink AS acquisitions_permalink,
	   acquisitions.acquired_on AS acquired_date
FROM organizations
JOIN acquisitions
ON organizations.permalink = acquisitions.permalink;

-- SQL left join

SELECT organizations.permalink AS companies_permalink,
	   organizations.name AS companies_name,
	   acquisitions.permalink AS acquisitions_permalink,
	   acquisitions.acquired_on AS acquired_date
FROM organizations
LEFT JOIN acquisitions
ON organizations.permalink = acquisitions.permalink;

-- Filtering in the ON clause

SELECT organizations.permalink AS companies_permalink,
	   organizations.name AS companies_name,
	   acquisitions.permalink AS acquisitions_permalink,
	   acquisitions.acquired_on AS acquired_date
FROM organizations
LEFT JOIN acquisitions
ON organizations.permalink = acquisitions.permalink
ORDER BY 1;

-- Filtering in the WHERE clause

SELECT organizations.permalink AS companies_permalink,
	   organizations.name AS companies_name,
	   acquisitions.permalink AS acquisitions_permalink,
	   acquisitions.acquired_on AS acquired_date
FROM organizations
LEFT JOIN acquisitions
ON organizations.permalink = acquisitions.permalink
WHERE acquisitions.permalink != '/company/1000memories'
OR acquisitions.permalink IS NULL
ORDER BY 1;
