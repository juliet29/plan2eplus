#!/opt/homebrew/bin/fish

set EP22IDD '/Applications/EnergyPlus-22-2-0/Energy+.idd'

# echo $EP22IDD
#echo 'Starting to idd'
# echo "first arg: $argv[1]"
set input $argv[1]

awk -v IGNORECASE=1 "/^$input,/" RS= $EP22IDD # |
# rg -o -e "^\$" -e "^(\w+\:*)+," -e "\\\(field|type|required-field|default|units) (.*\$)" |
# sed -E -e 's/,/\%/' -e '/field/s/ /_/g' -e 's/\\\field_(.*$)/\1/' -e 's/.+(alpha)/:str=""\%/' -e 's/.+(deg)/:float=0.0\%/' -e 's/.+( m)/:float=0.0\%/' -e 's/.+(real)/:float=0.0\%/' |
# awk 'BEGIN {RS="%"}  {print $1 $2 $3}'





