App / Area	Owner	What It Contains
Rwot:
accounts	         -	Custom user model, auth views (login/logout/register), password reset, permission groups

core	            -	Device, Category, Tag, Comparison models; all device views; Django admin config

api		            -JSON endpoints for AJAX calls (search suggestions, device data)
content	Annet	Content views (device list, detail, compare, search), all forms, device fixtures

Ann:
content		       -Content views (device list, detail, compare, search), all forms, device fixtures

Okedi:
blog		       -Post, Category, Comment models and views; post list and detail with comment handling
notifications	   -	Notification model, list view, mark-as-read; post_save signal on Comment
