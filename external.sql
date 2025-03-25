CREATE OR REPLACE EXTERNAL TABLE  `diattara.mosefdata.external_table`
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['gs://diattar/*.json']
); 

select *   from  `diattara.mosefdata.external_table`
