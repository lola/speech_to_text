# references
sox="/usr/local/bin/sox"
config="-b 16 -c 1 -r 16k"

# variables
source_folder="${1:-.}"
destination_folder="${source_folder}/audio-recordings-wav"

# print all params so user can see
clear
echo "Script operating using the following settings and parameters....."
echo ""
echo "which SoX: ${sox}"
echo "Config: ${config}"
echo "Source: ${source_folder}"
echo "Destination: ${destination_folder}"
echo ""

read -e -p "Do you wish to proceed? (y/n) : " confirm

if [ $confirm = "N" ] || [ $confirm = "n" ]; then
	exit
fi

# create destination if it does not exist
if [ ! -d "${destination_folder}" ]; then
	mkdir -p "${destination_folder}"
fi

# loop through all files in folder and convert them to wav
for input_file in *\ *;
do
	name_part=`basename "$input_file" .mp3`
	output_raw="$name_part.raw"
	output_file="$name_part.wav"
	
	#create wav if file does not exist
	if [ ! -f "$destination_folder/$output_file" ]; then
		$sox "${source_folder}/$input_file" "$destination_folder/$output_file" remix 1,2
		$sox $sox_options "${source_folder}/$input_file" "$destination_folder/$output_file" remix 1-2

		echo "$destination_folder/$output_file"
	else
		echo "Skipping ${input_file} as $destination_folder/$output_file exists."
	fi

done
