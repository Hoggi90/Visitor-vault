# Provider Configuration
provider "aws" {
  region = "eu-west-2" 
}

# RDS Database Instance
resource "aws_db_instance" "visitor_rds" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro"
  name                 = "visitorvaultdb"
  username             = "admin"
  password             = "Generation2024" 
  publicly_accessible  = true
  skip_final_snapshot  = true

  # Free-tier eligible
  backup_retention_period = 0
}

# Lambda Function Role and Policies
resource "aws_iam_role" "lambda_role" {
  name = "visitor_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function
resource "aws_lambda_function" "visitor_lambda" {
  function_name    = "visitor-vault-lambda"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  timeout          = 15
  filename         = "lambda_function.zip" # Upload your Lambda function as a ZIP file
  environment {
    variables = {
      DB_HOST     = aws_db_instance.visitor_rds.address
      DB_NAME     = aws_db_instance.visitor_rds.name
      DB_USER     = aws_db_instance.visitor_rds.username
      DB_PASSWORD = aws_db_instance.visitor_rds.password
    }
  }
}

# API Gateway
resource "aws_apigatewayv2_api" "visitor_api" {
  name          = "VisitorVaultAPI"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.visitor_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.visitor_lambda.invoke_arn
}

resource "aws_apigatewayv2_route" "post_route" {
  api_id    = aws_apigatewayv2_api.visitor_api.id
  route_key = "POST /submit"
  target    = aws_apigatewayv2_integration.lambda_integration.id
}

resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.visitor_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "apigateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.visitor_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.visitor_api.execution_arn}/*"
}

# Output the API Gateway URL
output "api_gateway_url" {
  value = aws_apigatewayv2_api.visitor_api.api_endpoint
}

# Output the RDS Endpoint
output "rds_endpoint" {
  value = aws_db_instance.visitor_rds.address
}
