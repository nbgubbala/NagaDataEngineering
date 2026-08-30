from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    spark = SparkSession.builder.appName("PySparkDataUIExample").master("local[*]").getOrCreate()

    sample_rows = [
        ("Alice", "Engineering", 85000, "New York"),
        ("Bob", "Analytics", 91000, "Chicago"),
        ("Carol", "Marketing", 78000, "Austin"),
        ("David", "Finance", 96000, "Boston"),
        ("Eve", "Operations", 72000, "Seattle"),
    ]

    df = spark.createDataFrame(sample_rows, ["name", "department", "salary", "city"])
    df = df.withColumn("salary", F.col("salary").cast("double"))

    print("Sample Spark DataFrame:")
    df.show(truncate=False)

    output_file = Path(__file__).resolve().parent / "sample_data.json"
    pandas_df = df.toPandas()
    pandas_df.to_json(output_file, orient="records", indent=2)

    print(f"Saved JSON data to: {output_file}")
    spark.stop()


if __name__ == "__main__":
    main()
