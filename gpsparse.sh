gpspipe -w -n 4|jq .speed|grep -v null
gpspipe -w -n 4|jq .alt|grep -v null
gpspipe -w -n 4|jq .lat|grep -v null
gpspipe -w -n 4|jq .lon|grep -v null
