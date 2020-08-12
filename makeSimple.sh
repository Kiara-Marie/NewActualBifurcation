#!/bin/sh

id=0
for a in "0.00001" " 0.0001" "0.001"
do
  for dist in "0.1" "0.2" "0.4"
  do  
    for tempDrop in "0.1" "1" "10" "100"
    do
      cp "modelRunner.sh" "modelRunner${id}.sh"
      sed -i "s/--shells 5/--shells $shell/" "modelRunner$id.sh"
      sed -i "s/--time 0/--time $t/" "modelRunner$id.sh"
      sed -i "s/--a -0.01/--a $a/" "modelRunner$id.sh"
      sed -i "s/--dist 0.2/--dist $dist/" "modelRunner$id.sh"
      sed -i "s/--tempDrop 1/--tempDrop $tempDrop/" "modelRunner$id.sh"
      sed -i "s/shells_5/shells_$shell/" "modelRunner$id.sh"
      sed -i "s/time_0/time_$t/" "modelRunner$id.sh"
      sed -i "s/a_-0.01/a_$a/" "modelRunner$id.sh"
      sed -i "s/dist_0.2/dist_$dist/" "modelRunner$id.sh"
      sed -i "s/tempDrop_1/tempDrop_$tempDrop/" "modelRunner$id.sh"
      id=$((id+1))
    done;
  done;
done;
