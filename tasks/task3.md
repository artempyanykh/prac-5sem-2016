# Assignment 3. Intro to modern programming tools and techniques. Fall '16 - Spring '17

## Description

**Applepen** is a large retail chain that sells two types of products: **apples** and **pens**.
The stores are located in various parts of the US and is serving customers for more than 10 years.

Recently, its top management decided to more actively use their sales data for decision making.
Each store collect the following information:
1. Procurement (apples and pens are procured twice a month).
2. Sales (transaction log, a record per sold item).
3. Inventory (monthly running total of apples and pens in stock).

The data is available in CSV format. Within the file data is sorted by date.

However, the data was never consolidated neither it was checked. Therefore, we need to get the following information.

### 1. Inventory for each day
We need inventory data for each day at the end of the day after all sales and procurement have been completed. This
data will be very valuable for store managers.

The inventory should be calculated based on the monthly totals. There's always some percent of stolen goods, but
currently there's no way to find out how many items were stolen exactly.


The data should be in the following format:

| date       | apple | pen |
|------------|-------|-----|
| 2006-01-01 | 14105 | 770 |
| ...        |       |     |

### 2. Amount of stolen goods per month

The data should be in the following format:

| date       | apple | pen |
|------------|-------|-----|
| 2006-01-31 | 4     | 4   |
| 2006-02-28 | 5     | 0   |
| ...        |       |     |


### 3. Aggregated number of sold and stolen goods per year/state

The data should be in the following format:

| year | state | apple_sold | apple_stolen | pen_sold | pen_stolen |
|------|-------|------------|--------------|----------|------------|
| 2006 | AK    | 4          | 2            | 2        |            |
| 2007 | AL    | 5          | 0            | 6        | 2          |
| ...  |       |            |              |          |            |

## Submission
You can use any programming languages and tools.
The assignment must be completed by a group of 3 to 4.
The process is described in [README](../README.org#submission-rules).

The set of input and output data to test your solution is available at:
https://console.cloud.google.com/storage/browser/artem-pyanykh-cmc-prac-task3-seed17

We recommend you getting familiar with [gcloud](https://cloud.google.com/sdk/gcloud/) command line tools and use `gsutil` to access data in Google Storage.

### Dates

* Submit before 19 March 2016.
* Pass review before 1 Apr 2016.

