from django.shortcuts import render
from django.http import JsonResponse
import string
import secrets
import re


def home(request):
    context = {}

    if request.method == "POST":

        is_ajax = (
            request.headers.get("X-Requested-With") == "XMLHttpRequest"
        )

        try:
            password_length = int(request.POST.get("myRange", 8))
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Invalid password length"},
                status=400
            )

        # Validate password length
        if not 1 <= password_length <= 50:
            return JsonResponse(
                {"error": "Password length must be between 1 and 50"},
                status=400
            )

        chars = request.POST.getlist("option")

        if not chars:
            return JsonResponse(
                {"error": "Select at least one character option"},
                status=400
            )

        password = create_password(password_length, chars)
        strength = password_strength(password)

        # Return JSON for AJAX requests
        if is_ajax:
            return JsonResponse({
                "new_password": password,
                "strength": strength
            })

        # Normal form submission fallback
        context["new_password"] = password
        context["strength"] = strength

    return render(request, "base.html", context)


def create_password(length, chars):
    char = ""

    if "uppercase" in chars:
        char += string.ascii_uppercase

    if "lowercase" in chars:
        char += string.ascii_lowercase

    if "numbers" in chars:
        char += string.digits

    if "symbols" in chars:
        char += string.punctuation

    if not char:
        char = string.ascii_letters

    # secrets.choice is more suitable for secure passwords
    return "".join(secrets.choice(char) for _ in range(length))


def password_strength(password):
    length = len(password)
    score = 0

    if length <= 4:
        score += 1
    elif length <= 8:
        score += 2
    elif length <= 12:
        score += 3
    else:
        score += 4

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"[0-9]", password):
        score += 1

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Good"
    elif score <= 6:
        return "Strong"
    else:
        return "Very Strong"
