Search.setIndex({"docnames": ["api", "changelog", "design", "developer_guide/developer_guide", "developer_guide/development", "developer_guide/todos", "index", "user_guide/customization", "user_guide/getting_started", "user_guide/modules/modules", "user_guide/modules/nox", "user_guide/modules/pre_commit_hooks", "user_guide/modules/sphinx/multiversion/changelog", "user_guide/modules/sphinx/multiversion/configuration", "user_guide/modules/sphinx/multiversion/context", "user_guide/modules/sphinx/multiversion/faq", "user_guide/modules/sphinx/multiversion/github_pages", "user_guide/modules/sphinx/multiversion/gitlab_pages", "user_guide/modules/sphinx/multiversion/multiversion", "user_guide/modules/sphinx/multiversion/quickstart", "user_guide/modules/sphinx/multiversion/templates", "user_guide/modules/sphinx/sphinx", "user_guide/user_guide", "user_guide/workflows"], "filenames": ["api.rst", "changelog.rst", "design.rst", "developer_guide/developer_guide.rst", "developer_guide/development.rst", "developer_guide/todos.rst", "index.rst", "user_guide/customization.rst", "user_guide/getting_started.rst", "user_guide/modules/modules.rst", "user_guide/modules/nox.rst", "user_guide/modules/pre_commit_hooks.rst", "user_guide/modules/sphinx/multiversion/changelog.rst", "user_guide/modules/sphinx/multiversion/configuration.rst", "user_guide/modules/sphinx/multiversion/context.rst", "user_guide/modules/sphinx/multiversion/faq.rst", "user_guide/modules/sphinx/multiversion/github_pages.rst", "user_guide/modules/sphinx/multiversion/gitlab_pages.rst", "user_guide/modules/sphinx/multiversion/multiversion.rst", "user_guide/modules/sphinx/multiversion/quickstart.rst", "user_guide/modules/sphinx/multiversion/templates.rst", "user_guide/modules/sphinx/sphinx.rst", "user_guide/user_guide.rst", "user_guide/workflows.rst"], "titles": ["\ud83e\uddf0 API Reference", "\ud83d\udcdd Changelog", "\ud83d\udcd7 Design Document", "\ud83d\udee0 Developer Guide", "\ud83d\udea7 Development - Contributing", "\ud83d\udccb Todo\u2019s", "Exasol Toolbox", "\ud83d\udd27 Customization", "\ud83d\udea6 Getting Started", "\ud83d\udce6 Modules", "nox", "pre_commit_hooks", "Changelog", "Configuration", "HTML Context", "Frequently Asked Questions", "Hosting on GitHub Pages", "Hosting on GitLab Pages", "sphinx-multiversion", "Quickstart", "Templates", "sphinx", "\ud83d\udc64 User Guide", "\ud83c\udfd7\ufe0f Workflows (CI/CD)"], "terms": {"sourc": [0, 4, 7, 8, 10, 11, 12, 13, 17, 18], "imgflip": [0, 4, 7, 10, 11], "com": [0, 4, 5, 7, 8, 10, 11, 17], "support": [1, 5, 15, 19, 20, 23], "custom": [1, 19, 20, 22], "path": [1, 2, 8, 12, 13, 15, 17], "filter": 1, "config": [1, 2, 5, 8, 12, 13], "object": [1, 2, 8, 18], "basic": [1, 2], "templat": [1, 2, 5, 8, 15, 18, 19], "workflow": [1, 4, 5, 6, 22], "file": [1, 2, 12, 13, 15, 16, 19, 20, 23], "addit": [1, 2, 12, 17, 18], "project": [1, 2, 4, 6, 13, 19, 22], "metadata": [1, 13, 15], "updat": [1, 2, 5, 12, 17, 23], "depend": [1, 2, 17], "migrat": 1, "exasol": [1, 2, 5, 8, 23], "organ": [1, 23], "initi": [1, 12, 18], "releas": [1, 2, 3, 6, 12, 14, 18, 19, 23], "unifi": 2, "tool": [2, 5, 17, 18], "i": [2, 5, 8, 12, 13, 14, 17, 18, 19, 23], "just": [2, 8, 15, 16, 19], "first": [2, 16, 17, 19], "step": 2, "when": [2, 12, 13, 17, 23], "come": 2, "reduc": 2, "cognit": 2, "administr": 2, "overhead": 2, "maintain": [2, 23], "work": [2, 5, 8, 12, 13, 16, 19, 23], "As": [2, 13, 20], "natur": 2, "next": [2, 19], "common": [2, 5, 13], "develop": [2, 5, 13, 14, 17, 18, 19], "e": [2, 12, 15, 23], "g": [2, 12, 13, 15, 23], "ci": [2, 4, 12, 22], "cd": [2, 4, 13, 22], "mainten": 2, "those": 2, "need": [2, 4, 8, 13, 16, 17, 19, 20, 23], "simplifi": [2, 23], "order": [2, 4, 8, 13, 23], "keep": 2, "complex": [2, 13], "effort": 2, "manag": [2, 6], "thi": [2, 8, 12, 13, 14, 15, 16, 17, 18, 20, 23], "serv": 2, "simplif": 2, "provid": [2, 13, 15, 16, 18], "dev": [2, 8], "configur": [2, 5, 6, 12, 14, 15, 18, 19], "base": [2, 8], "which": [2, 4, 8, 12, 13, 14, 15, 23], "autom": [2, 8], "It": [2, 13, 14, 15, 23], "obviou": 2, "each": [2, 12, 13, 15], "exactli": 2, "same": [2, 13], "we": 2, "deal": 2, "specif": [2, 5, 8, 17], "still": 2, "front": 2, "end": [2, 8], "build": [2, 6, 8, 12, 15, 17, 18, 19, 23], "etc": [2, 5, 15], "should": [2, 8, 13, 16, 17, 23], "look": [2, 13, 15, 16, 17, 19, 20], "mai": [2, 13, 15, 17], "have": [2, 13, 15, 16, 17, 18, 19, 20], "ideal": 2, "reus": 2, "exist": [2, 12, 13, 14, 15], "block": [2, 20], "mainli": 2, "three": 2, "main": [2, 12, 23], "purpos": [2, 18], "librari": 2, "code": [2, 6, 8, 12, 15, 18], "script": [2, 16, 17], "command": [2, 12, 18], "within": [2, 13], "python": [2, 5, 6, 8, 12, 13, 17, 23], "commonli": 2, "requir": [2, 8, 13, 17, 23], "function": [2, 10, 11, 12, 18], "appli": [2, 15, 18], "formatt": 2, "lint": [2, 6, 8], "type": [2, 6, 8, 16, 23], "check": [2, 5, 6, 8, 12, 13, 15, 17, 19, 23], "run": [2, 8, 13, 15, 17, 19], "unit": [2, 6, 8], "test": [2, 6, 8, 17], "integr": [2, 6, 8, 17], "determin": [2, 12, 13, 14], "coverag": [2, 6, 8], "open": [2, 8, 15, 23], "clean": [2, 8, 13], "verifi": [2, 23], "pr": [2, 5], "": [2, 3, 4, 8, 12, 13, 14, 15, 18, 20, 23], "merg": 2, "publish": [2, 4, 6, 17, 18, 23], "enforc": 2, "set": [2, 3, 8, 13], "co": 2, "usag": 2, "exampl": [2, 4, 8, 13, 15, 19, 20], "thought": 2, "onli": [2, 8, 13, 16, 17, 19], "import": [2, 8, 12, 14, 23], "us": [2, 8, 12, 13, 14, 15, 16, 17, 18, 19, 23], "non": [2, 12], "convent": 2, "over": [2, 13, 14], "Being": 2, "abl": [2, 13, 17, 19], "assum": [2, 19], "significantli": 2, "alwai": [2, 12, 13, 15, 17], "can": [2, 6, 8, 13, 14, 15, 16, 19, 20], "done": [2, 16, 19], "easili": [2, 16, 23], "more": [2, 13], "practic": 2, "transit": 2, "extens": [2, 6, 12, 13, 15, 18, 19], "point": [2, 8, 23], "hook": [2, 5, 6, 11], "where": [2, 12, 14], "behaviour": [2, 8, 15, 17], "If": [2, 8, 12, 13, 14, 16, 17, 19, 20], "t": [2, 12, 13, 15, 19], "someth": 2, "complic": 2, "implement": [2, 8], "you": [2, 8, 13, 14, 15, 16, 17, 19, 20, 23], "case": [2, 12, 13, 15], "least": [2, 8], "one": [2, 20], "kiss": 2, "stupid": 2, "simpl": 2, "shall": [2, 18], "add": [2, 5, 12, 15, 16, 17, 19, 20], "burden": 2, "top": 2, "try": [2, 13], "much": 2, "possibl": [2, 13, 18], "built": [2, 8, 13, 14, 17], "ar": [2, 8, 12, 13, 14, 17, 18, 23], "alreadi": [2, 16, 19], "relat": [2, 10], "issu": [2, 4, 5, 12, 15], "address": 2, "extend": [2, 20], "sphinx": [2, 8, 9, 12, 13, 14, 16, 17, 19, 20, 22], "clear": 2, "everyth": [2, 13, 16], "right": [2, 18], "from": [2, 4, 8, 12, 13, 15, 17, 18, 23], "begin": [2, 4], "continu": [2, 17, 23], "improv": [2, 15], "gener": [2, 5, 12, 13, 15, 16, 17, 19, 22], "yagni": 2, "ain": 2, "gonna": 2, "featur": 2, "thei": 2, "explicitli": [2, 8], "everi": [2, 17, 23], "singl": [2, 8, 13], "like": [2, 10, 13, 16], "rather": 2, "onc": 2, "second": [2, 17], "make": [2, 12, 13, 19, 23], "sens": 2, "move": [2, 13, 17], "two": [2, 12, 13, 17], "also": [2, 13, 14, 15, 16, 18, 19, 20], "clearli": 2, "show": [2, 19, 23], "dealt": 2, "soc": 2, "separ": [2, 15, 18, 19], "concern": 2, "due": 2, "differ": [2, 12, 19], "cover": 2, "achiev": 2, "outcom": 2, "boundari": 2, "made": [2, 13], "establish": 2, "infrastructur": 2, "github": [2, 4, 5, 8, 18, 23], "assembl": 2, "orchestr": 2, "execut": 2, "The": [2, 5, 6, 10, 13, 14, 15, 17, 18, 23], "actual": [2, 12, 15], "an": [2, 8, 12, 13, 14, 17, 20], "individu": [2, 13], "defin": [2, 8, 10], "ani": [2, 8, 13, 15, 16, 18], "machin": 2, "appropri": [2, 4], "environ": [2, 3, 5, 13, 17, 23], "nox": [2, 8, 9, 22], "iter": [2, 8, 14], "want": [2, 13, 15, 19, 20], "approach": 2, "ad": [2, 5, 12, 16, 20], "new": [2, 4, 13, 19], "instruct": 2, "automag": 2, "und": 2, "sync": 2, "whenev": 2, "toolbox": [2, 5], "get": [2, 14, 22], "pyproject": [2, 8], "toml": [2, 8], "dynam": 2, "part": [2, 15], "noxconfig": [2, 5, 8], "py": [2, 5, 8, 12, 13, 14, 15, 17, 19], "standard": [2, 6, 8], "obei": 2, "what": [2, 13, 17], "been": [2, 13, 18], "agre": 2, "upon": 2, "styleguid": 2, "runner": [2, 5, 17], "known": 2, "call": [2, 12, 17], "notifi": 2, "other": [2, 13, 18, 20], "lead": [2, 4, 12], "unexpect": 2, "fact": 2, "job": [2, 17, 23], "queue": 2, "therefor": 2, "all": [2, 8, 12, 13, 14, 18, 19, 23], "multipl": [2, 13, 19], "time": 2, "receiv": 2, "session": [2, 8], "argument": [2, 12], "isn": 2, "annot": [2, 8], "wa": [2, 4, 12, 18], "chosen": 2, "becaus": [2, 12, 15, 17], "straightforward": 2, "compact": 2, "coupl": 2, "our": 2, "so": [2, 15, 18, 20], "team": 2, "familiar": 2, "author": 2, "veri": 2, "That": 2, "said": 2, "depth": 2, "evalu": [2, 13], "haven": 2, "itself": [2, 5], "diagram": [2, 5], "noxfil": [2, 5, 8], "descript": [2, 23], "fix": [2, 4, 8, 12], "linter": [2, 8], "checker": [2, 8], "report": [2, 8, 12], "doc": [2, 5, 8, 13, 14, 16, 17, 19, 20, 23], "remov": [2, 8, 13, 17], "folder": [2, 8, 17, 23], "interact": [2, 5, 13], "yml": [2, 4, 16, 23], "consist": 2, "gh": [2, 23], "page": [2, 14, 18, 20, 23], "up": [2, 3, 19, 20], "poetri": [2, 4, 8, 23], "design": [3, 5], "document": [3, 5, 8, 12, 13, 14, 15, 17, 18, 19, 20, 23], "motiv": 3, "overview": 3, "contribut": 3, "creat": [3, 8, 16, 19, 20], "todo": 3, "chang": [4, 5, 17, 20], "log": [4, 12], "date": [4, 20], "latest": [4, 6, 14, 17, 20], "version": [4, 5, 8, 13, 16, 18, 19], "match": [4, 12, 13, 14], "packag": [4, 10, 11, 13], "tag": [4, 12, 14, 17, 18, 19, 23], "changelog": [4, 5, 8, 18], "For": [4, 13, 15, 16, 17, 19, 20], "0": [4, 8, 13, 16, 17, 20], "4": [4, 20], "changes_0": 4, "md": 4, "In": [4, 8, 11, 13, 14, 15, 20], "must": [4, 13, 18], "push": [4, 16, 23], "further": 4, "detail": [4, 16, 17, 19], "see": [4, 13, 16, 19], "local": [4, 8, 12, 13, 15, 19], "number": [4, 12], "git": [4, 8, 11, 12, 13, 15, 16], "x": 4, "y": [4, 17], "z": 4, "origin": [4, 5, 13, 16, 17], "delet": 4, "d": [4, 5, 13], "remot": [4, 12, 15, 17, 18, 19], "start": [4, 22], "process": [4, 12, 13], "action": [4, 8], "finish": [4, 5], "redo": 4, "manual": 4, "scenario": 4, "successfulli": [4, 17], "pypi": [4, 23], "upload": 4, "got": 4, "interrupt": [4, 18], "solut": 4, "task": [5, 6, 10, 17], "entri": [5, 8], "locat": 5, "home": 5, "rst": [5, 8, 20], "line": [5, 8, 12, 13], "149": 5, "180": 5, "commit": [5, 11, 13, 15, 16], "how": [5, 13], "setup": 5, "multivers": [5, 8, 9, 12, 13, 16, 17, 19, 20, 21], "cleanup": 5, "pre": [5, 10, 18], "instal": [5, 8, 17], "pre_commit_hook": [5, 9, 22], "http": [5, 8, 16, 17, 23], "serial": 5, "uid": 5, "repetit": 5, "prepar": [5, 22], "yaml": [5, 8], "helper": 5, "convert": 5, "list": [5, 8, 13, 15, 17, 18, 19], "central": 6, "format": [6, 8, 18], "upgrad": 6, "mang": 6, "core": 6, "workspac": [6, 8], "verif": 6, "event": [6, 18], "3": [6, 20, 23], "8": [6, 8, 16, 17], "pip": [6, 17], "found": [6, 12, 14], "here": [6, 13], "group": 8, "output": [8, 12, 15, 16, 18, 20], "html": [8, 13, 15, 16, 17, 18, 19, 20], "echo": 8, "m": [8, 12, 16], "sure": [8, 12, 13, 19, 23], "root": [8, 12, 15, 17], "contain": [8, 10, 11, 12, 13, 18], "modul": [8, 12, 22], "constant": 8, "name": [8, 12, 13, 14, 17, 18, 19, 20, 23], "project_config": 8, "follow": [8, 13, 14, 17, 18, 19, 20, 23], "attribut": [8, 14], "version_fil": 8, "altern": 8, "bellow": [8, 23], "adjust": 8, "valu": [8, 12, 13, 14], "__future__": 8, "dataclass": 8, "pathlib": 8, "mutablemap": 8, "frozen": 8, "true": [8, 13, 14, 16], "class": [8, 13, 20], "__file__": 8, "parent": [8, 13], "path_filt": 8, "str": [8, 13], "dist": 8, "egg": 8, "venv": 8, "staticmethod": 8, "def": 8, "pre_integration_tests_hook": 8, "_session": 8, "_config": 8, "_context": 8, "bool": [8, 13], "return": [8, 12, 14], "post_integration_tests_hook": 8, "properli": [8, 12], "your": [8, 13, 15, 16, 19, 20], "fail_und": 8, "pylint": 8, "fail": 8, "under": [8, 15, 18], "mypi": 8, "overrid": [8, 12, 18], "15": 8, "black": 8, "length": 8, "88": 8, "verbos": 8, "fals": [8, 13, 14, 16], "includ": [8, 13, 17, 18, 19], "pyi": 8, "isort": 8, "profil": 8, "force_grid_wrap": 8, "master": [8, 13, 14, 16, 17, 23], "max": 8, "800": 8, "ignore_error": 8, "scriv": 8, "new_fragment_templ": 8, "fragment": 8, "output_fil": 8, "liter": 8, "via": [8, 13], "them": [8, 13, 15, 23], "straight": 8, "forward": [8, 12], "default": [8, 13, 17, 19, 20], "noth": 8, "specifi": [8, 12, 17, 18], "option": [8, 13], "default_stag": 8, "repo": 8, "id": 8, "pass_filenam": 8, "languag": 8, "system": 8, "rev": 8, "v4": 8, "fixer": 8, "trail": 8, "whitespac": 8, "enabl": [8, 23], "readi": 8, "With": [8, 19], "l": 8, "path_to_your_project": 8, "mark": 8, "select": [8, 13], "skip": [8, 12, 13], "enjoi": 8, "similar": [11, 14], "directori": [12, 15, 16, 17, 18, 20], "miss": 12, "cat": [12, 17], "error": [12, 15], "window": 12, "18": 12, "bug": 12, "tri": 12, "load": 12, "conf": [12, 13, 14, 15, 17, 19], "instead": [12, 14, 15, 20], "could": [12, 19], "problem": 12, "13": 12, "wrong": 12, "__main__": 12, "prevent": [12, 13], "invoc": 12, "sphinx_multivers": [12, 19], "23": 12, "failur": 12, "find": [12, 13], "ref": [12, 13, 23], "invok": [12, 13], "repositori": [12, 15, 17, 23], "24": 12, "25": 12, "26": 12, "resolv": 12, "being": [12, 14], "reload": 12, "pars": 12, "now": [12, 16, 19], "own": 12, "perform": 12, "subprocess": 12, "do": [12, 16, 23], "context": [12, 13, 15, 18], "interpret": 12, "flag": [12, 13, 15], "isol": 12, "mode": 12, "pass": [12, 13], "through": [12, 23], "22": 12, "28": 12, "30": 12, "36": 12, "rewrit": 12, "handl": 12, "branch": [12, 14, 17, 18, 19, 23], "slash": 12, "unittest": 12, "doesn": 12, "break": 12, "futur": 12, "31": [12, 23], "35": 12, "exit": 12, "zero": 12, "statu": 12, "were": [12, 16], "some": [12, 13, 15], "both": [12, 13, 18], "automat": [12, 13, 15], "copi": [12, 13, 15], "temporari": [12, 13, 15], "9": 12, "absolut": 12, "vpathto": [12, 14, 18, 20], "ensur": 12, "rel": [12, 13, 14, 16, 17], "wai": [12, 13, 17, 18], "variabl": [12, 15, 17, 18, 19], "placehold": [12, 13], "expand": 12, "7": [12, 13, 23], "caus": [12, 15, 18], "c": [12, 18, 23], "read": [13, 15, 20], "usual": 13, "certain": [13, 19], "var": 13, "none": [13, 15], "ignor": [13, 23], "smv_tag_whitelist": 13, "r": [13, 17], "smv_branch_whitelist": 13, "smv_remote_whitelist": [13, 17], "smv_released_pattern": [13, 14], "insid": [13, 19], "smv_outputdir_format": 13, "whether": [13, 18], "prefer": 13, "dir": [13, 16], "conflict": 13, "smv_prefer_remote_ref": 13, "befor": 13, "smv_prebuild_command": 13, "doxygen": 13, "regular": [13, 14], "express": [13, 14, 18], "export": [13, 17], "outputdir": 13, "after": 13, "smv_prebuild_export_pattern": 13, "subdirectori": 13, "smv_prebuild_export_destin": 13, "result": 13, "artefact": [13, 20], "download": [13, 18], "smv_build_target": 13, "builder": [13, 14], "download_format": 13, "indic": 13, "intermedi": 13, "produc": 13, "smv_clean_intermediate_fil": 13, "dump": [13, 15], "don": [13, 15, 19], "v": [13, 20], "v2": 13, "1": [13, 18], "except": [13, 17], "upstream": 13, "To": [13, 16, 17, 19, 20, 23], "A": [13, 14, 17, 18], "ha": [13, 23], "allow": 13, "flexibl": 13, "regex": 13, "full": 13, "refnam": 13, "head": [13, 16, 17], "2": [13, 15, 18], "sed": 13, "necessari": [13, 15, 17], "out": [13, 15, 17, 18], "apidoc": 13, "autodoc": 13, "api": 13, "smv_postbuild_command": 13, "facilit": 13, "along": 13, "smv_prebuild_export_directori": 13, "equival": 13, "avail": [13, 14, 17, 18, 23], "postbuild": 13, "prior": 13, "place": 13, "o": 13, "mymodul": 13, "doxgen": 13, "titl": [13, 16, 17], "latex": [13, 17], "pdf": [13, 17], "note": [13, 17, 20], "would": 13, "logic": 13, "smv_postbuild_export_pattern": 13, "smv_postbuild_export_destin": 13, "seper": 13, "structur": 13, "style": 13, "string": [13, 14], "paramet": 13, "hash": 13, "truncat": 13, "charact": 13, "previou": 13, "pyformat": 13, "inform": [13, 20], "static": 13, "extern": 13, "program": 13, "build_target_nam": 13, "These": [13, 17], "field": 13, "popul": [13, 17], "uniqu": 13, "dictionari": 13, "displai": 13, "identifi": 13, "valid": [13, 23], "final": 13, "tar": 13, "zip": 13, "epub": 13, "entir": 13, "archiv": 13, "accord": 13, "avoid": 13, "ambigu": 13, "associ": 13, "illustr": 13, "limit": [13, 18], "index": [13, 14, 16, 17], "thu": 13, "gztar": 13, "bztar": 13, "xztar": 13, "singlehtml": 13, "latexpdf": 13, "addition": 13, "user": [13, 16], "resembl": 13, "example_doc": 13, "v0": 13, "howev": [13, 18], "xhtml": 13, "re": [13, 19, 20], "sinc": 13, "data": [13, 15, 16, 18, 20], "while": [13, 15], "leav": 13, "current": [13, 14, 15, 20], "unchang": 13, "refer": [13, 17, 23], "sometim": 13, "might": 13, "overid": 13, "insert": 13, "replac": [13, 23], "correct": 13, "exhal": 13, "exhale_arg": 13, "containmentfold": 13, "sourcedir": 13, "enclos": 13, "quot": 13, "shell": 13, "treat": 13, "expos": 14, "url": [14, 16, 17, 18, 19, 20], "is_releas": [14, 18, 20], "els": [14, 20], "most": 14, "whitelist": [14, 17, 18], "yield": 14, "h3": [14, 19, 20], "ul": [14, 19, 20], "item": [14, 19, 20], "li": [14, 19, 20], "href": [14, 16, 17, 19, 20], "endfor": [14, 19, 20], "properti": 14, "\u00ecs_releas": 14, "in_develop": [14, 20], "hasdoc": 14, "vhasdoc": [14, 18], "other_vers": 14, "take": [14, 20], "anoth": 14, "endif": [14, 19, 20], "pathto": 14, "doe": [14, 20], "its": [14, 17], "master_doc": 14, "go": 14, "current_vers": [14, 18, 20], "latest_vers": [14, 18, 20], "sever": 15, "sphinxcontrib": 15, "seem": 15, "correctli": 15, "recent": 15, "march": 15, "2020": [15, 18], "Their": 15, "heavili": 15, "reli": 15, "monkei": 15, "patch": [15, 18], "intern": 15, "runtim": 15, "prone": 15, "mess": 15, "contrast": 15, "fanci": 15, "written": 15, "json": 15, "Then": [15, 16], "write": 15, "mean": 15, "theme": [15, 18, 19], "without": [15, 18, 19], "No": 15, "downsid": 15, "restrict": 15, "kind": 15, "retain": [15, 18], "compat": 15, "hardcod": 15, "older": 15, "adapt": 15, "accordingli": 15, "bsd": [15, 18], "claus": [15, 18], "disabl": 16, "jekyl": 16, "checkout": 16, "orphan": 16, "touch": 16, "nojekyl": 16, "switch": 16, "back": 16, "mkdir": 16, "fine": 16, "dirnam": 16, "mv": 16, "onlin": 16, "navig": 16, "usernam": [16, 17], "io": [16, 17], "reponam": [16, 17], "addressbar": 16, "doctyp": [16, 17], "meta": [16, 17], "charset": [16, 17], "utf": [16, 17], "equiv": [16, 17], "refresh": [16, 17], "content": [16, 17, 19, 20, 23], "link": [16, 17], "canon": [16, 17], "before_deploi": 16, "docroot": 16, "cp": 16, "asset": 16, "deploi": [16, 17], "skip_cleanup": 16, "github_token": 16, "keep_histori": 16, "local_dir": 16, "pleas": [16, 17, 20], "deploy": [16, 17, 23], "ll": 17, "pattern": [17, 18], "websit": 17, "public": 17, "site": 17, "server": 17, "accomplish": 17, "recip": 17, "artifact": 17, "compress": 17, "imag": 17, "stage": 17, "before_script": 17, "apt": 17, "texliv": 17, "latexmk": 17, "extra": 17, "txt": 17, "docker": 17, "bash": 17, "redirect": 17, "ci_defualt_branch": 17, "eof": 17, "ci_default_branch": 17, "ci_pages_url": 17, "complet": 17, "rule": 17, "reflect": 17, "desir": 17, "dummi": 17, "predefin": 17, "domain": 17, "self": 18, "host": 18, "plugin": 18, "taken": 18, "holzhau": 18, "variou": 18, "samuel": 18, "emri": 18, "fork": 18, "licens": 18, "text": 18, "copyright": 18, "jan": 18, "holthui": 18, "ruhr": 18, "uni": 18, "bochum": 18, "de": 18, "reserv": 18, "redistribut": 18, "binari": 18, "form": 18, "modif": 18, "permit": 18, "condit": 18, "met": 18, "abov": 18, "notic": 18, "disclaim": 18, "reproduc": 18, "materi": 18, "distribut": 18, "softwar": 18, "BY": 18, "THE": 18, "holder": 18, "AND": 18, "contributor": 18, "AS": 18, "OR": 18, "impli": 18, "warranti": 18, "BUT": 18, "NOT": 18, "TO": 18, "OF": 18, "merchant": 18, "fit": 18, "FOR": 18, "particular": 18, "IN": 18, "NO": 18, "BE": 18, "liabl": 18, "direct": 18, "indirect": 18, "incident": 18, "special": 18, "exemplari": 18, "consequenti": 18, "damag": 18, "procur": 18, "substitut": 18, "good": 18, "servic": 18, "loss": 18, "profit": 18, "busi": 18, "ON": 18, "theori": 18, "liabil": 18, "contract": 18, "strict": 18, "tort": 18, "neglig": 18, "otherwis": 18, "aris": 18, "even": 18, "IF": 18, "advis": 18, "SUCH": 18, "footer": 18, "big": 18, "thank": 18, "dowl": 18, "quickstart": 18, "post": 18, "target": 18, "banner": 18, "readthedoc": 18, "gitlab": 18, "frequent": 18, "ask": 18, "question": 18, "act": 19, "wrapper": 19, "worri": 19, "picker": 19, "yet": 19, "tutori": 19, "_": [19, 20], "sidebar": [19, 20], "widget": [19, 20], "templates_path": [19, 20], "html_sidebar": [19, 20], "_templat": [19, 20], "rebuild": 19, "By": 19, "cater": 20, "snippet": [20, 23], "below": 20, "put": 20, "bodi": 20, "p": 20, "strong": 20, "old": 20, "super": 20, "endblock": 20, "div": 20, "toggl": 20, "role": 20, "aria": 20, "label": 20, "span": 20, "fa": 20, "book": 20, "caret": 20, "down": 20, "dl": 20, "dt": 20, "dd": 20, "regularli": 23, "One": 23, "trick": 23, "print": 23, "access": 23, "token": 23, "pypi_token": 23, "either": 23, "secret": 23, "pull_request": 23, "reopen": 23, "schedul": 23, "At": 23, "00": 23, "7th": 23, "dai": 23, "month": 23, "crontab": 23, "guru": 23, "cron": 23, "deliveri": 23}, "objects": {"": [[14, 0, 1, "", "current_version"], [8, 0, 1, "", "doc"], [14, 0, 1, "", "is_released"], [14, 0, 1, "", "latest_version"], [14, 0, 1, "", "name"], [14, 0, 1, "", "release"], [8, 0, 1, "", "root"], [14, 0, 1, "", "url"], [14, 0, 1, "", "version"], [8, 0, 1, "", "version_file"], [14, 0, 1, "id0", "versions"], [14, 1, 1, "", "vhasdoc"], [14, 1, 1, "", "vpathto"]], "versions": [[14, 0, 1, "", "branches"], [14, 0, 1, "", "in_development"], [14, 0, 1, "", "releases"], [14, 0, 1, "", "tags"]]}, "objtypes": {"0": "py:attribute", "1": "py:function"}, "objnames": {"0": ["py", "attribute", "Python attribute"], "1": ["py", "function", "Python function"]}, "titleterms": {"api": 0, "refer": 0, "changelog": [1, 12], "unreleas": 1, "0": [1, 12, 23], "3": [1, 8, 12], "2022": 1, "12": [1, 12], "21": 1, "ad": 1, "2": [1, 8, 12, 23], "20": 1, "chang": [1, 15], "document": [1, 2, 6, 16], "1": [1, 8, 12, 23], "11": [1, 12], "25": 1, "design": 2, "motiv": 2, "overview": 2, "principl": 2, "decis": 2, "detail": 2, "task": [2, 8], "todo": [2, 5], "workflow": [2, 23], "avail": [2, 8, 20], "action": 2, "develop": [3, 4, 20], "guid": [3, 22], "contribut": 4, "set": [4, 16], "up": [4, 16], "environ": 4, "creat": [4, 17], "releas": [4, 13, 20], "prerequisit": [4, 6], "trigger": 4, "what": [4, 15], "do": [4, 15], "fail": 4, "The": 4, "dure": 4, "pre": [4, 8, 13], "check": 4, "One": 4, "step": 4, "partial": 4, "": 5, "exasol": 6, "toolbox": [6, 8, 23], "featur": 6, "instal": 6, "custom": 7, "get": 8, "start": 8, "prepar": 8, "project": [8, 17, 18, 23], "add": [8, 23], "depend": 8, "fine": 8, "tune": 8, "gitignor": 8, "file": 8, "provid": 8, "configur": [8, 13, 17, 23], "4": [8, 12], "tool": [8, 15], "5": 8, "make": [8, 15], "6": 8, "setup": 8, "commit": 8, "hook": 8, "7": 8, "go": 8, "modul": 9, "nox": 10, "pre_commit_hook": 11, "version": [12, 14, 15, 20, 23], "2020": 12, "08": 12, "05": 12, "04": 12, "01": 12, "19": 12, "03": 12, "tag": [13, 15, 20], "branch": [13, 15, 16, 20], "remot": 13, "whitelist": 13, "pattern": 13, "post": 13, "build": [13, 16], "command": 13, "output": 13, "directori": 13, "format": 13, "specifi": 13, "addit": 13, "target": 13, "overrid": 13, "variabl": [13, 14], "html": 14, "context": 14, "object": 14, "function": 14, "other": 14, "frequent": 15, "ask": 15, "question": 15, "why": 15, "anoth": 15, "sphinx": [15, 18, 21], "doc": 15, "how": 15, "doe": 15, "work": 15, "i": 15, "need": 15, "old": 15, "ar": 15, "licens": 15, "term": 15, "multivers": [15, 18], "host": [16, 17], "github": 16, "page": [16, 17], "gh": 16, "redirect": 16, "from": 16, "root": 16, "autom": 16, "travi": 16, "ci": [16, 17, 23], "gitlab": 17, "your": [17, 23], "yml": 17, "link": 18, "gener": [18, 23], "appendix": 18, "quickstart": 19, "templat": 20, "list": 20, "all": 20, "separ": 20, "download": 20, "banner": 20, "readthedoc": 20, "theme": 20, "user": 22, "cd": 23, "determin": 23, "standard": 23, "pr": 23, "merg": 23}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 8, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.todo": 2, "sphinx.ext.viewcode": 1, "sphinx.ext.intersphinx": 1, "sphinx": 57}, "alltitles": {"\ud83e\uddf0 API Reference": [[0, "api-reference"]], "\ud83d\udcdd Changelog": [[1, "changelog"]], "Unreleased": [[1, "unreleased"]], "0.3.0 - 2022-12-21": [[1, "changelog-0-3-0"]], "\u2728 Added": [[1, "added"], [1, "id4"]], "0.2.0 \u2014 2022-12-20": [[1, "changelog-0-2-0"]], "\ud83d\udd27 Changed": [[1, "changed"]], "\ud83d\udcda Documentation": [[1, "documentation"], [6, "documentation"]], "0.1.0 \u2014 2022-11-25": [[1, "id5"]], "\ud83d\udcd7 Design Document": [[2, "design-document"]], "Motivation": [[2, "motivation"]], "Overview": [[2, "overview"]], "Design": [[2, "design"]], "Design Principles": [[2, "design-principles"]], "Design Decisions": [[2, "design-decisions"]], "Detailed Design": [[2, "detailed-design"]], "Tasks": [[2, "tasks"]], "Todo": [[2, "id1"], [2, "id2"], [5, null], [5, null]], "Workflows": [[2, "workflows"]], "Available Workflows": [[2, "available-workflows"]], "Available Actions": [[2, "available-actions"]], "\ud83d\udee0 Developer Guide": [[3, "developer-guide"]], "\ud83d\udea7 Development - Contributing": [[4, "development-contributing"]], "Setting up the Development Environment": [[4, "setting-up-the-development-environment"]], "Creating a Release": [[4, "creating-a-release"]], "Prerequisites": [[4, "prerequisites"]], "Triggering the Release": [[4, "triggering-the-release"]], "What to do if the release failed?": [[4, "what-to-do-if-the-release-failed"]], "The release failed during pre-release checks": [[4, "the-release-failed-during-pre-release-checks"]], "One of the release steps failed (Partial Release)": [[4, "one-of-the-release-steps-failed-partial-release"]], "\ud83d\udccb Todo\u2019s": [[5, "todo-s"]], "Exasol Toolbox": [[6, "exasol-toolbox"]], "\ud83d\ude80 Features": [[6, "features"]], "\ud83d\udd0c\ufe0f Prerequisites": [[6, "prerequisites"]], "\ud83d\udcbe Installation": [[6, "installation"]], "\ud83d\udd27 Customization": [[7, "customization"]], "\ud83d\udea6 Getting Started": [[8, "getting-started"]], "Preparing the Project": [[8, "preparing-the-project"]], "1. Add the toolbox as dependency": [[8, "add-the-toolbox-as-dependency"]], "2. Fine tune the .gitignore file": [[8, "fine-tune-the-gitignore-file"]], "3. Provide a project configuration": [[8, "provide-a-project-configuration"]], "4. Configure the tooling": [[8, "configure-the-tooling"]], "5. Make the toolbox task available": [[8, "make-the-toolbox-task-available"]], "6. Setup the pre-commit hooks": [[8, "setup-the-pre-commit-hooks"]], "7. Go \ud83e\udd5c": [[8, "go"]], "\ud83d\udce6 Modules": [[9, "modules"]], "nox": [[10, "nox"]], "pre_commit_hooks": [[11, "pre-commit-hooks"]], "Changelog": [[12, "changelog"]], "Version 0.2": [[12, "version-0-2"]], "Version 0.2.4 (2020-08-12)": [[12, "version-0-2-4-2020-08-12"]], "Version 0.2.3 (2020-05-04)": [[12, "version-0-2-3-2020-05-04"]], "Version 0.2.2 (2020-05-01)": [[12, "version-0-2-2-2020-05-01"]], "Version 0.2.1 (2020-04-19)": [[12, "version-0-2-1-2020-04-19"]], "Version 0.2.0 (2020-04-19)": [[12, "version-0-2-0-2020-04-19"]], "Version 0.1": [[12, "version-0-1"]], "Version 0.1.1 (2020-03-12)": [[12, "version-0-1-1-2020-03-12"]], "Version 0.1.0 (2020-03-11)": [[12, "version-0-1-0-2020-03-11"]], "Configuration": [[13, "configuration"]], "Tag/Branch/Remote whitelists": [[13, "tag-branch-remote-whitelists"]], "Release Pattern": [[13, "release-pattern"]], "Pre and post-build command": [[13, "pre-and-post-build-command"]], "Output Directory Format": [[13, "output-directory-format"]], "Specify Additional Build Targets": [[13, "specify-additional-build-targets"]], "Overriding Configuration Variables": [[13, "overriding-configuration-variables"]], "HTML Context": [[14, "html-context"]], "Version Objects": [[14, "version-objects"]], "Versions": [[14, "versions"]], "Functions": [[14, "functions"]], "Other Variables": [[14, "other-variables"]], "Frequently Asked Questions": [[15, "frequently-asked-questions"]], "Why another tool for versioning Sphinx docs?": [[15, "why-another-tool-for-versioning-sphinx-docs"]], "How does it work?": [[15, "how-does-it-work"]], "Do I need to make changes to old branches or tags?": [[15, "do-i-need-to-make-changes-to-old-branches-or-tags"]], "What are the license terms of sphinx-multiversion?": [[15, "what-are-the-license-terms-of-sphinx-multiversion"]], "Hosting on GitHub Pages": [[16, "hosting-on-github-pages"]], "Setting up the gh-pages Branch": [[16, "setting-up-the-gh-pages-branch"]], "Redirecting from the Document Root": [[16, "redirecting-from-the-document-root"]], "Automating documentation builds with Travis CI": [[16, "automating-documentation-builds-with-travis-ci"]], "Hosting on GitLab Pages": [[17, "hosting-on-gitlab-pages"]], "Configure your project": [[17, "configure-your-project"]], "Create .gitlab-ci.yml": [[17, "create-gitlab-ci-yml"]], "sphinx-multiversion": [[18, "sphinx-multiversion"]], "Project Links": [[18, "project-links"]], "General": [[18, null]], "Appendix": [[18, null]], "Quickstart": [[19, "quickstart"]], "Templates": [[20, "templates"]], "Version Listings": [[20, "version-listings"]], "List all branches/tags": [[20, "list-all-branches-tags"]], "List branches and tags separately": [[20, "list-branches-and-tags-separately"]], "List releases and development versions separately": [[20, "list-releases-and-development-versions-separately"]], "List available downloads": [[20, "list-available-downloads"]], "Version Banners": [[20, "version-banners"]], "ReadTheDocs Theme": [[20, "readthedocs-theme"]], "sphinx": [[21, "sphinx"]], "\ud83d\udc64 User Guide": [[22, "user-guide"]], "\ud83c\udfd7\ufe0f Workflows (CI/CD)": [[23, "workflows-ci-cd"]], "Generate CI & CI/CD workflows": [[23, "generate-ci-ci-cd-workflows"]], "0. Determine the toolbox version": [[23, "determine-the-toolbox-version"]], "1. Configure your project": [[23, "configure-your-project"]], "2. Add the standard workflows to your project": [[23, "add-the-standard-workflows-to-your-project"]], "CI Workflow": [[23, "ci-workflow"]], "CI/CD Workflow": [[23, "ci-cd-workflow"]], "PR-Merge Workflow": [[23, "pr-merge-workflow"]]}, "indexentries": {"doc": [[8, "doc"]], "root": [[8, "root"]], "version_file": [[8, "version_file"]], "branches (versions attribute)": [[14, "versions.branches"]], "built-in function": [[14, "vhasdoc"], [14, "vpathto"]], "current_version": [[14, "current_version"]], "in_development (versions attribute)": [[14, "versions.in_development"]], "is_released": [[14, "is_released"]], "latest_version": [[14, "latest_version"]], "name": [[14, "name"]], "release": [[14, "release"]], "releases (versions attribute)": [[14, "versions.releases"]], "tags (versions attribute)": [[14, "versions.tags"]], "url": [[14, "url"]], "version": [[14, "version"]], "versions": [[14, "id0"]], "vhasdoc()": [[14, "vhasdoc"]], "vpathto()": [[14, "vpathto"]]}})