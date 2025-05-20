import time as t
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    while True:
        city = input("Please enter a city name (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please try again.")

    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June or 'all'? ").lower()
        if month in months:
            break
        else:
            print("Invalid month. Please try again.")

    # Get user input for day
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? (Monday, Tuesday, ..., Sunday or 'all'): ").lower()
        if day in days:
            break
        else:
            print("Invalid day. Please try again.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = t.time()

    print('Most Common Month:', df['month'].mode()[0].title())
    print('Most Common Day of Week:', df['day_of_week'].mode()[0].title())
    print('Most Common Start Hour:', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-' * 40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = t.time()

    print('Most Commonly Used Start Station:', df['Start Station'].mode()[0])
    print('Most Commonly Used End Station:', df['End Station'].mode()[0])

    df['Trip Combination'] = df['Start Station'] + " to " + df['End Station']
    print('Most Common Trip from Start to End:', df['Trip Combination'].mode()[0])

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = t.time()

    print('Total Travel Time:', df['Trip Duration'].sum())
    print('Average Travel Time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-' * 40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = t.time()

    print('User Type Counts:\n', df['User Type'].value_counts())

    if 'Gender' in df:
        print('\nGender Counts:\n', df['Gender'].value_counts())

    if 'Birth Year' in df:
        print('\nEarliest Birth Year:', int(df['Birth Year'].min()))
        print('Most Recent Birth Year:', int(df['Birth Year'].max()))
        print('Most Common Birth Year:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no: ').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()