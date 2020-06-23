from datetime import datetime
import os
from pathlib import Path
import shutil
import time
from settings import settings, DateSource

disk_name = 'E'
base_folder = 'PhotoVideo/New/All/'
devices = ['Canon']

base_path = Path(f'{disk_name}:/{base_folder}')

pretend = True

def parse_file_name():
	pass

for cam in devices:
	log = []
	src_dir = 'tmp_' + cam
	src_path = base_path / src_dir
	dest_path = base_path

	if settings[cam]['date_source'] == DateSource.CREAT_DATE:
		apply_fn = os.path.getctime
	elif settings[cam]['date_source'] == DateSource.MODIF_DATE:
		apply_fn = os.path.getmtime
	else:
		apply_fn = parse_file_name

	files = []
	for e in settings[cam]['extensions']:
		files += list(src_path.glob(f'*.{e}'))

	for x in files:
		try:
			time_prefix = datetime.fromtimestamp(apply_fn(x)).strftime('%Y%m%d_%H%M%S')
			new_fname = f'{time_prefix}_{cam}_{x.name}'
			new_path = dest_path / new_fname
			if not pretend:
				x.rename(new_path)
			log.append(f'{x}, {new_path}\n')
		except e:
			print(x.name + ' error: ', e)

	with open(f'log_{cam}_{time.strftime("%y%m%d_%H%M%S")}{"_pretend" if pretend else ""}.csv',  'w', encoding='utf-8') as f:
		f.writelines(log)
