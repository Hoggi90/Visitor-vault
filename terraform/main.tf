provider "aws" {
  region = "eu-west-2" # Replace with your desired region
}

# Variables
variable "db_name" {
  default = "visitorvault"
}

variable "db_user" {
  default = "admin" # Replace with your username
}

variable "db_password" {
  default = "Generation2024" # Replace with a secure password
}

variable "s3_bucket_name" {
  default = "visitorvault-static-website"
}

# S3 Bucket for Static Website
resource "aws_s3_bucket" "website_bucket" {
  bucket = var.s3_bucket_name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_s3_bucket_policy" "website_bucket_policy" {
  bucket = aws_s3_bucket.website_bucket.id

  policy = <<EOT
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${aws_s3_bucket.website_bucket.id}/*"
    }
  ]
}
EOT
}

# RDS (MySQL)
resource "aws_db_instance" "mysql_db" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro" # Free-tier eligible
  name                 = var.db_name
  username             = var.db_user
  password             = var.db_password
  publicly_accessible  = true
  skip_final_snapshot  = true

  tags = {
    Name = "VisitorVaultDB"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_policy_attachment" {
  name       = "lambda_policy_attachment"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole"
}

# Lambda Function
resource "aws_lambda_function" "lambda" {
  function_name = "visitorvault-lambda"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  filename      = "${path.module}/lambda/lambda_function.zip"
  
  environment {
    variables = {
      DB_HOST     = aws_db_instance.mysql_db.address
      DB_NAME     = var.db_name
      DB_USER     = var.db_user
      DB_PASSWORD = var.db_password
    }
  }
}

resource "aws_lambda_permission" "api_gateway_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"
}

# API Gateway
resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "VisitorVaultAPI"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.api_gateway.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.lambda.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "route" {
  api_id    = aws_apigatewayv2_api.api_gateway.id
  route_key = "POST /submit"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "$default"
  auto_deploy = true
}

# Outputs
output "s3_bucket_url" {
  value = aws_s3_bucket.website_bucket.website_endpoint
}

output "api_gateway_endpoint" {
  value = aws_apigatewayv2_api.api_gateway.api_endpoint
}
