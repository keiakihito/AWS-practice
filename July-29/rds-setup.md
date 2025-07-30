# ✅ Amazon RDS PostgreSQL Setup Summary for `ipalpiti-kkatsumi-rds`

This document summarizes the full setup process for our AWS RDS PostgreSQL instance used to manage metadata and audio file indexing for the iPalpiti archive project.

---

## 📦 1. RDS Instance Configuration

- **DB Identifier**: `ipalpiti-kkatsumi-rds`
- **Engine**: PostgreSQL 17.4
- **Instance Class**: `db.t3.micro`
- **Region**: `us-east-2`
- **Publicly Accessible**: `Yes`
- **Storage**: 20 GiB (gp2), autoscaling enabled
- **Encryption**: Enabled (AWS KMS key: `aws/rds`)

---

## 🔐 2. Security Group Configuration

To allow secure access to the database from development environments:

- **Created new security group**: `rds-access-from-myip`
- **Inbound Rule**:
  - **Type**: PostgreSQL
  - **Port**: 5432
  - **Source**: `<your_public_ip>/32` (CIDR format)

> ⚠️ Access is IP-restricted. Please add your own IP address to the inbound rules if needed.

- **Associated Security Groups with RDS**:
  - ✅ `rds-access-from-myip`
  - ✅ `default` (still attached but not sufficient for external access)

---

## 🔐 3. SSL/TLS Configuration

To enforce secure communication, SSL is enabled:

- **Certificate Authority File Used**: `rds-ca-rsa2048-g1.pem`
- **SSL Mode in client (e.g., DataGrip)**: `Require`

Download link for official CA file (if needed):  
https://truststore.pki.rds.amazonaws.com/global/rds-ca-rsa2048-g1.pem

---

## 🔑 4. Access Credentials

- **Master Username**: `postgres`
- **Master Password**: 🔒 _Reset during setup (not stored by AWS, please store securely)_

---

## 🧪 5. Local Client Connection (e.g., DataGrip)

| Field     | Value                                                                 |
|-----------|-----------------------------------------------------------------------|
| Host      | `ipalpiti-kkatsumi-rds.c9yic0sisutz.us-east-2.rds.amazonaws.com`      |
| Port      | `5432`                                                                |
| User      | `postgres`                                                            |
| Password  | _Your password_                                                       |
| Database  | `postgres` (or another if created manually)                           |
| SSL       | Enabled with `rds-ca-rsa2048-g1.pem` in "Require" mode                |

---

## ✅ Tested and Confirmed

- ✅ Successfully connected via DataGrip with SSL
- ✅ Verified security group rules and public access
- ✅ Confirmed proper inbound port configuration for PostgreSQL

---

## 🧠 Notes

- Please do not expose port `5432` to `0.0.0.0/0` in production environments.
- Security group changes are effective immediately.
- You can add new team members by modifying the `rds-access-from-myip` group.

