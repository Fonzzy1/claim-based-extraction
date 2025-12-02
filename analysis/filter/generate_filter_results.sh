source run.sh

# Collect files to process
files=(experiments/configs/*FILTERTEST*)
missing_files=()
for file in "${files[@]}"; do
    base=$(basename "$file")
    pkl_file="experiments/results/${base%.yml}.pkl"
    if [ ! -f "$pkl_file" ]; then
        missing_files+=("$file")
    fi
done

total=${#missing_files[@]}
count=0

draw_progress_bar() {
    local progress=$1
    local total=$2
    local width=40
    local percent=$(( 100 * progress / total ))
    local filled=$(( width * progress / total ))
    local bar=""
    for ((i=0; i<$filled; i++)); do bar+="█"; done
    for ((i=filled; i<$width; i++)); do bar+=" "; done
    printf "\r[%s] %3d%% (%d/%d)" "$bar" "$percent" "$progress" "$total"
}

for file in "${missing_files[@]}"; do
    base=$(basename "$file")
    pkl_file="experiments/results/${base%.yml}.pkl"
    dc run --rm pipeline "$file" > /dev/null 2>&1
    if [ ! -f "$pkl_file" ]; then
        echo "Error: $pkl_file not found after running $file"
        echo "Config: $file"
        break
    fi
    ((count++))
    draw_progress_bar "$count" "$total"
done

echo -e "\nDone."
