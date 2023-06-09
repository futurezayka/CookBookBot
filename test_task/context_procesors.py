def user_is_authenticated(request):
    return {'user_is_authenticated': request.session.get('is_admin_logged_in')}
