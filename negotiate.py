def generate_email(service: str, price: str) -> str:
    """
    Generate a cancellation/negotiation email for a given subscription service.

    Args:
        service: The name of the service (e.g., "Netflix", "Adobe")
        price:   The current price string (e.g., "$19.99")

    Returns:
        A formatted email body as a string.
    """
    return (
        f"Subject: Subscription Review Request – {service}\n\n"
        f"Hi {service} Support Team,\n\n"
        f"I've been a loyal customer and I'm currently on a plan costing {price}/month. "
        f"I'm reviewing my subscriptions and am seriously considering cancelling unless "
        f"a better rate is available.\n\n"
        f"Before I make that decision, I wanted to reach out directly to ask:\n"
        f"  • Are there any loyalty discounts or promotional rates available?\n"
        f"  • Is there a lower-tier plan that might suit my usage?\n"
        f"  • Are there any upcoming promotions I should know about?\n\n"
        f"I'd really prefer to stay with {service} if we can find a price that works "
        f"for both of us. Please let me know what options are available.\n\n"
        f"Thank you for your time,\n"
        f"[Your Name]\n"
        f"[Your Account Email]"
    )
