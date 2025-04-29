# os dependent configuration
from platform import system as _OS
_CONFIG = {
    'Linux'  : {
        'OPTION1': "OPTION1 from Linux",
        'OPTION2': "OPTION2 from Linux",
        },
    'Darwin'  : {
        'OPTION1': "OPTION1 from Darwin",
        'OPTION2': "OPTION2 from Darwin",
        },
    'Windows'  : {
        'OPTION1': "OPTION1 from Windows",
        'OPTION2': "OPTION2 from Windows",
        },
}[_OS()]

# os dependent setup
option1 = _CONFIG['OPTION1']
option2 = _CONFIG['OPTION2']

print(option1)
print(option2)
