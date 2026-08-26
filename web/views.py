import requests

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def portfolio(request):
    return render(request, "portfolio.html")


def contact(request):
    enviado = False
    error = False

    if request.method == "POST":
        nombre = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        asunto = request.POST.get("subject", "").strip()
        mensaje = request.POST.get("message", "").strip()

        # Token generado por Cloudflare Turnstile
        turnstile_token = request.POST.get("cf-turnstile-response")

        print("TURNSTILE TOKEN:", turnstile_token)

        if not turnstile_token:
            print("❌ No llegó el token de Turnstile")
            error = True

        elif not all([nombre, email, asunto, mensaje]):
            error = True

        else:
            # Verificar Turnstile en los servidores de Cloudflare
            try:
                response = requests.post(
                    "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                    data={
                        "secret": settings.TURNSTILE_SECRET,
                        "response": turnstile_token,
                        "remoteip": request.META.get("REMOTE_ADDR"),
                    },
                    timeout=10,
                )

                turnstile_result = response.json()

                if not turnstile_result.get("success"):
                    print("Turnstile rechazó la solicitud:")
                    print(turnstile_result)

                    error = True

                else:
                    contenido = f"""
Has recibido un nuevo mensaje desde mcherrera.dev

Nombre: {nombre}
Email: {email}
Asunto: {asunto}

Mensaje:
{mensaje}
"""

                    try:
                        email_message = EmailMessage(
                            subject=f"[mcherrera.dev] {asunto}",
                            body=contenido,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[settings.CONTACT_EMAIL],
                            reply_to=[email],
                        )

                        email_message.send(fail_silently=False)

                        enviado = True

                    except Exception as e:
                        print(f"Error enviando correo: {e}")
                        error = True

            except requests.RequestException as e:
                print(f"Error comunicando con Cloudflare Turnstile: {e}")
                error = True

    return render(
        request,
        "contact.html",
        {
            "enviado": enviado,
            "error": error,
            "TURNSTILE_SITEKEY": settings.TURNSTILE_SITEKEY,
        },
    )