# Data Engineering Stack

---

## Programming & Software Engineering
> Core foundation for writing pipelines, automation, and scalable systems.

- Python (syntax, performance, idioms, testing, type hints)  
- SQL (querying, optimization, window functions)  
- Functional and object-oriented programming  
- Git and version control workflows (GitHub Flow, GitLab Flow)  
- API design (REST, JSON schema, OpenAPI)  
- Documentation tools: Sphinx, MkDocs, docstrings  
- Writing testable, maintainable code (unit/integration tests, test coverage)  
- CI/CD fundamentals: GitHub Actions, GitLab CI, GitOps, AWS CodePipeline  

---

## Data Modeling & Management
> Understanding how to structure, validate, and govern your data.

- Data modeling (OLTP vs OLAP, star/snowflake schemas)  
- File formats: CSV, JSON, Parquet, Avro, ORC  
- Table formats: Delta Lake, Iceberg, Hudi  
- Data quality: Great Expectations  
- Data governance: lineage, catalogs, data documentation  
- Compliance & contracts: GDPR, PII handling, data contracts (Protobuf, Avro schemas)  
- SCD (Slowly Changing Dimensions), CDC (Change Data Capture) strategies  
- Metadata management: OpenMetadata  

---

## Databases & Query Engines
> How data is stored and queried — from raw storage to analytics.

- Relational databases: PostgreSQL, MySQL, SQLite, DuckDB  
- NoSQL: MongoDB, key-value stores  
- Query engines: Trino, Presto, AWS Athena (serverless SQL on S3)  
- Data warehouses: Snowflake, BigQuery, Redshift  
- Query optimization: indexes, partitions, join strategies  
- Materialized views, caching strategies  

---

## Data Engineering Platforms & Orchestration
> Building and automating reliable data pipelines.

- ETL/ELT patterns (batch vs streaming)  
- Workflow orchestration: Airflow, Temporal  
- Declarative transformation: dbt  
- Dynamic DAGs, sensors, branching, retries  
- Modular, metadata-driven pipelines  

---

## Big Data & Distributed Processing
> Handling massive datasets and distributed compute frameworks.

- Apache Spark (batch and structured streaming, RDDs, DataFrames)  
- PySpark, lazy execution, Catalyst optimizer  
- Partitioning, bucketing, compaction strategies  
- Efficient storage formats for distributed compute (columnar, compressed)
- MPP (Massively Parallel Processing) architecture  

---

## Streaming & Real-Time Systems
> Low-latency and event-driven architectures.

- Kafka (brokers, producers, consumers)  
- Kafka Connect, Kafka Streams  
- Event-driven architecture fundamentals  
- Apache Flink (event-time, windowing, stateful streaming, fault tolerance)  
- Stream processing vs microbatch  

---

## Cloud & Infrastructure Engineering
> Deploying and running data systems at scale.

- Cloud platforms: AWS (primary), GCP, Azure  
- Object storage: AWS S3  
- IAM, VPCs, networking basics  
- Containers: Docker, AWS ECS (Elastic Container Service)  
- Container registry: AWS ECR  
- Kubernetes: Helm, autoscaling, job scheduling  
- Serverless: AWS Lambda  
- Stream transport: Amazon Kinesis  
- Infrastructure as Code (IaC): Terraform  

---

## Observability, Monitoring & Security
> Know when things break — and secure them by default.

- Logs, metrics, and tracing  
- Monitoring tools: Prometheus, Grafana  
- AWS monitoring: CloudWatch (logs, metrics, alerts)  
- Alerting and SLAs/SLOs  
- Access control: RBAC, IAM policies  
- Encryption: at rest and in transit  
- Secrets management: Vault, AWS Secrets Manager  

---

## Libraries, Tooling & Interfaces
> Tools to build, explore, and debug faster.

- Data manipulation: Polars, Pandas, PyArrow  
- SQL abstraction: SQLAlchemy  
- IDE and Notebooks: VSCode, PyCharm, Jupyter  
- Dashboards and apps: Streamlit, matplotlib, seaborn  
- SQL clients: DBeaver  

---

## Artificial Intelligence & Machine Learning
> Many data pipelines feed into or support ML and AI systems — understanding their architecture helps build robust integrations and prepare data effectively.

- ML foundations: regression, classification, evaluation metrics  
- Feature engineering, ML pipelines, model training/testing workflows  
- Batch vs real-time inference  
- LLM architecture: transformers, tokenization, embeddings  
- Retrieval-Augmented Generation (RAG) pipelines  
- Vector databases: FAISS, Pinecone, Chroma  
- Orchestration: LangChain, LlamaIndex  
- Vector store performance: indexing, scaling, memory tradeoffs  
- Prompt engineering: prompt templates, context length, system prompts  
- Multimodal models and generative pipelines
- Vision-Language models 

---

## Computer Science for Data Engineers
> Systems-level concepts to reason about performance, scale, and architecture.

- Operating systems: Linux CLI, file systems, permissions  
- Networking: HTTP, DNS, IP addressing, firewalls  
- Data structures & algorithms: maps, trees, sorting, hashing  
- Architecture patterns: queues, caches, pub/sub, backpressure  
- Memory and concurrency: stack/heap, GC, multithreading, multiprocessing  
- Systems design fundamentals: scalability, availability, fault tolerance  
- Distributed systems theory: CAP theorem, consistency models (ACID/BASE)  
