package spark
import org.apache.spark.sql.{SparkSession, Dataset}
import org.apache.spark.sql.functions._
object SaprkApp2  extends  App {

  // Définir un cas de classe pour représenter les données de ventes
  case class Sale(Date: String, Produit: String, Prix: Double, Quantité: Int, Vendeur: String)

  // Créer une session Spark
  val spark = SparkSession.builder()
    .appName("Sales Analysis")
    .master("local[*]")
    .getOrCreate()

  import spark.implicits._

  // Lire les données depuis le fichier texte en tant que Dataset
  val filePath = "C:\\Users\\ibrah\\Downloads\\SalutationProcessor-master\\uvs1\\src\\data\\Sales.txt"
  val salesDS: Dataset[Sale] = spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(filePath)
    .as[Sale]

  // Afficher les 5 premières lignes du Dataset
  println("Les 5 premières lignes du Dataset :")
  salesDS.show(5)

  // Calculer le montant total des ventes pour chaque produit
  val totalSalesByProduct = salesDS
    .withColumn("TotalVente", col("Prix") * col("Quantité"))
    .groupBy("Produit")
    .agg(sum("TotalVente").alias("MontantTotal"))
    .as[(String, Double)]

  println("Montant total des ventes pour chaque produit :")
  totalSalesByProduct.show()

  // Trouver le produit le plus vendu (en termes de quantité)
  val mostSoldProduct = salesDS
    .groupBy("Produit")
    .agg(sum("Quantité").alias("QuantitéTotale"))
    .orderBy(desc("QuantitéTotale"))
    .limit(1)
    .as[(String, Long)]

  println("Produit le plus vendu :")
  mostSoldProduct.show()

  // Calculer la somme totale des ventes pour chaque vendeur
  val totalSalesBySeller = salesDS
    .withColumn("TotalVente", col("Prix") * col("Quantité"))
    .groupBy("Vendeur")
    .agg(sum("TotalVente").alias("MontantTotal"))
    .as[(String, Double)]

  println("Somme totale des ventes pour chaque vendeur :")
  totalSalesBySeller.show()

  // Arrêter la session Spark
  spark.stop()

}
