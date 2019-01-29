Feature: Edit place name
  Assistant finds saved place and reassigns name or address

  Scenario: User asks to edit saved name and VA reassigns old name
    Given service is working
    And location Библиотека is saved
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says edit Библиотека
    Then VA validates input
    And VA asks "What would you like to change, name or address?"
    When user says change name
    Then VA asks "What is the new name?"
    When User says new name is Унылое место
    Then VA validates input
    When VA names updated location
    And VA asks for confirmation
    And User confirms
    Then VA updates location
    And VA says "Done"

  Scenario: User asks to edit saved name and VA reassigns address
    Given service is working
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says edit Унылое место
    Then VA validates input
    And VA asks "What would you like to change, name or address?"
    When user says change address
    Then VA asks "What is the new address?"
    When User says new address is улица Седова 55
    Then VA validates input
    When VA names updated location
    And VA asks for confirmation
    And User confirms
    Then VA updates location
    And VA says "Done"

  Scenario: User asks to edit saved name, but it does not exist
    Given service is working
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says edit Библиотека
    Then VA validates input
    And VA says "The place is not found"

  Scenario: User asks to edit saved name, but VA can't recognize new name
    Given service is working
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says edit Унылое место
    Then VA validates input
    And VA asks "What would you like to change, name or address?"
    When user says change name
    Then VA asks "What is the new name?"
    When User says nothing
    Then VA says 'Can't recognize name'
