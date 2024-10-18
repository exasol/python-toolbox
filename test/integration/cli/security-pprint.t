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
  >     }
  >   ]
  > }
  > EOF

Run test case

  $ tbx security pretty-print .security.json
  # Security
  
  |File|Cve|Cwe|Details|
  |---|:-:|:-:|---|
  |exasol/toolbox/sphinx/multiversion/main.py:556:16:||78|https://bandit.readthedocs.io/en/1.7.10/plugins/b602_subprocess_popen_with_shell_equals_true.html ,<br>https://cwe.mitre.org/data/definitions/78.html |
