# API Feature Specification

## Overview

**API Name:** [Descriptive name]
**Version:** v1
**Problem Statement:** [What does this API solve?]
**Primary Consumers:** [Who/what will call this API?]

## Endpoints

### Endpoint 1: [Name]

**Method:** `GET`/`POST`/`PUT`/`DELETE`/`PATCH`
**Path:** `/api/v1/resource/{id}`
**Description:** [What this endpoint does]

**Authentication:** Required/Optional
**Authorization:** [Required permissions/roles]

#### Request

**Path Parameters:**
```
{id} (string, required): Resource identifier
```

**Query Parameters:**
```
?filter=value (string, optional): Filter results
?page=1 (integer, optional): Page number for pagination
?limit=20 (integer, optional): Results per page (max 100)
```

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
```

**Request Body:**
```json
{
  "field1": "value",
  "field2": 123,
  "nested": {
    "property": true
  }
}
```

**Validation Rules:**
- `field1`: Required, 1-255 characters, alphanumeric
- `field2`: Required, integer, range 1-1000
- `nested.property`: Required, boolean

#### Response

**Success (200 OK):**
```json
{
  "data": {
    "id": "abc123",
    "field1": "value",
    "field2": 123,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**Error Responses:**

**400 Bad Request:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "field1",
        "issue": "Value exceeds maximum length"
      }
    ]
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**401 Unauthorized:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid authentication token"
  }
}
```

**403 Forbidden:**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions to access this resource"
  }
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

**429 Too Many Requests:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Retry after 60 seconds."
  },
  "meta": {
    "retry_after": 60
  }
}
```

**500 Internal Server Error:**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "request_id": "uuid"
  }
}
```

#### Example Usage

**cURL:**
```bash
curl -X GET 'https://api.example.com/api/v1/resource/abc123?filter=active' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json'
```

**JavaScript (fetch):**
```javascript
const response = await fetch('https://api.example.com/api/v1/resource/abc123', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

**Python (requests):**
```python
import requests

response = requests.get(
    'https://api.example.com/api/v1/resource/abc123',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)
data = response.json()
```

## Data Models

### Resource Model

```typescript
interface Resource {
  id: string;              // UUID
  field1: string;          // 1-255 characters
  field2: number;          // Integer, 1-1000
  status: ResourceStatus;  // Enum
  created_at: string;      // ISO 8601 timestamp
  updated_at: string;      // ISO 8601 timestamp
  metadata: Record<string, any>;  // Flexible key-value store
}

enum ResourceStatus {
  ACTIVE = 'active',
  PENDING = 'pending',
  ARCHIVED = 'archived'
}
```

## Authentication & Authorization

**Authentication Method:** Bearer token (JWT)

**Token Payload:**
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "roles": ["admin", "user"],
  "exp": 1642251600
}
```

**Authorization Rules:**
- `GET /api/v1/resource`: Requires `read:resources` permission
- `POST /api/v1/resource`: Requires `write:resources` permission
- `DELETE /api/v1/resource`: Requires `delete:resources` and `admin` role

## Rate Limiting

**Limits:**
- **Authenticated:** 1000 requests per hour
- **Unauthenticated:** 100 requests per hour

**Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1642251600
```

**Limit Exceeded Response:** HTTP 429 with `Retry-After` header

## Versioning Strategy

- **URL-based versioning:** `/api/v1/`, `/api/v2/`
- **Deprecation Notice:** 6 months before removal
- **Sunset Header:** `Sunset: Sat, 1 Jan 2026 00:00:00 GMT`

## Pagination

**Request:**
```
GET /api/v1/resources?page=2&limit=50
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "current_page": 2,
    "total_pages": 10,
    "total_items": 500,
    "items_per_page": 50,
    "has_next": true,
    "has_prev": true,
    "next_url": "/api/v1/resources?page=3&limit=50",
    "prev_url": "/api/v1/resources?page=1&limit=50"
  }
}
```

## Filtering & Sorting

**Filter Syntax:**
```
?filter[status]=active
?filter[created_after]=2025-01-01
?filter[field1][contains]=search
```

**Sorting:**
```
?sort=created_at          # Ascending
?sort=-created_at         # Descending
?sort=field1,-created_at  # Multiple fields
```

## Webhooks (if applicable)

**Event Types:**
- `resource.created`
- `resource.updated`
- `resource.deleted`

**Webhook Payload:**
```json
{
  "event": "resource.created",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "id": "abc123",
    "field1": "value"
  }
}
```

**Webhook Verification:** HMAC-SHA256 signature in `X-Webhook-Signature` header

## Performance Requirements

- **Response Time:** p50 < 100ms, p95 < 500ms, p99 < 1000ms
- **Throughput:** 10,000 requests/second per endpoint
- **Availability:** 99.9% uptime

## Error Handling

**Error Code Format:** `CATEGORY_SPECIFIC_ERROR`

**Categories:**
- `VALIDATION_*`: Input validation failures
- `AUTH_*`: Authentication/authorization failures
- `RESOURCE_*`: Resource-specific errors
- `RATE_LIMIT_*`: Rate limiting errors
- `INTERNAL_*`: Server errors

## Security Considerations

- **Input Validation:** Strict schema validation on all inputs
- **SQL Injection:** Use parameterized queries
- **XSS Prevention:** Sanitize all outputs
- **CORS:** Whitelist specific origins
- **HTTPS Only:** Reject HTTP requests
- **Secret Management:** Never expose keys in responses

## Testing Strategy

**Unit Tests:**
- Request validation logic
- Authorization checks
- Business logic

**Integration Tests:**
- Full request/response cycle
- Database interactions
- External service calls

**Load Tests:**
- Throughput under normal load
- Graceful degradation under high load
- Rate limiting effectiveness

## Documentation

- **OpenAPI/Swagger Spec:** Auto-generated from code
- **API Reference:** Hosted at `/docs`
- **Postman Collection:** Available for download
- **SDK Examples:** JavaScript, Python, Go, Ruby

## Monitoring & Alerts

**Metrics:**
- Request count by endpoint
- Response time percentiles
- Error rate by status code
- Authentication failures

**Alerts:**
- Error rate > 1% for 5 minutes
- p95 latency > 1000ms for 10 minutes
- Rate limit hits > 100/minute

---

**Spec Version:** 1.0
**Last Updated:** [Date]
**Author:** [Name]
