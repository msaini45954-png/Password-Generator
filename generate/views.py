from django.shortcuts import render
import string
import random
import re


# Create your views here.
def home(request):
    context = {}

    if request.method == "POST":
        password_length = int(request.POST.get("myRange"))
        chars = request.POST.getlist("option")

        password = create_password(password_length, chars)
        strength = password_strength(password)

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

    return "".join(random.choice(char) for _ in range(length))


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
