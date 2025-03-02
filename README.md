# **Data Engineering Project: Azure & Databricks Pipeline**

## ** Project Overview**
This project implements a **scalable data pipeline** using **Azure Blob Storage, Databricks, and Apache Spark** to ingest, process, and store product data. The data is extracted from an external API, cleaned and transformed using Databricks, and stored in Azure for further analysis and visualization.

---

## ** Project Structure**
```
📦 databricks-azure-pipeline
├── 📂 config               # Configuration files
│   ├── config.yaml        # Azure storage settings
├── 📂 data                 # Data storage (not pushed to GitHub)
│   ├── 📂 raw              # Raw data from API
│   ├── 📂 processed        # Processed data
├── 📂 notebooks            # Databricks notebooks
│   ├── 01_Data_Ingestion_and_Cleaning.ipynb
├── 📂 src                  # Python scripts
│   ├── config.py          # Load environment configurations
│   ├── azure_blob.py      # Azure Blob Storage connection
│   ├── etl
│   │   ├── ingest.py      # Fetch data from API and store in Azure
│   │   ├── transform.py   # Process and clean data in Databricks
│   ├── download_processed_data.py  # Download processed data from Azure
├── .gitignore              # Ignore unnecessary files
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

---

## ** Technologies Used**
- **Cloud Platform:** Azure Blob Storage
- **Processing Engine:** Apache Spark (Databricks)
- **Storage Formats:** JSON (raw), Parquet (processed)
- **Programming Language:** Python
- **Version Control:** Git & GitHub

---

## ** Project Workflow**
### **Step 1: Set Up Azure Blob Storage**
1. Created an **Azure Storage Account**.
2. Created two **containers**:
   - `raw-data`: To store raw JSON files.
   - `processed-data`: To store cleaned Parquet files.

### **Step 2: Extract Data from API & Store in Azure**
1. Used `requests` to fetch product data from **DummyJSON API**.
2. Saved the JSON data to Azure Blob Storage in `raw-data/products.json`.
3. Verified the upload using **Azure Portal**.

### **Step 3: Read Raw Data in Databricks**
1. Connected **Databricks** to **Azure Blob Storage** using access keys.
2. Loaded `products.json` into a **Spark DataFrame**:
    ```python
    df = spark.read.option("multiline", "true").json("wasbs://raw-data@datalakealexvidal.blob.core.windows.net/products.json")
    df.show(truncate=False)
    ```

### **Step 4: Data Cleaning & Transformation**
1. **Selected relevant columns & renamed them:**
    ```python
    from pyspark.sql.functions import col
    df_clean = df.select(
        col("id").alias("product_id"),
        col("title").alias("product_name"),
        col("price"),
        col("brand")
    )
    ```
2. **Removed duplicates & handled missing values:**
    ```python
    df_clean = df_clean.dropDuplicates()
    df_clean = df_clean.dropna(subset=["product_id", "product_name"])
    ```
3. **Added a timestamp column:**
    ```python
    from pyspark.sql.functions import current_timestamp
    df_clean = df_clean.withColumn("processing_date", current_timestamp())
    ```

### **Step 5: Store Processed Data in Azure**
1. Saved the cleaned DataFrame in **Parquet format**:
    ```python
    df_clean.write.mode("overwrite").parquet("wasbs://processed-data@datalakealexvidal.blob.core.windows.net/products_cleaned")
    ```
2. Verified the stored files in **Azure Portal**.

## ** How to Run the Project**
### **🔹 Install Dependencies**
```bash
pip install -r requirements.txt
```

### **🔹 Run the Data Ingestion Script**
```bash
python src/etl/ingest.py
```

### **🔹 Download Processed Data**
```bash
python src/download_processed_data.py
```


