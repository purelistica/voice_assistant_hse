Feature: delete saved place
  Deleting place which was saved

  Scenario: User asks to delete saved place and VA removes it from storage
    Given service is working
    And location Библиотека is saved
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says delete Библиотека
    Then VA validates input
    When VA asks for confirmation
    And User confirms
    Then VA deletes place
    And VA says "Done"

  Scenario: User asks to delete saved place, but changes his mind
    Given service is working
    And location Библиотека is saved
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says delete Библиотека
    Then VA validates input
    When VA asks for confirmation
    And User does not confirm
    Then VA says "Cancelled"

  Scenario: User asks to delete saved place, but it does not exist
    Given service is working
    And location Библиотека is saved
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says delete Пашин дом
    Then VA validates input
    Then VA says "The place is not found"
