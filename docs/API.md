# API Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: `https://your-api-domain.com`

## Authentication
Currently, the API does not require authentication. This will be added in future versions.

## Endpoints

### Health Check
- **GET** `/health`
  - Returns system health status

### Issues
- **GET** `/issues` - List all issues with filtering
- **GET** `/issues/{id}` - Get single issue
- **POST** `/issues` - Create new issue  
- **PUT** `/issues/{id}` - Update existing issue
- **DELETE** `/issues/{id}` - Delete issue

## Response Format
All API responses follow a consistent format with proper HTTP status codes and error handling.
