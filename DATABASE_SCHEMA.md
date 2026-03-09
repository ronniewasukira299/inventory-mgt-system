# Database Schema Design for Serial & Parallel Devices Web Platform

## Entities and Relationships

### User (Custom Model in accounts app)
- id (AutoField, Primary Key)
- username (CharField, unique)
- email (EmailField, unique)
- first_name (CharField)
- last_name (CharField)
- bio (TextField, optional)
- role (CharField, choices: admin, editor, viewer)
- joined_date (DateTimeField, auto_now_add)
- is_active (BooleanField, default=True)
- is_staff (BooleanField, default=False)
- date_joined (DateTimeField, auto_now_add)
- last_login (DateTimeField, null=True)

### Category
- id (AutoField, Primary Key)
- name (CharField, unique)
- description (TextField, optional)
- slug (SlugField, unique)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)

### Tag
- id (AutoField, Primary Key)
- name (CharField, unique)
- slug (SlugField, unique)
- created_at (DateTimeField, auto_now_add)

### Device
- id (AutoField, Primary Key)
- name (CharField)
- type (CharField, choices: serial, parallel)
- description (TextField)
- specs (JSONField)
- category (ForeignKey to Category)
- tags (ManyToManyField to Tag)
- created_by (ForeignKey to User)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)

### DeviceComparison
- id (AutoField, Primary Key)
- device1 (ForeignKey to Device)
- device2 (ForeignKey to Device)
- comparison_data (JSONField, stores comparison results)
- created_by (ForeignKey to User)
- created_at (DateTimeField, auto_now_add)

## Relationships
- User 1:N Device (created_by)
- User 1:N DeviceComparison (created_by)
- Category 1:N Device
- Tag N:N Device
- Device 1:N DeviceComparison (device1, device2)

## Indexes
- Device: type, category_id
- DeviceComparison: device1_id, device2_id