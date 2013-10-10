from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _
from django.conf import settings
from student.models import UserStanding

class UserStandingMiddleware(object):
	"""
	Checks a user's standing on request. Deletes their session if the user's
	status is 'disabled'.
	"""
	def process_request(self, request):
		user = request.user
		try:
			user_account = UserStanding.objects.get(user=user.id)
			# because user is a unique field in UserStanding, there will either be
			# one or zero user_accounts associated with a UserStanding
		except UserStanding.DoesNotExist:
			pass
		else:
			if user_account.account_status == u'account_disabled':
				msg = _(
                            'Your account has been disabled. If you believe '
                            'this was done in error, please contact us at '
                            '{link_start}{support_email}{link_end}'
                        ).format(
                            support_email = settings.CONTACT_EMAIL,
                            link_start = u'<a href="mailto:{address}?subject={subject_line}">'.format(
                                address=settings.CONTACT_EMAIL,
                                subject_line=_('Disabled Account'),
                            ),
                            link_end = u'</a>'
                        )
				return HttpResponseForbidden(msg)
