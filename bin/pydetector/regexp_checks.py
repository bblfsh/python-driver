import re
import six

__all__ = ['check_syntax_regex', 'check_modules_regex', 'check_modulesymbols_regex']

# Syntactic elements. Second item in the tuple is the score.
PY3OTHER_REGEXP = [
    (re.compile(r"^.*(\s|;|:)+raise\s+.*\s+from\s+None.*$", re.MULTILINE), 100),
    (re.compile(r"(\s|;|:)+nonlocal\s+.*$", re.MULTILINE), 100),
]

PY2OTHER_REGEXP = [
    (re.compile(r"(\s|;|:)+print\s+[^\(]", re.MULTILINE), 100),
    (re.compile(r"(\s|;|:)+basestring\s+[^\(]", re.MULTILINE), 100),
    (re.compile(r"(\s|;|:)+raw_input\s+\(.*\).*$", re.MULTILINE), 100),
    (re.compile(r"(\s|;|:)+\.has_key\s+[^\(]", re.MULTILINE), 100),
    (re.compile(r"(\s|;|:)+unicode\s+\(.*\).*$", re.MULTILINE), 25),
    (re.compile(r"(\s|;|:)+iteritems\s+\(.*\).*$", re.MULTILINE), 25),
    (re.compile(r"(\s|;|:)+iterkeys\s+\(.*\).*$", re.MULTILINE), 25),
    (re.compile(r"(\s|;|:)+itervalues\s+\(.*\).*$", re.MULTILINE), 25),
    (re.compile(r"(\s|;|:)+viewkeys\s+\(.*\).*$", re.MULTILINE), 25),
    (re.compile(r"(\s|;|:)+viewitems\s+\(.*\).*$", re.MULTILINE), 25),
    (re.compile(r"(\s|;|:)+viewvalues\s+\(.*\).*$", re.MULTILINE), 25),
    (re.compile(r"(\s|;|:)+__metaclass__\s+.*$", re.MULTILINE), 100),
    (re.compile(r"(\s|;|:)+xrange\s+\(.*\).*$", re.MULTILINE), 100),
    (re.compile(r"(\s|;|:)+xreadlines\s+\(.*\).*$", re.MULTILINE), 100),
    (re.compile(r"^.*(\s|;|:)+raise\s+\w+(\.\w+)?,\s+.*$", re.MULTILINE), 100),
    (re.compile(r"^.*(\s|;|:)+except\s+((?!\().)*,[^(as)].*$", re.MULTILINE), 100),
]


PY2ONLY_MODULES_REGEXP = None
PY3ONLY_MODULES_REGEXP = None
def generate_modules_regex():
    global PY2ONLY_MODULES_REGEXP
    global PY3ONLY_MODULES_REGEXP

    py2only_modules = [
        "cfmfile", r"[^hashlib\.]([^_]md5|[^_]sha)", "mimetools", "MimeWriter", "mimify",
        "multifile", "posixfile", "rfc822", "timing", "audiodev", "stringold", "bsddb185", "Canvas",
        "commands", "compiler", "dircache", "fpformat", "htmllib", "imageop", "linuxaudiodev", "mhlib",
        "popen2", "sgmllib", "sre", "statvfs", r"[^collections\.](UserDict|UserString|UserList)",
        "ConfigParser", "copy_reg", "Queue", "SockerServer", "sets", "StringIO", "cStringIO", "cPickle",
        "dbhash", "(g|dumb|which|any)dbm", "xmlrpclib", "(Doc|Simple)XMLRPCServer", "httplib",
        "HTMLParser", "Cookie", "cookielib", "(Base|Simple|CGI)HTTPServer", "urlparse", "robotparser"

    ]
    py3only_modules = [
        "configparser", "copyreg", "queue", "socketserver", "ipaddress", "lzma",
        "contextlib", "six", # six usually mean both compatible, so just mark as 3
        "reprlib", "dbm\.(bsd|dumb|ndbm|gdbm)", "xmlrpc\.(client|server)", "http\.(client|server)",
        "urllib\.(parse|robotparser)"
    ]

    def import_regex_gen(modlist):
        strregex_import = r"^\s+import\s+.*(%s)(\s+|,|$).*" % "|".join(modlist)
        strregex_from   = r"^\s+from\s+(%s)\s+import(\s+|,).*" % "|".join(modlist)

        return re.compile("^" + strregex_import + "|" + strregex_from, re.MULTILINE)

    PY2ONLY_MODULES_REGEXP = import_regex_gen(py2only_modules)
    PY3ONLY_MODULES_REGEXP = import_regex_gen(py3only_modules)


PY3MODULESYMBOLS_REGEXPS = []
PY2MODULESYMBOLS_REGEXPS = []
def generate_modulesymbols_regex():
    global PY3MODULESYMBOLS_REGEXPS
    global PY2MODULESYMBOLS_REGEXPS

    py2only_modulesymbols = {
        "os": ["getcwdu"],
        "sys": ["exitfunc", "maxint", "exc_type", "exc_value", "exc_traceback"],
        "operator": ["isCallable", "sequenceIncludes", "isSequenceType",
            "isMappingType", "isNumberType", "repeat", "irepeat"],
    }

    py3only_modulesymbols = {
        "abc": ["get_cache_token"],
        "contextlib": ["supress"],
        "filecmp": ["clear_cache"],
        "functools": ["partialmethod"],
        "gc": ["get_stats"],
        "glob": ["scape"],
        "hashlib": ["pbkdf2_hmac"],
        "html": ["unscape"],
        "inspect": ["signature", "Parameter", "BoundArguments", "getclosurevars"],
        "multiprocessing": ["spawn", "forkserver"],
        "operator": ["length_hint"],
        "os": ["get_inheritable", "set_inheritable", "get_handle_inheritable",
            "set_handle_inheritable", "sendfile", "pipe2", "getcwdu"],
        r"past\.utils": ["old_div"],
        "poplib": ["capa", "stsl"],
        "re": ["fullmatch"],
        "resource": ["prlimit"],
        "shutil": ["disk_usage"],
        "signal": ["pthread_sigmask", "pthread_kill", "sigpending", "sigwait",
                   "sigwaitinfo", "sigtimedwait"],
        "socket": ["sendmsg", "recvmsg", "recvmsg_info"],
        "ssl": ["create_default_context", "get_default_verify_paths"],
        "struct": ["iter_unpack"],
        "sys": ["getallocatedblocks", "implementation", "maxsize", "exc_info"],
        "textwrap": ["indent"],
        "time": ["get_clock_info", "monotonic", "perf_counter", "process_time"],
        "traceback": ["clear_frames"],
        "types": ["MappingProxyType", "new_class", "prepare_class"],
        "weakref": ["WeakMethod", "finalize"],
        r"xml\.etree": ["XMLPullParser"],
        "zlib": ["ZLIB_RUNTIME_VERSION"],
    }

    strregex_import = r"^\s+from\s+%s\s+import\s+(%s)(\s+|,|$).*"
    strregex_usage = r".*(\s+|,|:|;)%s\.(%s)(\s+|,|:).*"

    for modname, symbollist in six.iteritems(py3only_modulesymbols):
        PY3MODULESYMBOLS_REGEXPS.append(re.compile(
            strregex_import % (modname, "|".join(symbollist)) + "|" +
            strregex_usage % (modname, "|".join(symbollist)),
            re.MULTILINE
        ))

    for modname, symbollist in six.iteritems(py2only_modulesymbols):
        PY2MODULESYMBOLS_REGEXPS.append(re.compile(
            strregex_import % (modname, "|".join(symbollist)) + "|" +
            strregex_usage % (modname, "|".join(symbollist)),
            re.MULTILINE
        ))


# Generate compiled regexes at import time
generate_modules_regex()
generate_modulesymbols_regex()


def check_syntax_regex(code, matches):
    """
    Test for syntax elements specific of some Python version.

    Args:
        code (str): The code
        matches (List[Tuple[str, str]]): the list of matching rules. It will
        be modified in-place

    Returns:
        A tuple with the py3_score and the py2_score
    """
    py2_score = py3_score = 0

    for regtuple in PY3OTHER_REGEXP:
        m = regtuple[0].findall(code)
        if m:
            py3_score += (regtuple[1] * len(m))
            matches.append(("PY3SYNTAX_"+regtuple[0].pattern, m))

    for regtuple in PY2OTHER_REGEXP:
        m = regtuple[0].findall(code)
        if m:
            py2_score += (regtuple[1] * len(m))
            matches.append(("PY2SYNTAX_"+regtuple[0].pattern, m))

    return py2_score, py3_score

def check_modules_regex(code, matches, match_score):
    """
    Test for modules specific of some Python version.

    Args:
        code (str): The code
        matches (List[Tuple[str, str]]): the list of matching rules. It will
        be modified in-place

    Returns:
        A tuple with the py3_score and the py2_score
    """
    py2_score = py3_score = 0

    m = PY3ONLY_MODULES_REGEXP.findall(code)
    if m:
        py3_score += (match_score * len(m))
        matches.append(('PY3MODS:' + PY3ONLY_MODULES_REGEXP.pattern, m))

    m = PY2ONLY_MODULES_REGEXP.findall(code)
    if m:
        py2_score += (match_score * len(m))
        matches.append(('PY2MODS:' + PY2ONLY_MODULES_REGEXP.pattern, m))

    return py2_score, py3_score


def check_modulesymbols_regex(code, matches, symbols_score):
    """
    Test for module symbols specific of some Python version. Please note
    that this test can be very slow compared with the others since a
    lot of regular expressions are tested.

    Args:
        code (str): The code
        matches (List[Tuple[str, str]]): the list of matching rules. It will
        be modified in-place

    Returns:
        A tuple with the py3_score and the py2_score
    """
    py2_score = py3_score = 0
    for symregex in PY3MODULESYMBOLS_REGEXPS:
        m = symregex.findall(code)
        if m:
            matches.append(('PY3SYMS:' + symregex.pattern, m))
            py3_score += (symbols_score * len(m))

    # Currently this doesn't test for any py2symbols
    return py2_score, py3_score
