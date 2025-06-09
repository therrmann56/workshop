# filter/main.py
# Dieses Skript liest Logzeilen ein und filtert nur Zeilen mit dem Statuscode 200.

input_path = "/data/logs.txt"
output_path = "/data/filtered_logs.txt"

if __name__ == "__main__":
    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            if " 200 " in line:
                outfile.write(line)
    print(f"Gefilterte Logzeilen nach {output_path} geschrieben.")
