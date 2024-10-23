Схема базы данных:
![image](https://github.com/user-attachments/assets/fc9a19f1-03a2-4808-86d5-ae72eebc0366)
Техническое задание:
В больнице несколько отделений. Есть списки врачей по каждому отделению. В отделении опр. количество коек. Есть список диагнозов (болезней). Для каждого диагноза – список лекарств (что и сколько в день) и процедур (что и сколько раз). Разные диагнозы могут «использовать» одно и то же лекарство. Врач может назначить что-то из списка. Пациент может иметь несколько болезней и => несколько врачей. Врач может лечить нескольких больных. Ежедневно обновляется состояние больного (реанимация, болен, здоров, умер).
Требуется:
• Поддержка оформления нового больного (м.б. отправлен лечиться амбулаторно или размещен в отделении, если есть койки);
• Поддержка оформления/увольнения врача;
• Поддержка назначения/изменения лечения больному (не чаще раза в сутки) с учетом предотвращения возможной передозировки из-за такого же лекарства по другому диагнозу;
• Поддержка заполнения состояния больного;
• Поддержка автоматической выписки, если пациент здоров/умер;
• Поддержка перевода пациента в др. отделение, если по основной болезни здоров, а по другой болен;
Отчеты:
• Список врачей, пациенты которых умирают;
• Список лучших врачей по отделениям;
• Частота болезней пациентов за произвольный период времени;
• История больницы (за год/ за весь период работы больницы).
Дополнительные соглашения предметной области:
Доктор может ставить только те диагнозы, которые лечат в отделении, в котором он работает, назначать только те медикаменты, которые закреплены за назначенным диагнозом.
При смене дозировки старое назначение закрывается, и открывается назначение с другой дозировкой.
При поступлении пациента, ему отводится койка в одном отделении, в котором он проходит лечение до выписки по всем болезням.
Показатель эффективности врача при составлении рейтинга лучших врачей отделения высчитывается как разность выздоровевших и погибших по вине врача пациентов.
История больницы заключается в списке поступивших, выздоровевших и погибших пациентов по каждому отделению.