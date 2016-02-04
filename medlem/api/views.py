import ldap
from ldap.filter import filter_format, escape_filter_chars

from django.conf import settings

from jsonview.decorators import json_view


def required_parameters(*names):
    def inner(func):
        def view(request):
            values = []
            for name in names:
                value = request.GET.get(name, '').strip()
                if not value:
                    return {
                        'error': "missing key '{}'".format(name)
                    }, 400
                assert value
                values.append(value)
            return func(request, *values)
        return view
    return inner

ATTRIBUTES = ['uid', 'cn', 'sn', 'mail', 'givenName']


def connection():
    conn = ldap.initialize(settings.LDAP_SERVER_URI)
    conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    for opt, value in settings.LDAP_GLOBAL_OPTIONS.items():
        conn.set_option(opt, value)
    conn.simple_bind_s(
        settings.LDAP_BIND_DN,
        settings.LDAP_BIND_PASSWORD
    )
    return conn


def make_search_filter(data, any_parameter=False):
    params = []
    for key, value in data.items():
        if not isinstance(value, (list, tuple)):
            value = [value]
        for v in value:
            if not v:
                v = 'TRUE'
            params.append(filter_format('(%s=%s)', (key, v)))
    search_filter = ''.join(params)
    if len(params) > 1:
        if any_parameter:
            search_filter = '(|%s)' % search_filter
        else:
            search_filter = '(&%s)' % search_filter
    return search_filter


@json_view
@required_parameters('mail')
def exists(request, mail):
    search_filter = make_search_filter(
        dict(mail=mail, emailAlias=mail),
        any_parameter=True
    )
    # if search:
    #     other_filter = make_search_filter(search)
    #     search_filter = '(&{}{})'.format(search_filter, other_filter)

    rs = connection().search_s(
        settings.LDAP_SEARCH_BASE,
        ldap.SCOPE_SUBTREE,
        search_filter,
        ATTRIBUTES
    )
    for uid, result in rs:
        return True

    return False


@json_view
@required_parameters('mail')
def employee(request, mail):
    mail_filter = make_search_filter(
        dict(mail=mail, emailAlias=mail),
        any_parameter=True
    )
    other_filter = make_search_filter(
        dict(objectClass='mozComPerson')
    )
    search_filter = '(&{}{})'.format(mail_filter, other_filter)

    rs = connection().search_s(
        settings.LDAP_SEARCH_BASE,
        ldap.SCOPE_SUBTREE,
        search_filter,
        ATTRIBUTES
    )
    for uid, result in rs:
        return True

    return False


@json_view
@required_parameters('mail', 'cn')
def ingroup(request, mail, cn):
    # first, figure out the uid
    mail_filter = make_search_filter(dict(mail=mail))
    alias_filter = make_search_filter(dict(emailAlias=mail))
    search_filter = '(|{}{})'.format(mail_filter, alias_filter)

    rs = connection().search_s(
        settings.LDAP_SEARCH_BASE,
        ldap.SCOPE_SUBTREE,
        search_filter,
        ['uid']
    )
    uid = None
    for dn, result in rs:
        uid = result['uid'][0]
        break

    if not uid:
        return False

    search_filter = u"""
    (|
       (&(objectClass=groupOfNames)(cn=%(groupname)s)(member=%(dn)s))
       (&(objectClass=posixGroup)(|(cn=scm_*)(cn=svn_*))(cn=%(groupname)s)(memberUid=%(mail)s))
       (&(objectClass=posixGroup)(!(|(cn=scm_*)(cn=svn_*)))(cn=%(groupname)s)(memberUid=%(uid)s))
    )
    """

    search_filter = search_filter % {
        'groupname': escape_filter_chars(cn),
        'dn': escape_filter_chars(dn),
        'uid': escape_filter_chars(uid),
        'mail': escape_filter_chars(mail),
    }
    search_filter = search_filter.strip()

    rs = connection().search_s(
        settings.GROUP_LDAP_SEARCH_BASE,
        ldap.SCOPE_SUBTREE,
        search_filter,
        ['cn']
    )

    for __ in rs:
        return True

    return False
