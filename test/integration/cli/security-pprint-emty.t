Create test input

  $ cat > .security.json <<EOF
  > {
  >   "result":[
  >   ]
  > }
  > EOF

Run test case

  $ tbx security pretty-print .security.json
  # Security
  
  |File|line/<br>column|Cwe|Test ID|Details|
  |---|:-:|:-:|:-:|---|
  

