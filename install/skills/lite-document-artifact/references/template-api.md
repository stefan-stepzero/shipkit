# API Reference Template

Complete template for documenting REST/GraphQL APIs, webhooks, and API schemas.

---

#### Template: API Reference (api/)

```markdown
# [API Name]

**Created**: [Date]
**Status**: [Draft/Active/Deprecated]
**Owner**: [Team/Person]

---

## Overview

**Purpose**: [What this API does in 1-2 sentences]

**Base URL**: `[URL]`

---

## Authentication

**Method**: [Bearer token / API key / OAuth / None]

**Headers required**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

---

## Endpoints

### [Method] /endpoint-path

**Description**: [What this endpoint does]

**Request**:
```json
{
  "field1": "value",
  "field2": "value"
}
```

**Response** (200 OK):
```json
{
  "id": "123",
  "status": "success"
}
```

**Error responses**:
- `400 Bad Request` - [When this happens]
- `401 Unauthorized` - [When this happens]
- `404 Not Found` - [When this happens]
- `500 Server Error` - [When this happens]

**Example**:
```bash
curl -X POST https://api.example.com/endpoint \
  -H "Authorization: Bearer {token}" \
  -d '{"field1": "value"}'
```

---

## Rate Limits

[Rate limit info if applicable]

---

## Changelog

| Date | Change | Version |
|------|--------|---------|
| [Date] | Initial version | 1.0 |

---

## Related

- [Link to related implementation]
- [Link to related spec]
```

---

#### Template: Architecture