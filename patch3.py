import os
rh_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\Resource.h'
with open(rh_path, 'r', encoding='utf-8') as f:
    rh = f.read()
if 'IDR_WAV_COMPLETE' not in rh:
    rh = rh.replace('#define IDI_NTMU', '#define IDR_WAV_COMPLETE 110\n#define IDI_NTMU')
    with open(rh_path, 'w', encoding='utf-8') as f:
        f.write(rh)

rc_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\NTMU.rc'
with open(rc_path, 'r', encoding='utf-8') as f:
    rc = f.read()
if 'IDR_WAV_COMPLETE' not in rc:
    rc += '\nIDR_WAV_COMPLETE WAVE "res\\\\Complete.wav"\n'
    with open(rc_path, 'w', encoding='utf-8') as f:
        f.write(rc)
