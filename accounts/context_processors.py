def theme(request):
    """Expose the current theme (from cookie) to templates.

    Returns 'dark' or 'light'. Default is 'light'.
    """
    theme = request.COOKIES.get('theme', 'light')
    return {
        'theme': theme
    }
