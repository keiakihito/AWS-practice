# 📁 Project Setup: S3 + RDS + Metadata Schema (Phase 1)

This document outlines the setup process for managing iPalpiti archive data using Amazon S3 (for audio storage) and Amazon RDS (PostgreSQL for metadata). This is the first phase of the project, where we establish the architecture and manually populate the metadata schema.

---

## 1️⃣ S3 Bucket Configuration

- **Purpose**: Store all audio files (`.mp3`, `.m4a`, etc.)
- **Bucket Behavior**:
  - S3 does **not** use real folders — it uses **object keys** with slashes (`/`) to simulate directories.
  - For example:
    ```
    2025/
      Silvestrov/
        8.574481/
          01 - Elegie.mp3
          02 - Largo.mp3
    ```
- **Important Concepts**:
  - `S3 Key`: Full object path, e.g., `2025/Silvestrov/8.574481/01 - Elegie.mp3`
  - `S3 URI`: Used for signed playback links
- **Why S3 Key Matters**:
  - The `s3_key` is stored in PostgreSQL to associate metadata records with actual audio files in the bucket.

---

## 2️⃣ RDS PostgreSQL Setup

- **Instance Configuration**:
  - Public access: ✅ Enabled
  - Port: `5432`
  - Username: `postgres`
  - Password: (set manually during setup)
  - Database: `postgres` (can later create `ipalpiti_metadata`)

- **Client Setup (e.g., DataGrip)**:
  - Use the correct **endpoint hostname** from RDS
  - SSL is required:
    - Download the `.pem` certificate:
      [rds-ca-rsa2048-g1.pem](https://truststore.pki.rds.amazonaws.com/global/rds-ca-rsa2048-g1.pem)
    - In DataGrip: enable SSL and set mode to `Require`

- **If connection fails**:
  - Check that the Security Group assigned to RDS allows **Inbound TCP traffic on port 5432**
  - Add your IP address in the form: `123.45.67.89/32`
  - Make sure the correct Security Group is **attached to the RDS instance** via the AWS Console (`Modify → Connectivity`)

---

## 3️⃣ Schema Setup (SQL)

- SQL schema is defined in a file (e.g., `schema.sql`) and can be loaded manually into the RDS instance.

### Current Status:

- `albums` and `tracks` tables have been created based on the needs of classical music metadata:
  - Auto-increment IDs (`SERIAL`)
  - Fields for:
    - Title, composer, conductor, orchestra
    - Tags, genres, period, duration
    - Licensing status, original/digitized format
    - S3 key/path information
    - Soloists and instruments (free-text for now)
- See `schema.sql` for current structure (subject to iteration).

> 🛠 Next Steps:
> - Populate the database with initial metadata by manually entering album information.
> - Automate ingestion via CSV or scripts.
> - Set up API/Lambda connections to query S3 + RDS.

---