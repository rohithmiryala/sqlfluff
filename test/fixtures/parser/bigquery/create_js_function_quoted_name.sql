CREATE TEMP FUNCTION
qs(
    y STRING
)
RETURNS STRUCT<`$=` ARRAY<INT64>>
LANGUAGE js AS """
    CODE GOES HERE
"""
