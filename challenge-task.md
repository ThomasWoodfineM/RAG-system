# Challenge-Task

## 1) Description

Create a RAG system in Python for a short demo and explanation at our next meeting.
The RAG system should use the below mentioned report.md file to answer as many questions as possible
from section 2.

* The solution can be done locally on your laptop or on an online-plattform like google colab as long as it is presentable at the next meeting.
* The solution needs to scale well even with files much larger than the provided example and with lagrger textblocks in between. (so, no cheating with big models that can take the entire example file as context :-) )
* Bonus: consider tables much larger than the ones provided in the example file.
* Answer each question with preferably 1 LLM call or provide good reasons otherwise.
* In addition to the answer, the solution needs to print out the final prompt, including the contexts.

#### Notes:

The report.md is in Markdown format and can be copy/pasted and viewed in https://dillinger.io/ if no local installation of a markdown viewer 
is available.


## 2) Questions to answer:

* How many pizzas did Andy buy in 2022?
* Did Marta eat any pizza from year 2020 to year 2022?
* In which years did Sam eat more than one pizza?


# report.md:
---

# Consumed 

Our test subjectcs consumed various types of food and drinks during the tracked years. Here are the consumption
statistics of our most important test subjects.

## Food

Although various kinds of foods have been tracked during the given timeframe, in this report we are concentrating on on a tiny subset. Pizza and Tomato-Soup in particular.

#### Pizza

This table shows ammount of whole pizzas eaten by Sam and Andy during the recorded timeframe. 

| Person | 2020 | 2021 |  2022 |
|--------|------|------|-------|
| Sam    |  0   | 12   | 13    |
| Andy   | 1    | 3    | 1     |

### Tomato-Soup

Tomato-soup has been tracked for an additional year due to reasons outlined in the main report.

| Person | 2020 | 2021 |  2022 | 2023 |
|--------|------|------|-------|------|
| Sam    | 1    | 0    | 3     | 0    |
| Andy   | 1    | 3    | 4     | 0    |

## Drinks

#### Water

| Person | 2020 | 2021 |  2022 |
|--------|------|------|-------|
| Sam    | 9    | 9    | 9     |
| Andy   | 9    | 9    | 9     |

#### Juice

| Person | 2020 | 2021 |  2022 |
|--------|------|------|-------|
| Sam    | 3    | 3    | 3     |
| Andy   | 3    | 3    | 3     |


# Purchased

## Food

#### Pizza

Both sam and Andy purchased 4 pizzas each year from 2020 to 2022.

### Tomato-Soup

In the case of Tomato-Soup, the purchases allign perfectly with consumption.

| Person | 2020 | 2021 |  2022 | 2023 |
|--------|------|------|-------|------|
| Sam    | 1    | 0    | 3     | 0    |
| Andy   | 1    | 3    | 4     | 0    |