import json
from pathlib import Path

from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.appName("EmployeeDataExample").master("local[*]").getOrCreate()

    csv_path = Path(__file__).resolve().parent / "employees.csv"
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(str(csv_path))

    rows = [row.asDict(recursive=True) for row in df.collect()]
    output_file = Path(__file__).resolve().parent / "sample_data.json"
    output_file.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    print(f"Saved JSON data to: {output_file}")
    df.show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
