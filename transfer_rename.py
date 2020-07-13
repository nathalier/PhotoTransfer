from datetime import datetime
import os
from pathlib import Path
import re
import time
from settings import settings, DateSource


disk_name = 'E'
base_folder = 'PhotoVideo/'
devices = ['Canon', 'Lenovo2', 'GoPro']

base_path = Path(f'{disk_name}:/{base_folder}')

pretend = True


def date_from_file_name(pattern):
	def customized(file):
		return re.search('(' + pattern + ')', file.stem).groups()[0]
	return customized


def date_from_meta_info(fn):
	def customized(file):
		return datetime.fromtimestamp(fn(file)).strftime('%Y%m%d_%H%M%S')
	return customized


log = []
for cam in devices:
	src_dir = 'tmp_' + cam
	src_path = base_path / src_dir
	dest_path = base_path

	if settings[cam]['date_source'] == DateSource.CREAT_DATE:
		apply_fn = date_from_meta_info(os.path.getctime)
	elif settings[cam]['date_source'] == DateSource.MODIF_DATE:
		apply_fn = date_from_meta_info(os.path.getmtime)
	elif settings[cam]['date_source'] == DateSource.FILE_NAME and settings[cam]['pattern']:
		apply_fn = date_from_file_name(settings[cam]['pattern'])
	else:
		raise NotImplementedError('Unknown pattern. Common date extraction is not yet implemented.')

	files = []
	for e in settings[cam]['extensions']:
		files += list(src_path.glob(f'*.{e}'))

	for x in files:
		try:
			time_prefix = apply_fn(x)
			new_fname = settings[cam]['transform'](time_prefix, x)
			new_path = dest_path / new_fname
			if not pretend:
				x.rename(new_path)
			log.append(f'{x}, {new_path}\n')
		except Exception as e:
			print(x.name + ' error: ', e)

if log:
	with open(f'log_{time.strftime("%y%m%d_%H%M%S")}{"_pretend" if pretend else ""}.csv',
	          'w', encoding='utf-8') as f:
		f.writelines(log)
