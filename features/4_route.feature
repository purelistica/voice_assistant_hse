# Created by vadim at 1/23/19
Feature: Route Setup
 Assistant sets up route between two places and tells its duration

 Scenario: Assistant sets up route between two saved places on foot
  Given service is working
  And locations Пашин дом and Библиотека are saved
  When user says "Hello, Borya"
  Then VA says "Hello"
  When user says Set up route from Пашин дом to Библиотека
  Then VA validates locations
  When VA asks "Which way?"
  And User says go by foot
  Then VA says time
  #  optional
  When user gives command to start the route
  Then VA follows the route

  Scenario: Assistant sets up route between two saved places, but location(s) does not exist
  Given service is working
  When user says "Hello, Borya"
  Then VA says "Hello"
  When user says Set up route from Университет to Общага
  Then VA validates locations
  And VA says "Invalid location(s)"

 Scenario: Assistant sets up route between two saved places by car
  Given service is working
  And locations Пашин дом and Библиотека are saved
  When user says "Hello, Borya"
  Then VA says "Hello"
  When user says Set up route from Пашин дом to Библиотека
  Then VA validates locations
  When VA asks "Which way?"
  And User says go by car
  Then VA says time

 Scenario: Assistant sets up route between two saved places by public transport
  Given service is working
  And locations Пашин дом and Библиотека are saved
  When user says "Hello, Borya"
  Then VA says "Hello"
  When user says Set up route from Пашин дом to Библиотека
  Then VA validates locations
  When VA asks "Which way?"
  And User says go by transport
  Then VA says time

 Scenario: Assistant sets up route between the current location and the saved place by car
  Given service is working
  And locations Пашин дом and Библиотека are saved
  When user says "Hello, Borya"
  Then VA says "Hello"
  When user says Set up route to Библиотека
  Then VA validates locations
  When VA asks "Which way?"
  And User says go by car
  Then VA says time

 Scenario: Assistant sets up route between the current location and the saved place by car
  Given service is working
  And locations Пашин дом and Библиотека are saved
  When user says "Hello, Borya"
  Then VA says "Hello"
  When user says Set up route to Библиотека
  Then VA validates locations
  When VA asks "Which way?"
  And user says choose the fastest mode
  Then VA names the travel mode
  And VA says time
