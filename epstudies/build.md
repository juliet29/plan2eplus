# Converting idd format to dataclass

#### Getting only the information pertaining to the key 
sed -n -E '/\Shading:Site,/,/^$/p' Energy+.idd | bat

#### blank line
rg "^\$" door.txt

#### indicators of interest
rg "\\\(field|type|required-field|default)" door.txt

#### indicators and their values -> improved
rg "\\\(field|type|required-field|default) (.*\$)" door.txt

#### keys indicating a new idf object
rg "^(\w+\:*)+," window.txt

#### filter file down to desired information: 
rg -o -e "^\$" -e "^(\w+\:*)+," -e "\\\(field|type|required-field|default|units) (.*\$)"  window.txt


## edit the smaller file

#### get rid of the field indicator 
sed -E 's/\\\field (.*$)/\1/' test.txt

#### and replace spaces with underscore 
sed -E -e '/field/s/ /_/g' -e 's/\\\field_(.*$)/\1/' test.txt


#### put everything on the same line  
