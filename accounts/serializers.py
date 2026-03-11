from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . utils import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
from . serializers import UserSerialiser, UserProfileSerialiser
from django.core.mail import EmailMessage
from . models import UserProfile
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    # Check if the user exists (by username or email)
    user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()

    if user is None or not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN)

    # Check if the user is active
    if not user.is_active:
        return Response({ "error": "Account is inactive. Please check your email or contact support."}, status=status.HTTP_403_FORBIDDEN)
    # Generate tokens
    refresh = RefreshToken.for_user(user)

    # Get the user's profile (handling cases where it doesn't exist)
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_data = UserProfileSerialiser(user_profile).data  # Serialize UserProfile
    except UserProfile.DoesNotExist:
        user_data = {"error": "User profile not found"}  # Handle missing profile gracefully

    return Response({
        "refreshToken": str(refresh),
        "accessToken": str(refresh.access_token),
        "user": user_data  # Return full user profile data
    }, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])  # Allow anyone to register
def register(request):
    print(request.data)
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    password = request.data.get("password")
    id_number = request.data.get("id_number")
    user_type = request.data.get("role")
    gender = request.data.get("gender")
    department = request.data.get("department")

    if not all([username, email, password, first_name, last_name, id_number, user_type, gender]):
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password, is_active=False)  # Inactive
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    userProfile = UserProfile.objects.create(user=user, id_number=id_number, gender = gender, role = user_type)
    if 'image' in request.FILES:
        image = request.FILES['image']
        userProfile.image = image
        
    if department: userProfile.department = department
    userProfile.save()

    # Generate activation token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    activation_link = f"https://127.0.0.1:3000/activate/{uid}/{token}"

    # Send activation email
    subject = "Activate Your Account"
    html_message = render_to_string("activation_email.html", {"user": user, "activation_link": activation_link})
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email="admin@student_tracking.com",
        to=[user.email],
    )
    email.content_subtype = "html" 
    email.send()

    return Response({
            "message": "User registered successfully. Check your email to activate your account.", 
            "data":UserSerialiser(user).data
        }, 
        status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get("refresh")

    if refresh_token is None:
        return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
    except TokenError as e:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_all_view(request):
    user = request.user

    try:
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            # If not already blacklisted, blacklist it
            if not BlacklistedToken.objects.filter(token=token).exists():
                BlacklistedToken.objects.create(token=token)

        return Response({"message": "All sessions logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)

    except Exception as e:
        return Response({"error": "Something went wrong while logging out from all devices."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Account activated successfully. You can now log in."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired activation link."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    if not user.check_password(old_password):
        return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({"error": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get("email")
    user = User.objects.filter(email=email).first()

    if not user:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"http://127.0.0.1:3000/reset-password/{uid}/{token}"

    send_mail(
        "Password Reset Request",
        f"Click the link below to reset your password:\n{reset_url}",
        "admin@company.com",
        [email],
    )

    return Response({"message": "Password reset email has been sent with instructions on how to reset your password, Thank You"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, uidb64, token):
    """
    Resets the user's password using a secure token.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    if new_password != confirm_password:
        return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)


@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def user_profile(request):
    user = request.user
    if request.method == "GET":
        try:
            profile_data = UserProfile.objects.get(user = user)
            serializer = UserProfileSerialiser(profile_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist as e:
            return Response({"error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =="PUT":
        print(request.data)
        user_profile_data = get_object_or_404(UserProfile, user=request.user) 
        serializer = UserProfileSerialiser(user_profile_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
