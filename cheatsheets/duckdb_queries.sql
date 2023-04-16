-- select data on filter and save results to csv file and include a header
COPY 
    (SELECT * FROM posts WHERE lower(title) LIKE '%breaking%')
TO 
    'breaking_news.csv' 
    (FORMAT CSV, DELIMITER ',', HEADER); 