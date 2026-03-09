# API Documentation

## Authentication
All API endpoints require the user to be authenticated. Use session-based authentication or token-based authentication for API calls.

## Endpoints

### GET /api/devices/
Returns a list of devices in JSON format with filtering options.

**Parameters:**
- `type` (optional): Filter by device type ('serial' or 'parallel')
- `category` (optional): Filter by category ID

**Response:**
```json
{
  "devices": [
    {
      "id": 1,
      "name": "Arduino Uno",
      "type": "serial",
      "category": "Serial Devices",
      "specs": {"voltage": "5V", "clock": "16MHz"},
      "created_by": "admin"
    }
  ]
}
```

**Example Requests:**
- `/api/devices/` - Get all devices
- `/api/devices/?type=serial` - Get all serial devices
- `/api/devices/?category=1` - Get devices in category 1

### GET /api/search/
Returns search suggestions for devices based on query string.

**Parameters:**
- `q` (required): Search query string

**Response:**
```json
{
  "suggestions": [
    {"id": 1, "name": "Arduino Uno"},
    {"id": 3, "name": "Arduino Mega"}
  ]
}
```

**Example Request:**
- `/api/search/?q=arduino` - Search for devices containing "arduino"

## Views

### Device List View
- **URL**: `/`
- **Template**: core/device_list.html
- **Context Variables**:
  - `devices` (Page object): Paginated list of devices
  - `form` (DeviceSearchForm): Search form with fields for search, category, and device_type
  - `categories` (QuerySet): All available categories
  - `page_obj`: Pagination object
  - `is_paginated` (Boolean): Whether results are paginated

### Device Detail View
- **URL**: `/device/<id>/`
- **Template**: core/device_detail.html
- **Required**: User must be authenticated
- **Context Variables**:
  - `device` (Device object): The device being viewed
  - `user` (User object): Current authenticated user

### Device Comparison View
- **URL**: `/compare/<id1>/<id2>/`
- **Template**: core/device_comparison.html
- **Required**: User must be authenticated
- **Context Variables**:
  - `device1` (Device object): First device
  - `device2` (Device object): Second device
  - `comparison` (DeviceComparison object): Comparison data

### Contact View
- **URL**: `/contact/`
- **Template**: core/contact.html
- **Context Variables**:
  - `form` (ContactForm): Contact form with fields for name, email, subject, message

## Authentication Views

### Login
- **URL**: `/accounts/login/`
- **Method**: GET, POST
- **Template**: accounts/login.html
- **Rate Limit**: 5 attempts per minute (IP-based)
- **Context Variables**:
  - `form` (AuthenticationForm): Login form

### Register
- **URL**: `/accounts/register/`
- **Method**: GET, POST
- **Template**: accounts/register.html
- **Rate Limit**: 3 attempts per minute (IP-based)
- **Context Variables**:
  - `form` (UserRegisterForm): Registration form

### Profile
- **URL**: `/accounts/profile/`
- **Method**: GET
- **Template**: accounts/profile.html
- **Required**: User must be authenticated
- **Context Variables**:
  - `user` (User object): Current user with all profile information

### Password Reset
- **URL**: `/accounts/password_reset/`
- **Method**: GET, POST
- **Template**: accounts/password_reset.html
- **Context Variables**:
  - `form` (PasswordResetForm): Password reset form

### Logout
- **URL**: `/accounts/logout/`
- **Method**: POST
- **Redirects**: To `/accounts/login/`

## Error Responses

### 404 Not Found
Returned when a device or resource does not exist.

### 403 Forbidden
Returned when user lacks necessary permissions.

### 429 Too Many Requests
Returned when rate limit is exceeded (authentication endpoints).

## Search Query Examples

- Search for devices: `GET /?search=arduino`
- Filter by type: `GET /?device_type=serial`
- Filter by category: `GET /?category=1`
- Combine filters: `GET /?search=arduino&device_type=serial`

## Pagination

Device list view returns 10 items per page. Navigate using:
- Current page: `?page=1`
- Next page: `?page=2`
- Previous page: Navigation controls in template

## Rate Limiting

- Login endpoint: 5 attempts per minute per IP
- Register endpoint: 3 attempts per minute per IP
- All other endpoints: No rate limit (except via middleware)