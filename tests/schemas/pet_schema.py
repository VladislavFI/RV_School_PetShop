PET_SCHEMA = {
  "title": "Pet",
  "type": "object",
  "required": ["id", "name", "photoUrls", "status"],
  "properties": {
    "id": {
      "type": "integer"
    },
    "name": {
      "type": "string"
    },
    "category": {
      "type": "object",
      "required": ["id", "name"],
      "properties": {
        "id": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        }
      }
    },
    "photoUrls": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
          "id": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": ["available", "pending", "sold"]
    }
  }
}