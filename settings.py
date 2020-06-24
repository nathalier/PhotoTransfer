from enum import Enum


class DateSource(Enum):
	MODIF_DATE = 1
	CREAT_DATE = 2
	FILE_NAME = 3


def android_device(dev_name):
	return {
		'folder': f'tmp_{dev_name}',
		'date_source': DateSource.FILE_NAME,
		'pattern': '\d{8}_\d{6}.*',
		'extensions': ['jpg', 'mp4'],
		'transform': lambda time_prefix, file: f'{time_prefix}_{dev_name}{file.suffix}'}

settings = {
	'Canon': {
		'folder': 'tmp_Canon',
		'date_source': DateSource.CREAT_DATE,
		'extensions': ['jpg', 'mov', 'cr2', 'thm'],
		'transform': lambda time_prefix, file: f'{time_prefix}_Canon_{file.name}'
	},
	'LenovoS5Talka': android_device('LenovoS5Talka'),
	'LenovoAndr': android_device('LenovoAndr'),
	'LenovoIrynka': android_device('LenovoIrynka'),
	'Android': android_device('other')

}
