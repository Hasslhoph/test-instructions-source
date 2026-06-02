# Замена описания шкалы на слайдере оценки

## Замена фраз с помощью нового языкового файла

Для того чтобы заменить стандартные фразы на другие, вам понадобится создать собственный языковой файл. Для этого перейдите в административную часть модуля по пути адрес_портала`/bitrix/admin`. В левом меню нажмите «Контент» > «Структура сайта» > «Файлы и папки» > «bitrix»

![](_images-02/image181.png)

В папке `bitrix` найдите папку `php_interface` и откройте ее.

![](_images-02/image230.png)

В папке `php_interface` нажмите кнопку «Добавить» и создайте папку с названием `user_lang`. При создании папки укажите только название, никакие другие поля и чекбоксы заполнять не нужно.

![](_images-02/image315.png)

![](_images-02/image250.png)

Теперь перейдите в созданную папку `user_lang` и здесь аналогичным образом создайте папку с названием `ru`. При создании папки укажите только название, никакие другие поля и чекбоксы заполнять не нужно.

![](_images-02/image265.png)

Откройте папку `ru`. В блоке «Управление структурой» должен отобразиться следующий путь: `/bitrix/php_interface/user_lang/ru`

![](_images-02/image331.png)

На следующем шаге вам понадобится текстовый редактор кода. В рамках этой статьи мы будем использовать [Notepad++](https://notepad-plus-plus.org/downloads/). Откройте редактор и нажмите на иконку белого листа, чтобы создать новый файл.

![](_images-02/image517.png)

Затем скопируйте в файл следующие строки:

```php
<?
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_BAD"] = "Уровень ниже допустимого";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_NORMAL"] = "Допустимый уровень";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_GOOD"] = "Оптимальный уровень";
?>
```

В квадратных скобках вы можете увидеть следующие значения:

- `["ASSESSMENT_RADAR_CHART_COLOR_LABELS_BAD"]` — ID фразы, которая соответствует низкой оценке.

- `["ASSESSMENT_RADAR_CHART_COLOR_LABELS_NORMAL"]` — ID фразы, которая соответствует средней/допустимой оценке.

- `["ASSESSMENT_RADAR_CHART_COLOR_LABELS_GOOD"]` — ID фразы, которая соответствует высокой оценке.

![](_images-02/image490.png)

После ID фраз указаны сами фразы, которые выводятся в публичной части портала на слайдере оценки. Замените фразы в кавычках на нужные вам, например:

```php
<?
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_BAD"] = "Низкая оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_NORMAL"] = "Средняя оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_GOOD"] = "Высокая оценка";
?>
```

Убедитесь, что для данного файла выбрана кодировка `UTF-8`. Для этого в верхней панели выберите пункт `Кодировка`.

![](_images-02/image501.png)

Файл с языковыми фразами должен быть сохранен в формате `php`. Чтобы задать этот формат файлу в верхней панели выберите `Синтаксисы` > `P` > `PHP`.

![](_images-02/image388.png)

Теперь файл нужно сохранить. Для этого в верхнем меню нажмите «Файл» > «Сохранить как».

![](_images-02/image481.png)

В поле «Имя файла» укажите `lang` без кавычек. Обратите внимание, что название файла должно быть именно `lang`, в ином случае замена фраз не произойдет.

![](_images-02/image484.png)

В административной части портала вернитесь в ранее созданную папку `ru` (по пути `/bitrix/php_interface/user_lang/ru`) и нажмите «Загрузить файл».

![](_images-02/image445.png)

Загрузите ранее созданный файл lang.php в папку. Сохраните изменения.

![](_images-02/image525.png)

![](_images-02/image207.png)

Теперь перейдите в публичную часть портала откройте любую свою карточку оценки. Фразы с описанием оценок будут изменены на новые, эти изменения будут видны всем пользователям.

![](_images-02/image106.png)

## Редактирование фраз в языковом файле

Чтобы скорректировать фразы на слайдере оценки перейдите в папку `/bitrix/php_interface/user_lang/ru` и кликните на бургер-меню (≡) рядом с файлом `lang.php`. Выберите действие «Редактировать как `php`».

![](_images-02/image511.png)

В результате откроется форма для редактирования файла. Здесь достаточно изменить фразы на другие и нажать «Сохранить».

![](_images-02/image467.png)

## Добавление своей фразы после описания шкалы

Под описанием шкалы вы можете разместить свой заголовок с текстом. В текст можно добавить пояснение к процессу оценки и другие любые другие важные материалы: ссылки, изображения и так далее. Для десктопа и мобильного приложения фраза добавляется по-разному.

## Десктопная версия Б24

Согласно текущей инструкции создайте файл lang.php и вставьте в него следующий код:

```php
<?
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["INFO_BEFORE_COMPETENCE_ASSESSMENT"] = '
<div class="rating-heading assessment-heading">Заголовок</div>
<div class="rating-wrapper" style="grid-template-columns: none;">Текст описания</div>';
?>
```

Если файл lang.php уже создан и в него добавлены новые языковые фразы для описания шкалы, то данный код нужно добавить в этот же файл:

```php
<?
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_BAD"] = "Низкая оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_NORMAL"] = "Средняя оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_GOOD"] = "Высокая оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["INFO_BEFORE_COMPETENCE_ASSESSMENT"] = '
<div class="rating-heading assessment-heading">Заголовок</div>
<div class="rating-wrapper" style="grid-template-columns: none;">Текст описания</div>';
?>
```

В коде укажите свой заголовок, текст и любую другую HTMl-верстку. На слайдере оценивания блок с фразой будет выглядеть так:

![](_images-02/image134.png)

## Мобильное приложение Б24

Чтобы новая фраза также выводилась и в мобильном приложении Б24, дополните код. Для этого вставьте в этот же файл выделенную фразу:

```php
<?
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_BAD"] = "Низкая оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_NORMAL"] = "Средняя оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["ASSESSMENT_RADAR_CHART_COLOR_LABELS_GOOD"] = "Высокая оценка";
$MESS["/bitrix/components/ithive/assessment.360.assessing/templates/.default/lang/ru/template.php"]["INFO_BEFORE_COMPETENCE_ASSESSMENT"] = '
<div class="rating-heading assessment-heading">Заголовок</div>
<div class="rating-wrapper" style="grid-template-columns: none;">Текст описания</div>';
$MESS["/bitrix/mobileapp/ithive.assessment360/extensions/assessment/my-task-detail/lang/ru/extension.php"]["INFO_BEFORE_COMPETENCE_ASSESSMENT"] = 'Текст описания';
?>
```

Обратите внимание, что для фразы мобильного приложения нельзя использовать HTML-верстку. В качестве описания поддерживается только обычный текст.

В мобильном приложении фраза будет выглядеть так:

![](_images-02/image360.png)
