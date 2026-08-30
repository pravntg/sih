# Terraform Infrastructure Skeleton for Project ORCA

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "environment" {
  type    = string
  default = "staging"
}

# PostgreSQL + PostGIS RDS Cluster Skeleton
resource "aws_db_instance" "orca_geodb" {
  allocated_storage      = 50
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t4g.medium"
  db_name                = "orca_db"
  username               = "orca_admin"
  password               = var.db_password
  skip_final_snapshot    = true
  publicly_accessible    = false
}

variable "db_password" {
  type      = string
  sensitive = true
  default   = "ChangeMeInVault123!"
}

# S3 Bucket for Satellite Raster & Model Artifacts
resource "aws_s3_bucket" "orca_raster_bucket" {
  bucket = "orca-raster-artifacts-${var.environment}"
}
