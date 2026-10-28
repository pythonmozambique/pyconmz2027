def show_toolbar(request):
    """Show the debug toolbar only when a request asks for it with ?dt=1."""
    return request.GET.get("dt") == "1"
