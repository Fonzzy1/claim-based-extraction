source run.sh 

for file in experiments/configs/*FILTERTEST*; do
    echo "$file" 
    base=$(basename "$file")
    pkl_file="experiments/results/${base%.yml}.pkl"
    if [ ! -f "$pkl_file" ]; then
        dc run pipeline "$file" 
    fi
done
