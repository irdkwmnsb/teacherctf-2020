## Variability
```
> Waider91 [2020-04-21 07:36PM]
Решил сегодня опробовать систему электронных пропусков, решил что пойду в магазин. 
Выхожу на улицу, слышу крик из окна на третьем этаже соседнего дома. Я слышал, что 
социальная изоляция плохо действует на людей, но настолько отчаянного крика я раньше 
не слышал. Дальше следующее: из этого окна на меня летит две плашки оперативки. 
Благо у меня с собой был термос жидкого азота, сразу бросил плашки в него. Побежал 
домой, удалось сделать дамп памяти с этих плашек. Оказывается память была ECC, 
поэтому получилось восстановить почти всё. Там нет ничего интересного, но если 
вы хотите потыкаться, то дамп прилагаю. Вот вам и карантин...
[dump](dump.raw)
```

## Файлы: 
dump.raw

## Флаг: 
```TeacherCTF{this_flag_is_typed_in_notepad}```

## Решение:
Для работы с дампами оперативной памяти существует множество утилит, самая популярная из них - volatility. Название задания - синоним этого слова.  
Установить volatility можно на любой ОС, но я буду использовать ubuntu, потому что так проще.
На ubuntu volatility устанавливается одной командой - `sudo apt install volatility`
Первое что мы делаем, когда получаем дамп памяти это пытаемся понять, что за операционная система работала на том компьютере.  
Делается это с помощью команды 
```
$ volatility -f dump.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (dump.raw)
                      PAE type : No PAE
                           DTB : 0x39000L
                          KDBG : 0x80537d60L
          Number of Processors : 1
     Image Type (Service Pack) : 0
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2020-04-21 07:08:25 UTC+0000
     Image local date and time : 2020-04-21 11:08:25 +0400
```
Это Windows XP.
volatility позовляет нам посмотреть какие процессы были запущены на момент снятия дампа.
```
$ volatility -f dump.raw pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x80a335f8 System                    4      0     46      215 ------      0
0xffbb8b90 smss.exe                480      4      3       21 ------      0 2020-04-21 07:52:46 UTC+0000
0xffb92b78 csrss.exe               576    480     10      289      0      0 2020-04-21 07:52:46 UTC+0000
0xffb7f2f8 winlogon.exe            600    480     20      524      0      0 2020-04-21 07:52:46 UTC+0000
0xffb63588 services.exe            644    600     15      248      0      0 2020-04-21 07:52:46 UTC+0000
0xffb61bd8 lsass.exe               656    600     21      304      0      0 2020-04-21 07:52:46 UTC+0000
0xffb42020 svchost.exe             828    644     10      231      0      0 2020-04-21 07:52:47 UTC+0000
0xffb3b6e8 svchost.exe             936    644     68     1340      0      0 2020-04-21 07:52:47 UTC+0000
0xffb01da8 svchost.exe            1236    644      6       89      0      0 2020-04-21 07:52:56 UTC+0000
0xffafd928 svchost.exe            1276    644     13      152      0      0 2020-04-21 07:52:56 UTC+0000
0xffaee630 spoolsv.exe            1384    644     10      132      0      0 2020-04-21 07:52:56 UTC+0000
0xffa91b98 explorer.exe           1368   1284     10      300      0      0 2020-04-21 06:54:26 UTC+0000
0xff960da8 ctfmon.exe             1704   1368      1       59      0      0 2020-04-21 06:54:31 UTC+0000
0xff95fda8 msmsgs.exe              436   1368      5      137      0      0 2020-04-21 06:54:31 UTC+0000
0xffa00020 wpabaln.exe            1360    600      1       54      0      0 2020-04-21 06:56:26 UTC+0000
0xffaeb020 cmd.exe                 824   1368      1       17      0      0 2020-04-21 07:07:57 UTC+0000
```
Из необычного видим, что у пользователя была запущена консоль. (cmd.exe)
volatility позволяет посмотреть что было написано в консоли.
```
$ volatility -f dump.raw consoles
Volatility Foundation Volatility Framework 2.6
**************************************************
ConsoleProcess: csrss.exe Pid: 576
Console: 0x4e23b0 CommandHistorySize: 50
HistoryBufferCount: 1 HistoryBufferMax: 4
OriginalTitle: ????????? ??????
Title: ????????? ??????
AttachedProcess: cmd.exe Pid: 824 Handle: 0x64c
----
CommandHistory: 0x4e4d88 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 2 LastAdded: 1 LastDisplayed: 1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x64c
Cmd #0 at 0x4e29f0: cd "??? ?????????"
Cmd #1 at 0x4e1eb8: type flag.txt
----
Screen 0x4e2ab0 X:80 Y:300
Dump:
Microsoft Windows XP [?????? 5.1.2600]
(?) ?????????? ??????????, 1985-2001.

C:\Documents and Settings\David>cd "??? ?????????"

C:\Documents and Settings\David\??? ?????????>type flag.txt
???T e a c h e r C T F { t h i s _ f l a g _ i s _ t y p e d _ i n _ n o t e p a d }
C:\Documents and Settings\David\??? ?????????>
```
Получаем флаг
TeacherCTF{this_flag_is_typed_in_notepad}