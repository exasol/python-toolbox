Create test input

  $ cat > .security.json <<EOF
  > {
  >   "results":[
  >     {
  >       "code": "555                 subprocess.check_call(\n556                     config.smv_postbuild_command, cwd=current_cwd, shell=True\n557                 )\n558                 if config.smv_postbuild_export_pattern != \"\":\n559                     matches = find_matching_files_and_dirs(\n",
  >       "col_offset": 16,
  >       "end_col_offset": 17,
  >       "filename": "exasol/toolbox/sphinx/multiversion/main.py",
  >       "issue_confidence": "HIGH",
  >       "issue_cwe": {
  >         "id": 78,
  >         "link": "https://cwe.mitre.org/data/definitions/78.html"
  >       },
  >       "issue_severity": "HIGH",
  >       "issue_text": "subprocess call with shell=True identified, security issue.",
  >       "line_number": 556,
  >       "line_range": [
  >         555,
  >         556,
  >         557
  >       ],
  >       "more_info": "https://bandit.readthedocs.io/en/1.7.10/plugins/b602_subprocess_popen_with_shell_equals_true.html",
  >       "test_id": "B602",
  >       "test_name": "subprocess_popen_with_shell_equals_true"
  >     },
  >     {
  >       "code": "156         )\n157         subprocess.check_call(cmd, cwd=gitroot, stdout=fp)\n158         fp.seek(0)\n",
  >       "col_offset": 8,
  >       "end_col_offset": 58,
  >       "filename": "exasol/toolbox/sphinx/multiversion/git.py",
  >       "issue_confidence": "HIGH",
  >       "issue_cwe": {
  >         "id": 78,
  >         "link": "https://cwe.mitre.org/data/definitions/78.html"
  >       },
  >       "issue_severity": "LOW",
  >       "issue_text": "subprocess call - check for execution of untrusted input.",
  >       "line_number": 157,
  >       "line_range": [
  >         157
  >       ],
  >       "more_info": "https://bandit.readthedocs.io/en/1.7.10/plugins/b603_subprocess_without_shell_equals_true.html",
  >       "test_id": "B603",
  >       "test_name": "subprocess_without_shell_equals_true"
  >     },
  >     {
  >       "code": "159         with tarfile.TarFile(fileobj=fp) as tarfp:\n160             tarfp.extractall(dst)\n",
  >       "col_offset": 12,
  >       "end_col_offset": 33,
  >       "filename": "exasol/toolbox/sphinx/multiversion/git.py",
  >       "issue_confidence": "HIGH",
  >       "issue_cwe": {
  >         "id": 22,
  >         "link": "https://cwe.mitre.org/data/definitions/22.html"
  >       },
  >       "issue_severity": "HIGH",
  >       "issue_text": "tarfile.extractall used without any validation. Please check and discard dangerous members.",
  >       "line_number": 160,
  >       "line_range": [
  >         160
  >       ],
  >       "more_info": "https://bandit.readthedocs.io/en/1.7.10/plugins/b202_tarfile_unsafe_members.html",
  >       "test_id": "B202",
  >       "test_name": "tarfile_unsafe_members"
  >     }
  >   ]
  > }
  > EOF

Run test case

  $ tbx security pretty-print .security.json
  # Security
  
  |File|Cwe|Test ID|Details|
  |---|:-:|:-:|---|
  |exasol/toolbox/sphinx/multiversion/git.py:160:12:|22|B202|https://bandit.readthedocs.io/en/1.7.10/plugins/b202_tarfile_unsafe_members.html ,<br>https://cwe.mitre.org/data/definitions/22.html |
  |exasol/toolbox/sphinx/multiversion/git.py:157:8:|78|B603|https://bandit.readthedocs.io/en/1.7.10/plugins/b603_subprocess_without_shell_equals_true.html ,<br>https://cwe.mitre.org/data/definitions/78.html |
  |exasol/toolbox/sphinx/multiversion/main.py:556:16:|78|B602|https://bandit.readthedocs.io/en/1.7.10/plugins/b602_subprocess_popen_with_shell_equals_true.html ,<br>https://cwe.mitre.org/data/definitions/78.html |
