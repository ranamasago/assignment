SELECT
   TO_CHAR (init_license_dt,'MM') AS year_month,
   business_type,
   COUNT (*) AS store_count
FROM
   minato_restaurant
WHERE
   init_license_dt BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY
   year_month, business_type 
ORDER BY
    year_month, store_count DESC;