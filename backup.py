import shutil
import datetime

src_dir = '/Documents'
dst_dir = '/Backups'

now = datetime.datetime.now()

# Create the backup folder with the current date and time
dst_path = f'{dst_dir}/Documents_{now:%Y-%m-%d_%H-%M-%S}'

# Copy the entire directory
shutil.copytree(src_dir, dst_path)

print(f'Successfully created backup of {src_dir} at {dst_path}')