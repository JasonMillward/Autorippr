#!/bin/bash

new_version=$1
today="$(date +'%Y-%m-%d %R:%S %Z')"

if [ -z $new_version ]; then
    echo "Usage: $0 <new_version>";
    exit 1;
fi

version_string="$new_version, $today"

echo "Bumping applicable files to version: $version_string"

for i in `find . -type f -name "*.py"`;
do
    file=`basename $i`;
    echo "Bumping version of $i"
    sed -i "s/\$Id\s*.*\$;/\$Id: $version_string \$;/g" $i
done

