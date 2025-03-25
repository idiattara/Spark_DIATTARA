CREATE OR REPLACE MODEL `diattara.mosefdata.kmeansmodele`
OPTIONS (MODEL_TYPE='KMEANS', NUM_CLUSTERS=4) AS
SELECT lon, lat 
FROM `diattara.mosefdata.uber_data`

------------------------------------------------------------

SELECT * FROM ML.PREDICT(MODEL `diattara.mosefdata.kmeansmodele`,(SELECT  * FROM  `diattara.mosefdata.uber_data` ))
