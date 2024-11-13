val expresionregex="[0-9]{4}-[0-9]{2}-[0-9]{2}"

val df=Seq(("1" ,"200,123", "2020-12-13", "0,2"), ("2",  "100,13", "2019-11-13 11:40:00", "0,19"))
       .toDF("IdClient","PriceHTT", "Date_transaction",  "TVA")
df.withColumn("TVA", regexp_replace($"TVA", ",", ".").cast(DoubleType))
  .withColumn("PriceHTT", regexp_replace($"PriceHTT", ",", ".").cast(DoubleType))
 .withColumn("PriceTTC", round($"PriceHTT"*$"TVA"+$"PriceHTT", 1))
 .withColumn("jour", to_date(col("Date_transaction"),"yyyy-MM-dd HH:mm:SS").as("to_date"))
 .withColumn("dat", regexp_extract($"Date_transaction", expresionregex, 0))
 .show
