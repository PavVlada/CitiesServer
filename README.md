# CitiesServer
Простой сервер, который предоставляет REST API сервис

## getCityInfo
  Метод возвращает информацию о городе по его geonameid. Для вызова метода необходимо отправить запрос:
  ```
  getCityInfo?geonameid=<geonameid>
  ```
  где `<geonameid>` - geonameid (идентификатор) интересующего города.
  
  Сервер возвращает ответ в формате json со всеми атрибутами города (из описания базы данных GeoNames).
  
  Пример вызова метода:
  ```
  http://127.0.0.1:8000/getCityInfo?geonameid=461945
  ```
  
  Результат:
  ```
{
  "geonameid": 461945,
  "name": "Zuyevo",
  "asciiname": "Zuyevo",
  "alternatenames": "Zagor'ye,Zagor’ye,Zuevo,Zuyevo,Зуево",
  "latitude": 60.3331,
  "longitude": 38.6814,
  "feature class": "P",
  "feature code": "PPL",
  "country code": "RU",
  "cc2": null,
  "admin1 code": "85",
  "admin2 code": null,
  "admin3 code": null,
  "admin4 code": null,
  "population": 0,
  "elevation": null,
  "dem": 129,
  "timezone": "Europe/Moscow",
  "modification date": "2012-04-05"
}
  ```
  
  Если город с таким geonameid (идентификатором) не найден, то метод возвращает пустой json.
  
  Пример:
  ```
  http://127.0.0.1:8000/getCityInfo?geonameid=0
  ```
  
  Результат:
  ```
  {}
  ```
  
  ## getCityList
  Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией. 
  
  Для вызова метода необходимо отправить запрос:
  ```
  getCityList?page=<page>&number=<number>
  ```
  где `<page>` - номер отображаемой страницы, `<number>` - количество отображаемых на странице городов.
  
  Сервер возвращает список городов со всеми их атрибутами в формате json.
  Пример вызова метода:
  ```
  http://127.0.0.1:8000/getCityList?page=100&number=2
  ```
  Результат:
  ```
{
  "198": {
    "geonameid": 451945,
    "name": "Mishevo",
    "asciiname": "Mishevo",
    "alternatenames": "Mishevo,Мишево",
    "latitude": 56.97825,
    "longitude": 34.26705,
    "feature class": "P",
    "feature code": "PPL",
    "country code": "RU",
    "cc2": null,
    "admin1 code": "77",
    "admin2 code": null,
    "admin3 code": null,
    "admin4 code": null,
    "population": 0,
    "elevation": null,
    "dem": 231,
    "timezone": "Europe/Moscow",
    "modification date": "2012-01-16"
  },
  "199": {
    "geonameid": 451946,
    "name": "Minino",
    "asciiname": "Minino",
    "alternatenames": "Minino,Минино",
    "latitude": 56.70315,
    "longitude": 34.48691,
    "feature class": "P",
    "feature code": "PPL",
    "country code": "RU",
    "cc2": null,
    "admin1 code": "77",
    "admin2 code": null,
    "admin3 code": null,
    "admin4 code": null,
    "population": 0,
    "elevation": null,
    "dem": 257,
    "timezone": "Europe/Moscow",
    "modification date": "2012-01-16"
  }
}
  ```
  Если номер страницы и количество отображаемых городов на ней превышает число имеющихся городов, то метод возвращает пустой json.
  
  
  ## getTwoCitiesInfo
  Метод принимает названия двух городов на русском языке и получает информацию о найденных городах; определяет, какой из этих городов расположен севернее и одинаковая ли у них временная зона. Если отличная, то дополнительно определяет разницу между их временными зонами. Когда несколько городов имеют одно и то же название, метод выбирает город с большим населением. Если население совпадает, то метод выбирает первый попавшийся город.
  
  Для вызова метода необходимо отправить запрос:
  ```
  getTwoCitiesInfo?city1=<city1>&city2=<city2>
  ```
  где `<city1>` - это название первого города на русском языке, `<city2>` - название второго города на русском языке.
  
  Сервер возвращает ответ в формате json с атрибутами двух городов (в поле `city1` информация о первом городе, в `city2` информация о втором городе) с указанием, какой из городов расположен севернее (поле `NorthernCity`); совпадает ли их временная зона (поле `SameTimeZone`); если нет, то указывает разницу в часах (поле `TimeZoneDifferenceInHours`).
  
  Пример вызова метода:
  ```
  http://127.0.0.1:8000/getTwoCitiesInfo?city1=Санкт-Петербург&city2=Владивосток
  ```
  Результат:
  ```
  {
  "city1": {
    "geonameid": 451747,
    "name": "Zyabrikovo",
    "asciiname": "Zyabrikovo",
    "alternatenames": null,
    "latitude": 56.84665,
    "longitude": 34.7048,
    "feature class": "P",
    "feature code": "PPL",
    "country code": "RU",
    "cc2": null,
    "admin1 code": "77",
    "admin2 code": NaN,
    "admin3 code": NaN,
    "admin4 code": NaN,
    "population": 0,
    "elevation": NaN,
    "dem": 204,
    "timezone": "Europe/Moscow",
    "modification date": "2011-07-09"
  },
  "city2": {
    "geonameid": 6423862,
    "name": "Nanayskiy",
    "asciiname": "Nanayskiy",
    "alternatenames": "Nanajskij,Nanayskiy,Нанайский",
    "latitude": 47.2356,
    "longitude": 135.60251,
    "feature class": "H",
    "feature code": "STM",
    "country code": "RU",
    "cc2": null,
    "admin1 code": "30",
    "admin2 code": NaN,
    "admin3 code": NaN,
    "admin4 code": NaN,
    "population": 0,
    "elevation": NaN,
    "dem": 173,
    "timezone": "Asia/Vladivostok",
    "modification date": "2012-10-07"
  },
  "NorthernCity": "Zyabrikovo",
  "SameTimeZone": false,
  "TimeZoneDifferenceInHours": 7
}
```
Если хотя бы один город не найден, то метод возвращает пустой json.

 ## getHint
 Метод принимает часть названия города на русском языке и возвращает подсказку с возможными вариантами продолжения.
 
 Для вызова метода необходимо отправить запрос:
 ```
 getHint?city=<city>
 ```
 где `<city>` - часть названия города на русском языке.
 
 Сервер возвращает ответ в формате json со списком возможных вариантов продолжения на русском языке.
 
 Пример вызова метода:
 ```
 http://127.0.0.1:8000/getHint?city=Привет
 ```
 Результат:
 ```
 {
  "hint": [
    "Приветливая",
    "Приветливый",
    "Приветненское",
    "Приветная",
    "Привет",
    "Приветино",
    "Приветный",
    "Приветок"
  ]
}
```
Если возможные варианты продолжения не найдены, то метод возвращает пустой json.
 
