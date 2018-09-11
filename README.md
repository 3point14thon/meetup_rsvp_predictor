# showup

## Using machine learning to predict meetup event attendance

### Motivation

Anyone who has thrown an event knows the toil of guessing the number of people to plan for. Plan for too many people and you are left with too much food and an uncomfortably large room or conversely you find your self packed into a small room trying to give away food that will surely spoil if it can't find a home.

By giving an estimated range of people I aim to alleviate some of this frustration.

### Product

The website is currently working locally and will soon be accessible via the world wide web.

To get a prediction for your event input the event details, then hit the "RSVP" button.

The model was integrated into the website via flask and the site is self-hosted on AWS.

### Data

All the data I used in the project was gathered through meetups' API. (link API here)

The data that is currently in use in this project is half the events within 100 miles of Seattle from August 8th 2015 to August 8th 2018 (about 155k events) but I hope to expand this to national data for the same time frame.

The data included in this repo is the half currently being used. The entire corpus of data is stored in a mongo db.

### Modeling

#### Features
The model takes 6 inputs:

Name Tfidf
Description Tfidf
Description word count
Month of year
Day of week
Time of Day

I filled missing description and name values with empty strings after confirming that this is consistant with how the description/name would be displayed on the meetup website.

#### Scoring and Label Processing
The "yes_rsvp_count" and "waitlist_count" columns from the original meetup data were summed together to get total attendance. This was then loged + 1 ,log(y + 1). Mean squared error was used as the performance metric but was empleminted before the labels or predictions were converted back from log form. The end result is a scoring metric that behaves like mean squared log error.

#### Model Selection
I tried both a poisson regression and a random forest regressor at several hyperparameters. Ultimately random forest outperformed the poisson regression. Getting an average three fold cross validation score of 0.66 opposed to the random forests score of 0.44.

For the final model I increased the number of trees to 1,000 resulting in a test score of 0.36. Using the average of the training data attendance as our prediction gets a score of 0.77 for comparison.
