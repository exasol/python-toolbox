Search.setIndex({"docnames": ["api", "changelog", "design", "developer_guide/developer_guide", "developer_guide/development", "developer_guide/ideas", "github_actions/github_actions", "github_actions/security_issues", "index", "tools", "user_guide/customization", "user_guide/getting_started", "user_guide/modules/modules", "user_guide/modules/nox", "user_guide/modules/pre_commit_hooks", "user_guide/modules/sphinx/multiversion/changelog", "user_guide/modules/sphinx/multiversion/configuration", "user_guide/modules/sphinx/multiversion/context", "user_guide/modules/sphinx/multiversion/faq", "user_guide/modules/sphinx/multiversion/github_pages", "user_guide/modules/sphinx/multiversion/gitlab_pages", "user_guide/modules/sphinx/multiversion/multiversion", "user_guide/modules/sphinx/multiversion/quickstart", "user_guide/modules/sphinx/multiversion/templates", "user_guide/modules/sphinx/sphinx", "user_guide/user_guide", "user_guide/workflows"], "filenames": ["api.rst", "changelog.rst", "design.rst", "developer_guide/developer_guide.rst", "developer_guide/development.rst", "developer_guide/ideas.rst", "github_actions/github_actions.rst", "github_actions/security_issues.rst", "index.rst", "tools.rst", "user_guide/customization.rst", "user_guide/getting_started.rst", "user_guide/modules/modules.rst", "user_guide/modules/nox.rst", "user_guide/modules/pre_commit_hooks.rst", "user_guide/modules/sphinx/multiversion/changelog.rst", "user_guide/modules/sphinx/multiversion/configuration.rst", "user_guide/modules/sphinx/multiversion/context.rst", "user_guide/modules/sphinx/multiversion/faq.rst", "user_guide/modules/sphinx/multiversion/github_pages.rst", "user_guide/modules/sphinx/multiversion/gitlab_pages.rst", "user_guide/modules/sphinx/multiversion/multiversion.rst", "user_guide/modules/sphinx/multiversion/quickstart.rst", "user_guide/modules/sphinx/multiversion/templates.rst", "user_guide/modules/sphinx/sphinx.rst", "user_guide/user_guide.rst", "user_guide/workflows.rst"], "titles": ["\ud83e\uddf0 API Reference", "\ud83d\udcdd Changelog", "\ud83d\udcd7 Design Document", "\ud83d\udee0 Developer Guide", "\ud83d\udea7 Development - Contributing", "\ud83d\udccb Ideas", "\ud83e\uddba Github Actions", "security-issues", "Exasol Toolbox", "\ud83d\udcbb Tools", "\ud83d\udd27 Customization", "\ud83d\udea6 Getting Started", "\ud83d\udce6 Modules", "nox", "pre_commit_hooks", "Changelog", "Configuration", "HTML Context", "Frequently Asked Questions", "Hosting on GitHub Pages", "Hosting on GitLab Pages", "sphinx-multiversion", "Quickstart", "Templates", "sphinx", "\ud83d\udc64 User Guide", "\ud83c\udfd7\ufe0f Workflows (CI/CD)"], "terms": {"sourc": [0, 4, 10, 11, 13, 14, 15, 16, 20, 21], "imgflip": [0, 4, 10, 13, 14], "com": [0, 4, 5, 10, 11, 13, 14, 20], "secur": [1, 5, 6], "command": [1, 2, 9, 15, 21, 26], "issu": [1, 2, 4, 5, 6, 15, 18], "action": [1, 4, 7, 11], "first": [1, 2, 19, 20, 22], "version": [1, 4, 5, 11, 16, 19, 21, 22], "tbx": [1, 9, 11], "cli": [1, 11], "tool": [1, 2, 5, 7, 20, 21], "support": [1, 5, 18, 22, 23, 26], "manag": [1, 2, 8], "github": [1, 2, 4, 5, 11, 21, 26], "workflow": [1, 4, 5, 7, 8, 25], "autogener": 1, "comment": 1, "py": [1, 2, 5, 11, 15, 16, 17, 18, 20, 22], "better": 1, "clariti": 1, "updat": [1, 2, 5, 15, 20, 26], "depend": [1, 2, 7, 20], "templat": [1, 2, 5, 18, 21, 22], "metric": [1, 11, 26], "nox": [1, 2, 11, 12, 25], "task": [1, 5, 8, 13, 20], "": [1, 2, 4, 5, 7, 9, 11, 15, 16, 17, 18, 21, 23, 26], "report": [1, 2, 5, 7, 11, 15, 26], "which": [1, 2, 4, 7, 11, 15, 16, 17, 18], "gener": [1, 2, 5, 11, 15, 16, 18, 19, 20, 22, 25], "call": [1, 2, 7, 15, 20], "invoc": [1, 15], "standard": [1, 2, 8, 11], "ci": [1, 2, 4, 15, 25], "cd": [1, 2, 4, 16, 25], "pr": [1, 2, 5], "merg": [1, 2], "scriv": 1, "custom": [1, 22, 23, 25], "path": [1, 2, 11, 15, 16, 18, 20], "filter": 1, "config": [1, 2, 5, 11, 15, 16], "object": [1, 2, 11, 21], "basic": [1, 2], "file": [1, 2, 15, 16, 18, 19, 22, 23, 26], "addit": [1, 2, 5, 7, 15, 20, 21], "project": [1, 2, 4, 7, 8, 16, 22, 25], "metadata": [1, 16, 18], "migrat": 1, "exasol": [1, 2, 5, 7, 11, 26], "organ": [1, 26], "initi": [1, 15, 21], "releas": [1, 2, 3, 8, 15, 17, 21, 22, 26], "unifi": 2, "i": [2, 5, 7, 9, 11, 15, 16, 17, 20, 21, 22], "just": [2, 11, 18, 19, 22], "step": [2, 7], "when": [2, 15, 16, 20], "come": 2, "reduc": 2, "cognit": 2, "administr": 2, "overhead": 2, "maintain": [2, 26], "work": [2, 5, 11, 15, 16, 19, 22, 26], "As": [2, 16, 23], "natur": 2, "next": [2, 22], "common": [2, 5, 7, 16], "develop": [2, 5, 16, 17, 20, 21, 22], "e": [2, 15, 18], "g": [2, 15, 16, 18], "mainten": 2, "those": 2, "need": [2, 4, 7, 11, 16, 19, 20, 22, 23, 26], "simplifi": [2, 26], "order": [2, 4, 7, 11, 16, 26], "keep": 2, "complex": [2, 16], "effort": 2, "thi": [2, 7, 11, 15, 16, 17, 18, 19, 20, 21, 23, 26], "serv": 2, "simplif": 2, "provid": [2, 7, 9, 16, 18, 19, 21], "dev": [2, 11], "configur": [2, 5, 6, 8, 15, 17, 18, 21, 22], "base": [2, 7, 11], "autom": [2, 11], "It": [2, 16, 17, 18, 26], "obviou": 2, "each": [2, 15, 16, 18], "exactli": 2, "same": [2, 16], "we": 2, "deal": 2, "specif": [2, 5, 7, 9, 11, 20], "still": 2, "front": 2, "end": [2, 11], "build": [2, 8, 11, 15, 18, 20, 21, 22, 26], "etc": [2, 5, 18], "should": [2, 11, 16, 19, 20, 26], "look": [2, 16, 18, 19, 20, 22, 23], "mai": [2, 7, 16, 18, 20, 26], "have": [2, 16, 18, 19, 20, 21, 22, 23, 26], "ideal": 2, "reus": 2, "exist": [2, 15, 16, 17, 18], "block": [2, 23], "mainli": 2, "three": 2, "main": [2, 15, 26], "purpos": [2, 21], "librari": 2, "code": [2, 7, 8, 11, 15, 18, 21], "script": [2, 11, 19, 20], "within": [2, 16], "python": [2, 5, 7, 8, 9, 11, 15, 16, 20, 26], "commonli": 2, "requir": [2, 7, 11, 16, 20, 26], "function": [2, 13, 14, 15, 21], "appli": [2, 7, 18, 21], "formatt": 2, "lint": [2, 8, 11], "type": [2, 5, 7, 8, 11, 19, 26], "check": [2, 5, 7, 8, 11, 15, 16, 18, 20, 22, 26], "run": [2, 7, 11, 16, 18, 20, 22, 26], "unit": [2, 8, 11], "test": [2, 8, 11, 20], "integr": [2, 8, 11, 20], "determin": [2, 15, 16, 17], "coverag": [2, 8, 11], "open": [2, 11, 18, 26], "clean": [2, 11, 16], "verifi": [2, 26], "publish": [2, 4, 8, 20, 21, 26], "enforc": 2, "set": [2, 3, 9, 11, 16], "co": 2, "usag": [2, 6], "exampl": [2, 4, 6, 11, 16, 18, 22, 23], "thought": 2, "onli": [2, 7, 11, 16, 19, 20, 22], "import": [2, 11, 15, 17, 26], "us": [2, 7, 11, 15, 16, 17, 18, 19, 20, 21, 22, 26], "non": [2, 15], "convent": 2, "over": [2, 16, 17], "Being": 2, "abl": [2, 16, 20, 22], "assum": [2, 22], "significantli": 2, "alwai": [2, 9, 15, 16, 18, 20], "can": [2, 7, 8, 11, 16, 17, 18, 19, 22, 23], "done": [2, 19, 22], "easili": [2, 19, 26], "more": [2, 16], "practic": 2, "transit": 2, "extens": [2, 8, 15, 16, 18, 21, 22], "point": [2, 9, 11], "hook": [2, 5, 8, 14], "where": [2, 15, 17], "behaviour": [2, 11, 18, 20], "If": [2, 9, 11, 15, 16, 17, 19, 20, 22, 23, 26], "t": [2, 15, 16, 18, 22], "someth": 2, "complic": 2, "implement": [2, 11], "you": [2, 11, 16, 17, 18, 19, 20, 22, 23, 26], "case": [2, 7, 15, 16, 18], "least": [2, 11], "one": [2, 23], "kiss": 2, "stupid": 2, "simpl": 2, "shall": [2, 7, 21], "add": [2, 5, 7, 15, 18, 19, 20, 22, 23], "burden": 2, "top": 2, "try": [2, 16], "much": 2, "possibl": [2, 16, 21], "built": [2, 11, 16, 17, 20], "ar": [2, 7, 9, 11, 15, 16, 17, 20, 21], "alreadi": [2, 7, 19, 22, 26], "relat": [2, 13], "address": 2, "extend": [2, 23], "sphinx": [2, 11, 12, 15, 16, 17, 19, 20, 22, 23, 25], "clear": 2, "everyth": [2, 16, 19], "right": [2, 21], "from": [2, 4, 11, 15, 16, 18, 20, 21, 26], "begin": [2, 4], "continu": [2, 20, 26], "improv": [2, 18], "yagni": 2, "ain": 2, "gonna": 2, "featur": 2, "thei": 2, "explicitli": [2, 11], "everi": [2, 7, 20, 26], "singl": [2, 11, 16], "like": [2, 13, 16, 19], "rather": [2, 7], "onc": 2, "second": [2, 20], "make": [2, 7, 15, 16, 22, 26], "sens": 2, "move": [2, 16, 20], "two": [2, 7, 15, 16, 20], "also": [2, 16, 17, 18, 19, 21, 22, 23], "clearli": 2, "show": [2, 22, 26], "dealt": 2, "soc": 2, "separ": [2, 18, 21, 22], "concern": 2, "due": 2, "differ": [2, 15, 22], "cover": 2, "achiev": 2, "outcom": 2, "boundari": 2, "made": [2, 16], "establish": 2, "infrastructur": [2, 11], "assembl": 2, "orchestr": 2, "execut": [2, 7], "The": [2, 5, 7, 8, 9, 13, 16, 17, 18, 20, 21, 26], "actual": [2, 15, 18], "an": [2, 9, 11, 15, 16, 17, 20, 23], "individu": [2, 16], "defin": [2, 11, 13], "ani": [2, 11, 16, 18, 19, 21], "machin": 2, "appropri": [2, 4], "environ": [2, 3, 5, 16, 20, 26], "iter": [2, 11, 17], "want": [2, 16, 18, 22, 23, 26], "approach": 2, "ad": [2, 5, 15, 19, 23], "new": [2, 4, 16, 22], "instruct": 2, "automag": 2, "und": 2, "sync": 2, "whenev": 2, "toolbox": [2, 5, 7, 9], "get": [2, 17, 25], "pyproject": [2, 11], "toml": [2, 11], "dynam": 2, "part": [2, 18], "noxconfig": [2, 5, 11], "obei": 2, "what": [2, 16, 20], "been": [2, 16, 21], "agre": 2, "upon": 2, "styleguid": 2, "runner": [2, 5, 11, 20], "known": 2, "notifi": 2, "other": [2, 16, 21, 23], "lead": [2, 4, 15], "unexpect": 2, "fact": 2, "job": [2, 7, 20, 26], "queue": 2, "therefor": [2, 7], "all": [2, 11, 15, 16, 17, 21, 22, 26], "multipl": [2, 16, 22], "time": 2, "receiv": 2, "session": [2, 11], "argument": [2, 15], "isn": 2, "annot": [2, 11], "wa": [2, 4, 15, 21], "chosen": 2, "becaus": [2, 15, 18, 20], "straightforward": 2, "compact": 2, "coupl": 2, "our": 2, "so": [2, 18, 21, 23], "team": 2, "familiar": 2, "author": 2, "veri": 2, "That": 2, "said": 2, "depth": 2, "evalu": [2, 16], "haven": 2, "itself": [2, 5, 7], "diagram": [2, 5], "noxfil": [2, 5, 11], "descript": [2, 7, 26], "fix": [2, 4, 11, 15], "linter": [2, 11], "checker": [2, 11], "doc": [2, 5, 11, 16, 17, 19, 20, 22, 23, 26], "remov": [2, 11, 16, 20], "folder": [2, 11, 20, 26], "interact": [2, 5, 16], "yml": [2, 4, 19, 26], "consist": 2, "gh": [2, 26], "page": [2, 17, 21, 23, 26], "up": [2, 3, 22, 23], "poetri": [2, 4, 11, 26], "design": [3, 5], "document": [3, 5, 11, 15, 16, 17, 18, 20, 21, 22, 23, 26], "motiv": 3, "overview": 3, "contribut": [3, 7], "creat": [3, 7, 9, 11, 19, 22, 23], "idea": [3, 6], "chang": [4, 5, 7, 20, 23], "log": [4, 15], "date": [4, 23], "latest": [4, 7, 8, 17, 20, 23], "match": [4, 15, 16, 17], "packag": [4, 13, 14, 16], "tag": [4, 15, 17, 20, 21, 22, 26], "changelog": [4, 5, 21], "For": [4, 16, 18, 19, 20, 22, 23], "0": [4, 7, 11, 16, 19, 20, 23], "4": [4, 23], "changes_0": 4, "md": 4, "In": [4, 7, 11, 14, 16, 17, 18, 23], "must": [4, 16, 21], "push": [4, 19, 26], "further": 4, "detail": [4, 5, 7, 9, 19, 20, 22], "see": [4, 5, 7, 16, 19, 22], "local": [4, 11, 15, 16, 18, 22], "number": [4, 15], "git": [4, 11, 14, 15, 16, 18, 19], "x": 4, "y": [4, 20], "z": 4, "origin": [4, 5, 16, 19, 20], "delet": 4, "d": [4, 5, 16], "remot": [4, 15, 18, 20, 21, 22], "start": [4, 25], "process": [4, 15, 16], "finish": [4, 5], "redo": 4, "manual": 4, "scenario": 4, "successfulli": [4, 20], "pypi": [4, 26], "upload": 4, "got": 4, "interrupt": [4, 21], "solut": 4, "entri": [5, 9, 11], "locat": 5, "home": 5, "rst": [5, 23], "line": [5, 7, 9, 11, 15, 16], "149": 5, "180": 5, "github_act": 5, "security_issu": 5, "94": 5, "consid": [5, 7], "adapt": [5, 7, 18], "cve": [5, 7], "format": [5, 6, 8, 11, 21], "input": [5, 6], "here": [5, 7, 8, 16], "99": 5, "commit": [5, 14, 16, 18, 19], "how": [5, 16], "setup": 5, "multivers": [5, 11, 12, 15, 16, 19, 20, 22, 23, 24], "cleanup": 5, "pre": [5, 13, 21], "instal": [5, 11, 20, 26], "pre_commit_hook": [5, 12, 25], "http": [5, 7, 11, 19, 20, 26], "serial": 5, "uid": 5, "repetit": 5, "prepar": [5, 25], "yaml": [5, 11], "helper": 5, "convert": [5, 7], "list": [5, 11, 16, 18, 20, 21, 22], "name": [7, 11, 15, 16, 17, 20, 21, 22, 23, 26], "repositori": [7, 15, 18, 20, 26], "schedul": [7, 26], "dai": [7, 26], "00": [7, 26], "crontab": [7, 26], "guru": [7, 26], "cron": [7, 26], "report_security_issu": 7, "ubuntu": 7, "permiss": 7, "write": [7, 18], "scm": 7, "checkout": [7, 9, 19], "v4": [7, 11], "6": 7, "maven": 7, "cat": [7, 15, 20], "json": [7, 11, 18], "secret": [7, 26], "github_token": [7, 19], "expos": [7, 17], "3": [7, 8, 23, 26], "paramet": [7, 16], "section": 7, "below": [7, 23], "workspac": [7, 8, 11], "sure": [7, 11, 15, 16, 22, 26], "specifi": [7, 11, 15, 20, 21], "context": [7, 15, 16, 18, 21], "output": [7, 11, 15, 18, 19, 21, 23], "current": [7, 16, 17, 18, 23], "avail": [7, 16, 17, 20, 21, 26], "oss": 7, "plugin": [7, 21], "pass": [7, 15, 16], "through": [7, 15, 26], "expect": 7, "intput": 7, "jsonl": 7, "follow": [7, 11, 16, 17, 20, 21, 22, 23, 26], "form": [7, 21], "id": [7, 11], "cwe": 7, "multilin": 7, "string": [7, 16, 17], "coordin": 7, "refer": [7, 16, 20], "url": [7, 17, 19, 20, 21, 22, 23], "futur": [7, 15], "than": 7, "your": [7, 11, 16, 18, 19, 22, 23], "own": [7, 15], "temporari": [7, 15, 16, 18], "enabl": [7, 11, 26], "queri": 7, "central": 8, "upgrad": 8, "mang": 8, "core": 8, "verif": 8, "event": [8, 21], "8": [8, 19, 20], "pip": [8, 20], "found": [8, 15, 17], "ship": 9, "whose": 9, "structur": [9, 16], "tree": 9, "manner": 9, "along": [9, 16], "matter": 9, "nest": 9, "subcommand": 9, "subsubcommand": 9, "suffici": 9, "accord": [9, 16], "subsect": 9, "bellow": [9, 11, 26], "isssu": 9, "noth": [9, 11], "avial": 9, "yet": [9, 22], "group": 11, "html": [11, 16, 18, 19, 20, 21, 22, 23], "echo": 11, "m": [11, 15, 19], "root": [11, 15, 18, 20], "contain": [11, 13, 14, 15, 16, 21], "modul": [11, 15, 25], "constant": 11, "project_config": 11, "attribut": [11, 17], "version_fil": 11, "altern": 11, "adjust": 11, "valu": [11, 15, 16, 17], "__future__": 11, "dataclass": 11, "pathlib": 11, "mutablemap": 11, "frozen": 11, "true": [11, 16, 17, 19], "class": [11, 16, 23], "__file__": 11, "parent": [11, 16], "path_filt": 11, "str": [11, 16], "dist": 11, "egg": 11, "venv": 11, "staticmethod": 11, "def": 11, "pre_integration_tests_hook": 11, "_session": 11, "_config": 11, "_context": 11, "bool": [11, 16], "return": [11, 15, 17], "post_integration_tests_hook": 11, "properli": [11, 15], "fail_und": 11, "pylint": 11, "fail": 11, "under": [11, 18, 21], "mypi": 11, "overrid": [11, 15, 21], "relative_fil": 11, "15": 11, "black": 11, "length": 11, "88": 11, "verbos": 11, "fals": [11, 16, 17, 19], "includ": [11, 16, 20, 21, 22], "pyi": 11, "isort": 11, "profil": 11, "force_grid_wrap": 11, "master": [11, 16, 17, 19, 20, 26], "color": 11, "text": [11, 21], "txt": [11, 20], "max": 11, "800": 11, "ignore_error": 11, "via": [11, 16], "them": [11, 16, 18, 26], "straight": 11, "forward": [11, 15], "target": [11, 21], "disabl": [11, 19], "wildcard": 11, "unus": 11, "default": [11, 16, 20, 22, 23], "option": [11, 16], "default_stag": 11, "repo": 11, "pass_filenam": 11, "languag": 11, "system": 11, "rev": 11, "fixer": 11, "trail": 11, "whitespac": 11, "readi": 11, "With": [11, 22], "l": 11, "path_to_your_project": 11, "collect": 11, "summari": 11, "mark": 11, "select": [11, 16], "skip": [11, 15, 16], "enjoi": 11, "similar": [14, 17], "directori": [15, 18, 19, 20, 21, 23], "miss": 15, "error": [15, 18], "window": 15, "18": 15, "bug": 15, "tri": 15, "load": 15, "conf": [15, 16, 17, 18, 20, 22], "instead": [15, 17, 18, 23, 26], "could": [15, 22], "problem": 15, "13": 15, "wrong": 15, "__main__": 15, "prevent": [15, 16], "sphinx_multivers": [15, 22], "23": 15, "failur": 15, "find": [15, 16], "ref": [15, 16], "invok": [15, 16], "24": 15, "25": 15, "26": 15, "resolv": 15, "being": [15, 17], "reload": 15, "pars": 15, "now": [15, 19, 22], "perform": 15, "subprocess": 15, "do": [15, 19, 26], "interpret": 15, "flag": [15, 16, 18], "isol": 15, "mode": 15, "22": 15, "28": 15, "30": 15, "36": 15, "rewrit": 15, "handl": 15, "branch": [15, 17, 20, 21, 22, 26], "slash": 15, "unittest": 15, "doesn": 15, "break": 15, "31": [15, 26], "35": 15, "exit": 15, "zero": 15, "statu": 15, "were": [15, 19], "some": [15, 16, 18], "both": [15, 16, 21], "automat": [15, 16, 18], "copi": [15, 16, 18], "9": 15, "absolut": 15, "vpathto": [15, 17, 21, 23], "ensur": 15, "rel": [15, 16, 17, 19, 20], "wai": [15, 16, 20, 21], "variabl": [15, 18, 20, 21, 22], "placehold": [15, 16], "expand": 15, "7": [15, 16, 26], "caus": [15, 18, 21], "c": [15, 21, 26], "read": [16, 18, 23], "usual": 16, "certain": [16, 22], "var": 16, "none": [16, 18], "ignor": [16, 26], "smv_tag_whitelist": 16, "r": [16, 20], "smv_branch_whitelist": 16, "smv_remote_whitelist": [16, 20], "smv_released_pattern": [16, 17], "insid": [16, 22], "smv_outputdir_format": 16, "whether": [16, 21], "prefer": 16, "dir": [16, 19], "conflict": 16, "smv_prefer_remote_ref": 16, "befor": 16, "smv_prebuild_command": 16, "doxygen": 16, "regular": [16, 17], "express": [16, 17, 21], "export": [16, 20], "outputdir": 16, "after": 16, "smv_prebuild_export_pattern": 16, "subdirectori": 16, "smv_prebuild_export_destin": 16, "result": 16, "artefact": [16, 23], "download": [16, 21], "smv_build_target": 16, "builder": [16, 17], "download_format": 16, "indic": 16, "intermedi": 16, "produc": 16, "smv_clean_intermediate_fil": 16, "dump": [16, 18], "don": [16, 18, 22], "v": [16, 23], "v2": 16, "1": [16, 21], "except": [16, 20], "upstream": 16, "To": [16, 19, 20, 22, 23, 26], "A": [16, 17, 20, 21], "ha": [16, 26], "allow": 16, "flexibl": 16, "regex": 16, "full": 16, "refnam": 16, "head": [16, 19, 20], "2": [16, 18, 21], "sed": 16, "necessari": [16, 18, 20], "out": [16, 18, 20, 21], "apidoc": 16, "autodoc": 16, "api": 16, "smv_postbuild_command": 16, "facilit": 16, "smv_prebuild_export_directori": 16, "equival": 16, "postbuild": 16, "prior": 16, "place": 16, "o": 16, "mymodul": 16, "doxgen": 16, "titl": [16, 19, 20], "latex": [16, 20], "pdf": [16, 20], "note": [16, 20, 23], "would": 16, "logic": 16, "smv_postbuild_export_pattern": 16, "smv_postbuild_export_destin": 16, "seper": 16, "style": 16, "hash": 16, "truncat": 16, "charact": 16, "previou": 16, "pyformat": 16, "inform": [16, 23], "static": 16, "extern": 16, "program": 16, "build_target_nam": 16, "These": [16, 20], "field": 16, "popul": [16, 20], "uniqu": 16, "dictionari": 16, "displai": 16, "identifi": 16, "valid": [16, 26], "final": 16, "tar": 16, "zip": 16, "epub": 16, "entir": 16, "archiv": 16, "avoid": 16, "ambigu": 16, "associ": 16, "illustr": 16, "limit": [16, 21], "index": [16, 17, 19, 20], "thu": 16, "gztar": 16, "bztar": 16, "xztar": 16, "singlehtml": 16, "latexpdf": 16, "addition": 16, "user": [16, 19], "resembl": 16, "example_doc": 16, "v0": 16, "howev": [16, 21], "xhtml": 16, "re": [16, 22, 23], "sinc": 16, "data": [16, 18, 19, 21, 23], "while": [16, 18], "leav": 16, "unchang": 16, "sometim": 16, "might": 16, "overid": 16, "insert": 16, "replac": 16, "correct": 16, "exhal": 16, "exhale_arg": 16, "containmentfold": 16, "sourcedir": 16, "enclos": 16, "quot": 16, "shell": 16, "treat": 16, "is_releas": [17, 21, 23], "els": [17, 23], "most": 17, "whitelist": [17, 20, 21], "yield": 17, "h3": [17, 22, 23], "ul": [17, 22, 23], "item": [17, 22, 23], "li": [17, 22, 23], "href": [17, 19, 20, 22, 23], "endfor": [17, 22, 23], "properti": 17, "\u00ecs_releas": 17, "in_develop": [17, 23], "hasdoc": 17, "vhasdoc": [17, 21], "other_vers": 17, "take": [17, 23], "anoth": 17, "endif": [17, 22, 23], "pathto": 17, "doe": [17, 23], "its": [17, 20], "master_doc": 17, "go": 17, "current_vers": [17, 21, 23], "latest_vers": [17, 21, 23], "sever": 18, "sphinxcontrib": 18, "seem": 18, "correctli": 18, "recent": 18, "march": 18, "2020": [18, 21], "Their": 18, "heavili": 18, "reli": 18, "monkei": 18, "patch": [18, 21], "intern": 18, "runtim": 18, "prone": 18, "mess": 18, "contrast": 18, "fanci": 18, "written": 18, "Then": [18, 19], "mean": 18, "theme": [18, 21, 22], "without": [18, 21, 22], "No": 18, "downsid": 18, "restrict": 18, "kind": 18, "retain": [18, 21], "compat": 18, "hardcod": 18, "older": 18, "accordingli": 18, "bsd": [18, 21], "claus": [18, 21], "jekyl": 19, "orphan": 19, "touch": 19, "nojekyl": 19, "switch": 19, "back": 19, "mkdir": 19, "fine": 19, "dirnam": 19, "mv": 19, "onlin": 19, "navig": 19, "usernam": [19, 20], "io": [19, 20], "reponam": [19, 20], "addressbar": 19, "doctyp": [19, 20], "meta": [19, 20], "charset": [19, 20], "utf": [19, 20], "equiv": [19, 20], "refresh": [19, 20], "content": [19, 20, 22, 23, 26], "link": [19, 20], "canon": [19, 20], "before_deploi": 19, "docroot": 19, "cp": 19, "asset": 19, "deploi": [19, 20], "skip_cleanup": 19, "keep_histori": 19, "local_dir": 19, "pleas": [19, 20, 23], "deploy": [19, 20, 26], "ll": 20, "pattern": [20, 21], "websit": 20, "public": 20, "site": 20, "server": 20, "accomplish": 20, "recip": 20, "artifact": 20, "compress": 20, "imag": 20, "stage": 20, "before_script": 20, "apt": 20, "texliv": 20, "latexmk": 20, "extra": 20, "docker": 20, "bash": 20, "redirect": 20, "ci_defualt_branch": 20, "eof": 20, "ci_default_branch": 20, "ci_pages_url": 20, "complet": 20, "rule": 20, "reflect": 20, "desir": 20, "dummi": 20, "predefin": 20, "domain": 20, "self": 21, "host": 21, "taken": 21, "holzhau": 21, "variou": [21, 26], "samuel": 21, "emri": 21, "fork": 21, "licens": 21, "copyright": 21, "jan": 21, "holthui": 21, "ruhr": 21, "uni": 21, "bochum": 21, "de": 21, "reserv": 21, "redistribut": 21, "binari": 21, "modif": 21, "permit": 21, "condit": 21, "met": 21, "abov": 21, "notic": 21, "disclaim": 21, "reproduc": 21, "materi": 21, "distribut": 21, "softwar": 21, "BY": 21, "THE": 21, "holder": 21, "AND": 21, "contributor": 21, "AS": 21, "OR": 21, "impli": 21, "warranti": 21, "BUT": 21, "NOT": 21, "TO": 21, "OF": 21, "merchant": 21, "fit": 21, "FOR": 21, "particular": 21, "IN": 21, "NO": 21, "BE": 21, "liabl": 21, "direct": 21, "indirect": 21, "incident": 21, "special": 21, "exemplari": 21, "consequenti": 21, "damag": 21, "procur": 21, "substitut": 21, "good": 21, "servic": 21, "loss": 21, "profit": 21, "busi": 21, "ON": 21, "theori": 21, "liabil": 21, "contract": 21, "strict": 21, "tort": 21, "neglig": 21, "otherwis": 21, "aris": 21, "even": 21, "IF": 21, "advis": 21, "SUCH": 21, "footer": 21, "big": 21, "thank": 21, "dowl": 21, "quickstart": 21, "post": 21, "banner": 21, "readthedoc": 21, "gitlab": 21, "frequent": 21, "ask": 21, "question": 21, "act": 22, "wrapper": 22, "worri": 22, "picker": 22, "tutori": 22, "_": [22, 23], "sidebar": [22, 23], "widget": [22, 23], "templates_path": [22, 23], "html_sidebar": [22, 23], "_templat": [22, 23], "rebuild": 22, "By": 22, "cater": 23, "snippet": [23, 26], "put": 23, "bodi": 23, "p": 23, "strong": 23, "old": 23, "super": 23, "endblock": 23, "div": 23, "toggl": 23, "role": 23, "aria": 23, "label": 23, "span": 23, "fa": 23, "book": 23, "caret": 23, "down": 23, "dl": 23, "dt": 23, "dd": 23, "regularli": 26, "One": 26, "trick": 26, "print": 26, "access": 26, "token": 26, "pypi_token": 26, "either": 26, "tbox": 26, "pull_request": 26, "reopen": 26, "At": 26, "7th": 26, "month": 26, "5": 26, "deliveri": 26}, "objects": {"": [[17, 0, 1, "", "current_version"], [11, 0, 1, "", "doc"], [17, 0, 1, "", "is_released"], [17, 0, 1, "", "latest_version"], [17, 0, 1, "", "name"], [17, 0, 1, "", "release"], [11, 0, 1, "", "root"], [17, 0, 1, "", "url"], [17, 0, 1, "", "version"], [11, 0, 1, "", "version_file"], [17, 0, 1, "id0", "versions"], [17, 1, 1, "", "vhasdoc"], [17, 1, 1, "", "vpathto"]], "versions": [[17, 0, 1, "", "branches"], [17, 0, 1, "", "in_development"], [17, 0, 1, "", "releases"], [17, 0, 1, "", "tags"]]}, "objtypes": {"0": "py:attribute", "1": "py:function"}, "objnames": {"0": ["py", "attribute", "Python attribute"], "1": ["py", "function", "Python function"]}, "titleterms": {"api": 0, "refer": 0, "changelog": [1, 15], "unreleas": 1, "ad": 1, "0": [1, 15, 26], "5": [1, 11], "2023": 1, "10": 1, "12": [1, 15], "chang": [1, 18], "4": [1, 11, 15], "04": [1, 15], "19": [1, 15], "remov": 1, "3": [1, 11, 15], "2022": 1, "21": 1, "2": [1, 11, 15, 26], "20": 1, "document": [1, 2, 8, 19], "1": [1, 11, 15, 26], "11": [1, 15], "25": 1, "design": 2, "motiv": 2, "overview": 2, "principl": 2, "decis": 2, "detail": 2, "task": [2, 11], "todo": [2, 5, 7], "workflow": [2, 26], "avail": [2, 11, 23], "action": [2, 6], "develop": [3, 4, 23], "guid": [3, 25], "contribut": 4, "set": [4, 19], "up": [4, 19], "environ": 4, "creat": [4, 20], "releas": [4, 16, 23], "prerequisit": [4, 8], "trigger": 4, "what": [4, 18], "do": [4, 18], "fail": 4, "The": 4, "dure": 4, "pre": [4, 11, 16], "check": 4, "One": 4, "step": 4, "partial": 4, "idea": [5, 7], "github": [6, 7, 19], "secur": 7, "issu": 7, "exampl": 7, "usag": 7, "configur": [7, 11, 16, 20, 26], "command": [7, 16], "format": [7, 16], "input": 7, "token": 7, "exasol": 8, "toolbox": [8, 11, 26], "featur": 8, "instal": 8, "tool": [9, 11, 18], "how": [9, 18], "get": [9, 11], "help": 9, "custom": 10, "start": 11, "prepar": 11, "project": [11, 20, 21, 26], "add": [11, 26], "depend": 11, "fine": 11, "tune": 11, "gitignor": 11, "file": 11, "provid": 11, "make": [11, 18], "6": 11, "setup": 11, "commit": 11, "hook": 11, "7": 11, "go": 11, "modul": 12, "nox": 13, "pre_commit_hook": 14, "version": [15, 17, 18, 23, 26], "2020": 15, "08": 15, "05": 15, "01": 15, "03": 15, "tag": [16, 18, 23], "branch": [16, 18, 19, 23], "remot": 16, "whitelist": 16, "pattern": 16, "post": 16, "build": [16, 19], "output": 16, "directori": 16, "specifi": 16, "addit": 16, "target": 16, "overrid": 16, "variabl": [16, 17], "html": 17, "context": 17, "object": 17, "function": 17, "other": 17, "frequent": 18, "ask": 18, "question": 18, "why": 18, "anoth": 18, "sphinx": [18, 21, 24], "doc": 18, "doe": 18, "work": 18, "i": 18, "need": 18, "old": 18, "ar": 18, "licens": 18, "term": 18, "multivers": [18, 21], "host": [19, 20], "page": [19, 20], "gh": 19, "redirect": 19, "from": 19, "root": 19, "autom": 19, "travi": 19, "ci": [19, 20, 26], "gitlab": 20, "your": [20, 26], "yml": 20, "link": 21, "gener": [21, 26], "appendix": 21, "quickstart": 22, "templat": 23, "list": 23, "all": 23, "separ": 23, "download": 23, "banner": 23, "readthedoc": 23, "theme": 23, "user": 25, "cd": 26, "determin": 26, "standard": 26, "pr": 26, "merg": 26}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 8, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.todo": 2, "sphinx.ext.viewcode": 1, "sphinx.ext.intersphinx": 1, "sphinx": 57}, "alltitles": {"\ud83e\uddf0 API Reference": [[0, "api-reference"]], "\ud83d\udcdd Changelog": [[1, "changelog"]], "Unreleased": [[1, "unreleased"]], "\u2728 Added": [[1, "added"], [1, "id3"], [1, "id5"], [1, "id8"], [1, "id11"]], "0.5.0 - 2023-10-12": [[1, "changelog-0-5-0"]], "\ud83d\udd27 Changed": [[1, "changed"], [1, "id6"], [1, "id9"], [1, "id12"]], "0.4.0 - 2023-04-19": [[1, "changelog-0-4-0"]], "\ud83d\uddd1 Removed": [[1, "removed"]], "0.3.0 - 2022-12-21": [[1, "changelog-0-3-0"]], "0.2.0 \u2014 2022-12-20": [[1, "changelog-0-2-0"]], "\ud83d\udcda Documentation": [[1, "documentation"], [8, "documentation"]], "0.1.0 \u2014 2022-11-25": [[1, "id13"]], "\ud83d\udcd7 Design Document": [[2, "design-document"]], "Motivation": [[2, "motivation"]], "Overview": [[2, "overview"]], "Design": [[2, "design"]], "Design Principles": [[2, "design-principles"]], "Design Decisions": [[2, "design-decisions"]], "Detailed Design": [[2, "detailed-design"]], "Tasks": [[2, "tasks"]], "Todo": [[2, "id1"], [2, "id2"], [5, null], [5, null], [5, null], [5, null], [7, "id1"], [7, "id2"]], "Workflows": [[2, "workflows"]], "Available Workflows": [[2, "available-workflows"]], "Available Actions": [[2, "available-actions"]], "\ud83d\udee0 Developer Guide": [[3, "developer-guide"]], "\ud83d\udea7 Development - Contributing": [[4, "development-contributing"]], "Setting up the Development Environment": [[4, "setting-up-the-development-environment"]], "Creating a Release": [[4, "creating-a-release"]], "Prerequisites": [[4, "prerequisites"]], "Triggering the Release": [[4, "triggering-the-release"]], "What to do if the release failed?": [[4, "what-to-do-if-the-release-failed"]], "The release failed during pre-release checks": [[4, "the-release-failed-during-pre-release-checks"]], "One of the release steps failed (Partial Release)": [[4, "one-of-the-release-steps-failed-partial-release"]], "\ud83d\udccb Ideas": [[5, "ideas"]], "\ud83e\uddba Github Actions": [[6, "github-actions"]], "security-issues": [[7, "security-issues"]], "Example Usage": [[7, "example-usage"]], "Configuration": [[7, "configuration"], [16, "configuration"]], "command": [[7, "command"]], "format": [[7, "format"]], "Input Format": [[7, "input-format"]], "github-token": [[7, "github-token"]], "Ideas": [[7, "ideas"]], "Exasol Toolbox": [[8, "exasol-toolbox"]], "\ud83d\ude80 Features": [[8, "features"]], "\ud83d\udd0c\ufe0f Prerequisites": [[8, "prerequisites"]], "\ud83d\udcbe Installation": [[8, "installation"]], "\ud83d\udcbb Tools": [[9, "tools"]], "How to get Help": [[9, "how-to-get-help"]], "\ud83d\udd27 Customization": [[10, "customization"]], "\ud83d\udea6 Getting Started": [[11, "getting-started"]], "Preparing the Project": [[11, "preparing-the-project"]], "1. Add the toolbox as dependency": [[11, "add-the-toolbox-as-dependency"]], "2. Fine tune the .gitignore file": [[11, "fine-tune-the-gitignore-file"]], "3. Provide a project configuration": [[11, "provide-a-project-configuration"]], "4. Configure the tooling": [[11, "configure-the-tooling"]], "5. Make the toolbox task available": [[11, "make-the-toolbox-task-available"]], "6. Setup the pre-commit hooks": [[11, "setup-the-pre-commit-hooks"]], "7. Go \ud83e\udd5c": [[11, "go"]], "\ud83d\udce6 Modules": [[12, "modules"]], "nox": [[13, "nox"]], "pre_commit_hooks": [[14, "pre-commit-hooks"]], "Changelog": [[15, "changelog"]], "Version 0.2": [[15, "version-0-2"]], "Version 0.2.4 (2020-08-12)": [[15, "version-0-2-4-2020-08-12"]], "Version 0.2.3 (2020-05-04)": [[15, "version-0-2-3-2020-05-04"]], "Version 0.2.2 (2020-05-01)": [[15, "version-0-2-2-2020-05-01"]], "Version 0.2.1 (2020-04-19)": [[15, "version-0-2-1-2020-04-19"]], "Version 0.2.0 (2020-04-19)": [[15, "version-0-2-0-2020-04-19"]], "Version 0.1": [[15, "version-0-1"]], "Version 0.1.1 (2020-03-12)": [[15, "version-0-1-1-2020-03-12"]], "Version 0.1.0 (2020-03-11)": [[15, "version-0-1-0-2020-03-11"]], "Tag/Branch/Remote whitelists": [[16, "tag-branch-remote-whitelists"]], "Release Pattern": [[16, "release-pattern"]], "Pre and post-build command": [[16, "pre-and-post-build-command"]], "Output Directory Format": [[16, "output-directory-format"]], "Specify Additional Build Targets": [[16, "specify-additional-build-targets"]], "Overriding Configuration Variables": [[16, "overriding-configuration-variables"]], "HTML Context": [[17, "html-context"]], "Version Objects": [[17, "version-objects"]], "Versions": [[17, "versions"]], "Functions": [[17, "functions"]], "Other Variables": [[17, "other-variables"]], "Frequently Asked Questions": [[18, "frequently-asked-questions"]], "Why another tool for versioning Sphinx docs?": [[18, "why-another-tool-for-versioning-sphinx-docs"]], "How does it work?": [[18, "how-does-it-work"]], "Do I need to make changes to old branches or tags?": [[18, "do-i-need-to-make-changes-to-old-branches-or-tags"]], "What are the license terms of sphinx-multiversion?": [[18, "what-are-the-license-terms-of-sphinx-multiversion"]], "Hosting on GitHub Pages": [[19, "hosting-on-github-pages"]], "Setting up the gh-pages Branch": [[19, "setting-up-the-gh-pages-branch"]], "Redirecting from the Document Root": [[19, "redirecting-from-the-document-root"]], "Automating documentation builds with Travis CI": [[19, "automating-documentation-builds-with-travis-ci"]], "Hosting on GitLab Pages": [[20, "hosting-on-gitlab-pages"]], "Configure your project": [[20, "configure-your-project"]], "Create .gitlab-ci.yml": [[20, "create-gitlab-ci-yml"]], "sphinx-multiversion": [[21, "sphinx-multiversion"]], "Project Links": [[21, "project-links"]], "General": [[21, null]], "Appendix": [[21, null]], "Quickstart": [[22, "quickstart"]], "Templates": [[23, "templates"]], "Version Listings": [[23, "version-listings"]], "List all branches/tags": [[23, "list-all-branches-tags"]], "List branches and tags separately": [[23, "list-branches-and-tags-separately"]], "List releases and development versions separately": [[23, "list-releases-and-development-versions-separately"]], "List available downloads": [[23, "list-available-downloads"]], "Version Banners": [[23, "version-banners"]], "ReadTheDocs Theme": [[23, "readthedocs-theme"]], "sphinx": [[24, "sphinx"]], "\ud83d\udc64 User Guide": [[25, "user-guide"]], "\ud83c\udfd7\ufe0f Workflows (CI/CD)": [[26, "workflows-ci-cd"]], "Generate CI & CI/CD workflows": [[26, "generate-ci-ci-cd-workflows"]], "0. Determine the toolbox version": [[26, "determine-the-toolbox-version"]], "1. Configure your project": [[26, "configure-your-project"]], "2. Add the standard workflows to your project": [[26, "add-the-standard-workflows-to-your-project"]], "CI Workflow": [[26, "ci-workflow"]], "CI/CD Workflow": [[26, "ci-cd-workflow"]], "PR-Merge Workflow": [[26, "pr-merge-workflow"]]}, "indexentries": {"doc": [[11, "doc"]], "root": [[11, "root"]], "version_file": [[11, "version_file"]], "branches (versions attribute)": [[17, "versions.branches"]], "built-in function": [[17, "vhasdoc"], [17, "vpathto"]], "current_version": [[17, "current_version"]], "in_development (versions attribute)": [[17, "versions.in_development"]], "is_released": [[17, "is_released"]], "latest_version": [[17, "latest_version"]], "name": [[17, "name"]], "release": [[17, "release"]], "releases (versions attribute)": [[17, "versions.releases"]], "tags (versions attribute)": [[17, "versions.tags"]], "url": [[17, "url"]], "version": [[17, "version"]], "versions": [[17, "id0"]], "vhasdoc()": [[17, "vhasdoc"]], "vpathto()": [[17, "vpathto"]]}})