class XFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Або 'ALLOW-FROM http://example.com' для дозволу певних доменів
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response
