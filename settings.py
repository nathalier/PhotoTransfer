from enum import Enum


class DateSource(Enum):
	MODIF_DATE = 1
	CREAT_DATE = 2
	FILE_NAME = 3


settings = {
	'Canon': {
		'folder': 'tmp_Canon',
		'date_source': DateSource.CREAT_DATE,
		'extensions': ['jpg', 'mov', 'cr2']
	}
}
