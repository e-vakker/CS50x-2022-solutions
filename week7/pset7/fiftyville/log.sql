-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time
-- each of their interview transcripts mentions the bakery.
-- Littering took place at 16:36. No known witnesses.
-- Кража утки CS50 произошла в 10:15 утра в пекарне на Хамфри-стрит.
-- Сегодня были опрошены три свидетеля, которые присутствовали в тот момент.
-- в каждом из их интервью упоминается пекарня.
-- Замусоривание произошло в 16:36. Свидетелей нет.
SELECT description FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28
AND street="Humphrey Street";

--| Jose    | “Ah,” said he, “I forgot that I had not seen you for some weeks. It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”                                                                                                                               |
--| Eugene  | “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”                                                                                                                                                                                      |
--| Barbara | “You had my note?” he asked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.                                                                                                                   |
--| Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
--| Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
--| Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
--| Lily    | Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day. My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.                                                                        |
--| Emma    | I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour. They never bought anything.                                                                                                                                                                                 |
--| Хосе | -- Ах, -- сказал он, -- я забыл, что не видел вас несколько недель. Это небольшой сувенир от короля Богемии в обмен на мою помощь в деле с бумагами Ирэн Адлер. |
--| Евгений | -- Я полагаю, -- сказал Холмс, -- что, когда мистер Уиндибэнк вернулся из Франции, он был очень раздражен тем, что вы отправились на бал. |
--| Барбара | — У тебя была моя записка? — спросил он низким резким голосом с сильным немецким акцентом. — Я сказал тебе, что позвоню. Он переводил взгляд с одного на другого из нас, словно не зная, к кому обратиться. |
--| Рут | Где-то через десять минут после кражи я увидел, как вор сел в машину на стоянке пекарни и уехал. Если у вас есть видеозаписи с парковки пекарни, вы можете поискать автомобили, которые покинули парковку в этот период времени. |
--| Евгений | Я не знаю имени вора, но я узнал его. Сегодня утром, прежде чем я пришел в пекарню Эммы, я проходил мимо банкомата на Леггетт-стрит и увидел там вора, снимающего деньги. |
--| Раймонд | Когда вор выходил из пекарни, они позвонили кому-то, кто разговаривал с ними менее минуты. Во время разговора я услышал, как вор сказал, что они планируют вылететь завтра самым ранним рейсом из Фифтивилля. Затем вор попросил человека на другом конце телефона купить билет на самолет. |
--| Лили | У нашего соседнего здания суда есть очень надоедливый петух, который громко кукарекает в 6 утра каждый день. Мои сыновья Роберт и Патрик отвезли петуха в город далеко-далеко, чтобы он нас больше никогда не беспокоил. Мои сыновья благополучно прибыли в Париж. |
--| Эмма | Я владелец пекарни, и кто-то вошел, что-то подозрительно шепча в телефон около получаса. Они никогда ничего не покупали. |
SELECT name, transcript FROM interviews
WHERE year = 2021
AND month = 7
AND day = 28;
-- Cписок подозреваемых людей. Одного из этих людей он видел снимающим деньги в банкомает
--+--------+---------+----------------+-----------------+---------------+
--|   id   |  name   |  phone_number  | passport_number | license_plate |
--+--------+---------+----------------+-----------------+---------------+
--| 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
--| 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
--| 458378 | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
--| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
--| 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
--| 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
--| 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |
--| 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
--+--------+---------+----------------+-----------------+---------------+

SELECT id, name, phone_number, passport_number, license_plate FROM people
WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021
AND month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw")) ORDER BY passport_number;

--+------------------------+--------------+-------------------------------------+---------------+------+--------+
--| destination_airport_id | abbreviation |              full_name              |     city      | hour | minute |
--+------------------------+--------------+-------------------------------------+---------------+------+--------+
--| 4                      | LGA          | LaGuardia Airport                   | New York City | 8    | 20     |
--| 1                      | ORD          | O'Hare International Airport        | Chicago       | 9    | 30     |
--| 11                     | SFO          | San Francisco International Airport | San Francisco | 12   | 15     |
--| 9                      | HND          | Tokyo International Airport         | Tokyo         | 15   | 20     |
--| 6                      | BOS          | Logan International Airport         | Boston        | 16   | 0      |
--+------------------------+--------------+-------------------------------------+---------------+------+--------+
SELECT destination_airport_id, abbreviation, full_name, city, hour, minute FROM flights, airports
WHERE flights.destination_airport_id = airports.id
AND year = 2021
AND month = 7
AND day = 29 ORDER BY hour, minute DESC;

SELECT abbreviation, full_name, city, hour, minute FROM flights, airports
WHERE flights.origin_airport_id = airports.id
AND year = 2021
AND month = 7
AND day = 29 ORDER BY hour, minute DESC;


--+-----------------+------+
--| passport_number | seat |
--+-----------------+------+
--| 1540955065      | 5C   |
--| 1695452385      | 3B   |
--| 1988161715      | 6D   |
--| 5773159633      | 4A   |
--| 7214083635      | 2A   |
--| 8294398571      | 6C   |
--| 8496433585      | 7B   |
--| 9878712108      | 7A   |
--+-----------------+------+

SELECT passport_number, seat FROM passengers
WHERE flight_id IN
(SELECT id FROM flights
WHERE destination_airport_id = 4
AND year = 2021
AND month = 7
AND day = 29
AND hour = 8
AND minute = 20) ORDER BY passport_number;

-- По словам свидетеля преступник звонил по телефону и просил купить билет на самый ранний рейс след. день после кражи.
-- Список подозреваемых состоит из тех кто снимал деньги с банкомата и летел самолетом в New York city.
--+--------+--------+----------------+-----------------+---------------+
--|   id   |  name  |  phone_number  | passport_number | license_plate |
--+--------+--------+----------------+-----------------+---------------+
--| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
--| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
--| 467400 | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
--| 395717 | Kenny  | (826) 555-1652 | 9878712108      | 30G67EN       |
--+--------+--------+----------------+-----------------+---------------+
SELECT id, name, phone_number, passport_number, license_plate FROM people
WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021
AND month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw"))
AND passport_number IN
(SELECT passport_number FROM passengers
WHERE flight_id IN
(SELECT id FROM flights
WHERE destination_airport_id = 4
AND year = 2021
AND month = 7
AND day = 29
AND hour = 8
AND minute = 20)) ORDER BY passport_number;

--+----------+---------------+------+-------+-----+------+--------+
--| activity | license_plate | year | month | day | hour | minute |
--+----------+---------------+------+-------+-----+------+--------+
--| entrance | 30G67EN       | 2021 | 7     | 26  | 8    | 23     |
--| entrance | 94KL13X       | 2021 | 7     | 28  | 8    | 23     |
--| entrance | 1106N58       | 2021 | 7     | 28  | 8    | 34     |
--| entrance | 4328GD8       | 2021 | 7     | 28  | 9    | 14     |
--| exit     | 94KL13X       | 2021 | 7     | 28  | 10   | 18     | BRUCE
--| exit     | 4328GD8       | 2021 | 7     | 28  | 10   | 19     |
--| exit     | 1106N58       | 2021 | 7     | 28  | 10   | 35     | TAYLOR
--| entrance | 30G67EN       | 2021 | 7     | 30  | 12   | 36     |
--| exit     | 30G67EN       | 2021 | 7     | 30  | 17   | 12     |
--| exit     | 30G67EN       | 2021 | 7     | 26  | 17   | 51     |
--+----------+---------------+------+-------+-----+------+--------+

SELECT activity, license_plate, day, hour, minute FROM bakery_security_logs
WHERE year = 2021
AND month = 7
AND day = 28
AND license_plate = "1106N58"
OR license_plate = "94KL13X"
OR license_plate = "4328GD8"
OR license_plate = "30G67EN"
ORDER BY hour, minute;


-- Звонок с места преступления менее 1 минуты итого 2 подозреваемых.
--+----------------+----------------+----------+
--|     caller     |    receiver    | duration |
--+----------------+----------------+----------+
--| (367) 555-5533 | (375) 555-8161 | 45       | Bruce
--| (286) 555-6063 | (676) 555-6554 | 43       | Taylor
--+--------+--------+----------------+-----------------+---------------+
--|   id   |  name  |  phone_number  | passport_number | license_plate |
--+--------+--------+----------------+-----------------+---------------+
--| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
--| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |

SELECT caller, receiver, duration FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 60;

--+-------+-----------------+---------------+----------------+
--| name  | passport_number | license_plate |  phone_number  |
--+-------+-----------------+---------------+----------------+
--| James | 2438825627      | Q13SVG6       | (676) 555-6554 | Звонил Taylor
--| Robin |                 | 4V16VO0       | (375) 555-8161 | Звонил Bruce
--+-------+-----------------+---------------+----------------+

SELECT name, passport_number, license_plate, phone_number FROM people
WHERE phone_number = "(375) 555-8161"
OR phone_number = "(676) 555-6554";

--+----------+---------------+-----+------+--------+
--| activity | license_plate | day | hour | minute |
--+----------+---------------+-----+------+--------+
--| entrance | Q13SVG6       | 25  | 8    | 39     |
--| exit     | Q13SVG6       | 25  | 16   | 21     |
--| entrance | 4V16VO0       | 28  | 8    | 50     |
--| exit     | 4V16VO0       | 28  | 8    | 50     |
--| entrance | Q13SVG6       | 29  | 12   | 19     |
--| exit     | Q13SVG6       | 29  | 17   | 43     |
--+----------+---------------+-----+------+--------+
SELECT activity, license_plate, day, hour, minute FROM bakery_security_logs
WHERE year = 2021
AND license_plate = "Q13SVG6"
OR license_plate = "4V16VO0"
ORDER BY day, hour, minute;