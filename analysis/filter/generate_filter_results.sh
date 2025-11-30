source run.sh

# Collect files to process
files=(experiments/configs/*FILTERTEST*)
total=${#files[@]}
count=0

for file in "${files[@]}"; do
    echo "$file"
    base=$(basename "$file")
    pkl_file="experiments/results/${base%.yml}.pkl"
    if [ ! -f "$pkl_file" ]; then
        dc run --rm pipeline "$file"
    fi
    ((count++))
    # Show progress bar
    progress=$((count * 50 / total))
    bar=$(printf "%-${progress}s" "=")
    printf "\rProgress: [%-50s] %d/%d" "$bar" "$count" "$total"
done

echo -e "\nDone."
