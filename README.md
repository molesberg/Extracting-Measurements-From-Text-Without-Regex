# ExtractingMeasurementsFromTextWithoutRegex
Code from July 2023.
Problem inspiration: I have a relational database with a text field of notes, which may include measurements of windows. I want to extract any construction measurements from the notes and write them into float fields for width, height, and thickness so that my database is more machine readable in the future.

Each section of notes will have no more than five (5) window measurements in it. Measurement units may be noted as inches (“), feet (‘), or not marked. Measurements are assumed to be in Width X Height X Thickness unless otherwise marked. 

In 2024 I learned how to use Regular Expressions (Regex) and rewrote this code in a much more efficient manner. I would recommend anyone with a similar problem set just use Regex, but this code was still fun to build.
