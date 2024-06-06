# #!/bin/bash

# 检查输入参数
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <path_to_project1> <path_to_project2> <output_log_file>"
    exit 1
fi

# 获取输入参数
PROJECT1=$1
PROJECT2=$2
LOGFILE=$3

# 检查项目路径是否存在
if [ ! -d "$PROJECT1" ]; then
    echo "Error: Directory $PROJECT1 does not exist."
    exit 1
fi

if [ ! -d "$PROJECT2" ]; then
    echo "Error: Directory $PROJECT2 does not exist."
    exit 1
fi

# 清空日志文件
> "$LOGFILE"

PROJECT_PATH_1=""
PROJECT_PATH_2=""
DIFF_LIST_FILE=""

# 清空或创建输出文件
> "$DIFF_LIST_FILE"

# 遍历第一个项目路径下的所有文件
find "$PROJECT_PATH_1" -type f | while read -r file1; do
    # 获取相对路径
    relative_path="${file1#$PROJECT_PATH_1/}"

    # 对应的第二个项目路径下的文件
    file2="$PROJECT_PATH_2/$relative_path"

    # 检查第二个项目路径下是否存在该文件
    if [ -f "$file2" ]; then
        # 对比两个文件
        diff_output=$(diff "$file1" "$file2")

        # 如果存在差异
        if [ -n "$diff_output" ]; then
            # 记录存在差异的文件
            echo "Difference in file: $relative_path" >> "$DIFF_LIST_FILE"
            echo "Path 1: $file1" >> "$DIFF_LIST_FILE"
            echo "Path 2: $file2" >> "$DIFF_LIST_FILE"
            echo "" >> "$DIFF_LIST_FILE"

            # 将差异保存为 .log 文件
            log_file="${relative_path//\//_}.log"
            echo "$diff_output" > "$log_file"
        fi
    else
        # 如果第二个项目路径下不存在该文件，也记录下来
        echo "File only in Path 1: $relative_path" >> "$DIFF_LIST_FILE"
        echo "Path 1: $file1" >> "$DIFF_LIST_FILE"
        echo "Path 2: $file2 (does not exist)" >> "$DIFF_LIST_FILE"
        echo "" >> "$DIFF_LIST_FILE"
    fi
done

# 遍历第二个项目路径下的所有文件，检查是否有在第一个项目路径下不存在的文件
find "$PROJECT_PATH_2" -type f | while read -r file2; do
    # 获取相对路径
    relative_path="${file2#$PROJECT_PATH_2/}"

    # 对应的第一个项目路径下的文件
    file1="$PROJECT_PATH_1/$relative_path"

    # 检查第一个项目路径下是否存在该文件
    if [ ! -f "$file1" ]; then
        # 记录不存在的文件
        echo "File only in Path 2: $relative_path" >> "$DIFF_LIST_FILE"
        echo "Path 1: $file1 (does not exist)" >> "$DIFF_LIST_FILE"
        echo "Path 2: $file2" >> "$DIFF_LIST_FILE"
        echo "" >> "$DIFF_LIST_FILE"
    fi
done

echo "Diff comparison completed. Check $DIFF_LIST_FILE for the list of differing files."