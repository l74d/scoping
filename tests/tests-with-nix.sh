env -u PYTHONPATH nix-shell big-test.nix --run 'python big-test.py'
echo -e "python3."{6,7,8,9}" small"{,-in-function,-rename}".py\n" | nix-shell -p python3{6,7,8,9} --run sh
    
