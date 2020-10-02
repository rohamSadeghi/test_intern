from rest_framework.throttling import ScopedRateThrottle


class PhoneNumberScopedRateThrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):

        if 'phone_number' in request.data:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.data['phone_number']
            }
        return super().get_cache_key(request, view)
