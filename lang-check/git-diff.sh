#!/bin/bash

# Load .env file
if [ -f "$(dirname "$0")/.env" ]; then
    source "$(dirname "$0")/.env"
fi

# Check if environment variable exists
if [ -z "${DIFY_API_KEY}" ]; then
    echo "Error: DIFY_API_KEY environment variable is not set"
    exit 1
fi

# Initialize debug mode flag
debug_mode=false

# Process command line arguments
while getopts "t" opt; do
    case $opt in
        t)
            debug_mode=true
            ;;
    esac
done

# Get current commit ID (first 5 characters)
commit_id=$(git log -1 --oneline | awk '{print $1}' | cut -c1-5)

# Get Git repository root path
repo_root=$(git rev-parse --show-toplevel)

# Get current month and day
current_date=$(date +"%m%d")

# Get script directory path
script_dir=$(dirname "$(realpath "$0")")

# Set file path, filename includes commit ID and current date with .txt extension
log_file="${script_dir}/commit-${commit_id}-${current_date}.txt"

# Create or clear log file
echo "" > "$log_file"

# Get list of changed files, filter non-file information
changed_files=$(git diff --name-only origin/main...HEAD)

# Iterate through each changed file
for file in $changed_files
do
    # Check if file exists and is a .md file
    if [ -f "$repo_root/$file" ] && [[ "$file" == *.md ]]; then
        # Output start tag
        echo "<start---lang-check/$file---start>" >> "$log_file"
        
        # Output file content
        cat "$repo_root/$file" >> "$log_file"
        
        # Output end tag
        echo -e "\n\n<end---/$file---end>\n" >> "$log_file"
        
    fi
done

if [ "$debug_mode" = true ]; then
    echo "Output saved to $log_file"
fi

# Set API key and other constants
api_key="${DIFY_API_KEY}"
user=$(git config user.name)

# Check if file exists
if [ ! -f "$log_file" ]; then
    echo "Error: File $log_file does not exist"
    exit 1
fi

# Read .txt file content
query_content=$(<"$log_file")

# Debug output
if [ "$debug_mode" = true ]; then
    echo "===== Debug Info ====="
    echo "File path: $log_file"
    echo "Content length: ${#query_content}"
    echo "Content preview (first 100 chars):"
    echo "${query_content:0:100}"
    echo "=================="
fi

# Prepare JSON data
json_data=$(cat <<EOF
{
    "inputs": {"query": $(printf '%s' "$query_content" | jq -R -s .)},
    "response_mode": "blocking",
    "user": "$user"
}
EOF
)

# Debug output
if [ "$debug_mode" = true ]; then
    echo "===== API Request Data ====="
    echo "$json_data"
    echo "===================="
fi

# Send POST request via curl
if [ "$debug_mode" = true ]; then
    # Request with debug info, 30 seconds timeout
    response=$(curl -X POST 'https://api.dify.ai/v1/completion-messages' \
    --header "Authorization: Bearer $api_key" \
    --header "Content-Type: application/json" \
    --data "$json_data" \
    --max-time 30 \
    -v | jq -r '.answer')
else
    # Request without debug info, 30 seconds timeout
    response=$(curl -X POST 'https://api.dify.ai/v1/completion-messages' \
    --header "Authorization: Bearer $api_key" \
    --header "Content-Type: application/json" \
    --data "$json_data" \
    --max-time 30 \
    -s | jq -r '.answer')
fi

# Check if curl was successful
if [ $? -ne 0 ]; then
    echo "Error: API request timeout or failed"
    exit 1
fi

# Output API response
echo "$response"

# Check if response contains error marker
if echo "$response" | grep -q "❌"; then
    exit 1
else
    exit 0
fi